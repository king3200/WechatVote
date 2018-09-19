from django.test import TestCase
from rest_framework.test import APITestCase, APIClient

from Vote.models import VoteEvent, VotingItem


class TestVote(APITestCase):

    def setUp(self):
        event = VoteEvent.objects.create(name='视频大赛', start_date='2018-9-15', end_date='2018-9-30',
                                 desc='测试视频大赛投票', is_open=True)
        item1 = VotingItem.objects.create(name='重医附一院', avatar_url='https://gw.alipayobjects.com/zos/rmsportal/JjNULDGGwgOZmsZAqvjH.png',
                                          desc = '李医生的视频', info_url='http://www.baidu.com', event=event)
        item2 = VotingItem.objects.create(name='重医附2院', avatar_url='https://gw.alipayobjects.com/zos/rmsportal/JjNULDGGwgOZmsZAqvjH.png',
                                          desc='王医生的视频', info_url='http://www.baidu.com', event=event)
        item3 = VotingItem.objects.create(name='重医附3院', avatar_url='https://gw.alipayobjects.com/zos/rmsportal/JjNULDGGwgOZmsZAqvjH.png',
                                          desc='周医生的视频', info_url='http://www.baidu.com', event=event)
        self.items = [item1, item2, item3]

        self.evt_id = event.id
        self.client = APIClient()

    def test_get_vote_proj(self):

        response = self.client.get('/retrive/1')
        self.assertEqual(response.status_code, 200)

    def test_voting(self):
        response = self.client.post('/voting', data={'projId': self.evt_id, 'id': self.items[1].id},
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.items[1].counter, 1)
        response = self.client.post('/voting', data={'projId': self.evt_id, 'id': self.items[1].id},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, '今天已经投过票了')

