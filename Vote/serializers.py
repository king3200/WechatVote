from rest_framework import serializers
from Vote.models import VoteEvent, VotingItem, Voter


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'


class VoteItemSerializer(serializers.ModelSerializer):

    def vote(self):
        self.validated_data['counter'] += 1
        print(self.instance)

    class Meta:
        model = VotingItem
        fields = '__all__'


class VoteEventSerializer(serializers.ModelSerializer):
    items = VoteItemSerializer(many=True, read_only=True)
    is_open = serializers.BooleanField()

    class Meta:
        model = VoteEvent
        fields = '__all__'