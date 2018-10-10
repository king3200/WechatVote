import hashlib
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from Vote.models import VoteEvent, Voter, VotingItem
from Vote.serializers import VoteEventSerializer
from WechatVote import we_settings, settings
from WechatVote.utils import wx_get_openid, wx_check_subscribe
from WechatVote.we_settings import wx_appID


class WXTokenAccess(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
        token = we_settings.wx_token

        access_paras = sorted([token, timestamp, nonce])
        access_paras_str = ''.join(access_paras)
        sha1_str = hashlib.sha1(access_paras_str.encode('utf-8')).hexdigest()
        if sha1_str == signature:
            return HttpResponse(echostr)
        else:
            return Response('微信认证失败', status=status.HTTP_400_BAD_REQUEST)


class Index(APIView):

    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        """
        根据项目ID获取投票页面
        :param request:
        :param projid:
        :return:
        """
        url = '''https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_base&state=123#wechat_redirect
        '''.format(wx_appID, 'http%3A%2F%2Fvote.xinwo.online%2Fwx-callback')
        return HttpResponseRedirect(url)


class VoteIndex(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        # 检查是否关注公众号
        if 'openid' in request.session and 'access_token' in request.session:
            if wx_check_subscribe(request.session['openid']):
                return render_to_response('index.html')
            else:
                return render_to_response('error.html', {'msg': '请先关注公众号才能投票哦'})
        return render_to_response('error.html', {'msg': '请使用微信公众号进入该页面'})
        # request.session['openid'] = 'oJKPqw5vR4FqqZRcjq8c4Uaf9aKo'
        # return render_to_response('index.html')


class WXCallback(APIView):

    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        """
        微信端用户登录回调
        :param request:
        :return:
        """
        code = request.GET.get('code', None)
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': '参数错误'})
        wx_openid_json = wx_get_openid(code)
        wx_openid = wx_openid_json['openid']
        wx_access_token = wx_openid_json['access_token']

        #判断是否已关注公众号
        # if wx_check_subscribe(wx_openid):
            # 写入session
        request.session['openid'] = wx_openid
        request.session['access_token'] = wx_access_token
        return HttpResponseRedirect('/voteindex')
        # else:
        #     return render_to_response('error.html', {'error': '请先关注公众号'})


class VoteEventRetrive(RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
    lookup_field = 'id'
    queryset = VoteEvent.objects.all()
    serializer_class = VoteEventSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_open:
            return Response({'detail': '该项目未开放'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class Voting(APIView):

    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):

        proj_id = request.data.get('projId', None)
        item_id = request.data.get('id', None)
        if not item_id:
            return Response({'detail': '没有参数'}, status=status.HTTP_400_BAD_REQUEST)

        # 使用微信openid记录投票， IP地址太多内网用户了~~~
        # if 'HTTP_X_FORWARDED_FOR' in request.META:
        #     ip = request.META['HTTP_X_FORWARDED_FOR']
        # else:
        #     ip = request.META['REMOTE_ADDR']

        # test session
        # request.session['openid'] = 'asdfggg'

        if 'openid' not in request.session:
            return Response({'detail': '请使用微信渠道投票'}, status=status.HTTP_400_BAD_REQUEST)

        ip = request.session['openid']

        user_agent = request.META.get('HTTP_USER_AGENT', None)
        platform = 1 if user_agent and 'MicroMessenger' in user_agent else 2

        try:
            proj = VoteEvent.objects.get(id=proj_id)
            item = VotingItem.objects.get(id=item_id)
        except (VotingItem.DoesNotExist, IndexError):
            return Response({'detail': '找不到投票对象'}, status=status.HTTP_400_BAD_REQUEST)

        #判断item是否隶属于proj
        if item not in proj.items.all():
            return Response({'detail': '参数错误'}, status=status.HTTP_400_BAD_REQUEST)

        if item in proj.items.all() and item.vote(ip, platform):
            pass
        else:
            return Response({'detail': '每个用户每天只能投%d票' % settings.vote_times}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
