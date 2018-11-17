from django.utils import timezone
from django.conf import settings
from django.db import models

import WechatVote


class VoteEvent(models.Model):
    name = models.CharField(max_length=128, verbose_name='标题')
    start_date = models.DateField(verbose_name='开始时间')
    end_date = models.DateField(verbose_name='结束时间')
    desc = models.TextField(verbose_name='投票简介')
    is_open = models.BooleanField(default=True, verbose_name='是否开放')

    def __str__(self):
        return '%d-%s' % (self.id, self.name)

    class Meta:
        verbose_name = '投票项目'
        verbose_name_plural = '投票项目'


class VotingItem(models.Model):
    name = models.CharField(max_length=64, verbose_name='名称')
    org = models.CharField(max_length=32, verbose_name='机构名称', blank=True, null=True, default=None)
    avatar_url = models.URLField(verbose_name='头像链接')
    desc = models.TextField(verbose_name='介绍', blank=True, default='')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    info_url = models.URLField(blank=True, null=True, verbose_name='详情链接')
    event = models.ForeignKey(VoteEvent, on_delete=models.SET_NULL, null=True, verbose_name='归属', related_name='items')
    counter = models.IntegerField(default=0)

    @property
    def avatar(self):
        if not self.avatar_url:
            return '%s/%s' % (settings.AVATAR_PREFIX, self.avatar_url)

    def __str__(self):
        return '<VotingItem # %d:%s>' % (self.id, self.name)

    def vote(self, ip, platform, item=None):
        #判断ip在今天的总票数是否超过限制
        voter_list = Voter.objects.filter(ip=ip, event=self.event, vote_time__day=timezone.now().day)
        if voter_list.count() >= settings.VOTE_TIME:
            return False

        #可以投票：规则0 判断ip在这个项目上是否已投过票
        if settings.VOTE_RULE == 0:
            if voter_list.filter(vote_item=self).exists():
                return False
            else:
                Voter.objects.create(ip=ip, platform=platform, event=self.event, vote_item=self,
                                             vote_count=1, vote_time=timezone.now())
        #可以投票： 规则1  ip可以把票投给相同项目
        elif settings.VOTE_RULE == 1:
            Voter.objects.create(ip=ip, platform=platform, event=self.event, vote_item=self,
                                         vote_count=1, vote_time=timezone.now())
        else:
            print('settings.vote_rule can only be 1 or 2, but now is %s' % str(settings.vote_rule))
            return False

        # voters = Voter.objects.filter(ip=ip, event=self.event, vote_item=self)
        # if not voters.exists():
        #     voter = Voter(ip=ip, platform=platform, event=self.event, vote_item=self)
        # else:
        #     voter = voters[0]
        #     if not voter.can_vote():
        #         return False

        self.counter += 1
        # voter.vote_time = timezone.now()
        # voter.save()
        self.save()

        return True

    class Meta:
        verbose_name = '投票对象'
        verbose_name_plural = '投票对象'


class Voter(models.Model):
    platform_choices = [
        (1, '微信'),
        (2, '网页')
    ]
    event = models.ForeignKey(VoteEvent, on_delete=models.CASCADE, related_name='voters')
    ip = models.CharField(max_length=32)
    platform = models.IntegerField(choices=platform_choices)
    vote_time = models.DateTimeField(default=timezone.now, verbose_name='投票时间')
    vote_count = models.IntegerField(default=1)
    vote_item = models.ForeignKey(VotingItem, on_delete=models.SET_NULL, related_name='voters', null=True, default=None)

    def can_vote(self):
        time_diff = timezone.now().day - self.vote_time.day
        if time_diff >= 1:
            self.vote_count = 0

        if self.vote_count < WechatVote.settings.vote_times:
            self.vote_count += 1
            self.save()
            return True
        return False

    class Meta:
        verbose_name = '投票者'
        verbose_name_plural = '投票者'


class WeChatOpenID(models.Model):
    openid = models.CharField(max_length=64)
    access_token = models.CharField(max_length=128)
