from django.utils import timezone
from django.conf import settings
from django.db import models


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

    def vote(self, ip, platform):
        voters = Voter.objects.filter(ip=ip, event=self.event)
        if not voters.exists():
            voter = Voter(ip=ip, platform=platform, event=self.event)
        else:
            voter = voters[0]
            if not voter.can_vote():
                return False

        self.counter += 1
        voter.vote_time = timezone.now()
        voter.save()
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

    def can_vote(self):
        time_diff = timezone.now().day - self.vote_time.day
        if time_diff >= 1:
            return True
        return False

    class Meta:
        verbose_name = '投票者'
        verbose_name_plural = '投票者'