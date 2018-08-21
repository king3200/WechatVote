from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from Vote.models import VoteEvent, Voter, VotingItem
from Vote.serializers import VoteEventSerializer


class Index(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        return Response('hello world')


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
        print(request.data)
        proj_id = request.data.get('projId', None)
        item_id = request.data.get('id', None)
        if not item_id:
            return Response({'detail': '没有参数id'}, status=status.HTTP_400_BAD_REQUEST)

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        user_agent = request.META.get('HTTP_USER_AGENT', None)
        platform = 1 if 'MicroMessenger' in user_agent else 2

        try:
            proj = VoteEvent.objects.get(id=proj_id)
            item = VotingItem.objects.get(id=item_id)
        except (VotingItem.DoesNotExist, IndexError):
            return Response({'detail': '找不到投票对象'}, status=status.HTTP_400_BAD_REQUEST)

        #判断item是否隶属于proj
        if item not in proj.items.all():
            return Response({'detail': '参数错误'}, status=status.HTTP_400_BAD_REQUEST)

        voter = Voter.objects.filter(ip=ip, event=proj).order_by('vote_time').last()
        if voter:
            if item in proj.items.all() and voter.can_vote() and item.vote(ip, platform):
                pass
            else:
                return Response({'detail': '今天已经投过票了'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not item.vote(ip=ip, platform=platform):
                return Response({'detail': '今天已经投过票了'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)




