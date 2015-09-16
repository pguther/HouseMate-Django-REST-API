__author__ = 'Philip'

from django.forms import widgets
from rest_framework import serializers
from api.models import Chore
from django.contrib.auth.models import User

class ChoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chore
        fields = ('id', 'name', 'owner', 'description','assigned_to', 'assigned', 'claimed', 'claimed_by', 'completed', 'due_day', 'expired')

    owner = serializers.ReadOnlyField(source='owner.username')
    assigned_to = serializers.ReadOnlyField(source='assigned_to.username')

    def create(self, validated_data):
        return Chore.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.assigned = validated_data.get('assigned', instance.assigned)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance

        '''
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    group_id = serializers.IntegerField()
    weekday = serializers.IntegerField()
    day = serializers.CharField(required=True, allow_blank=False, max_length=100)
    description = serializers.TextField()
    assigned = serializers.BooleanField(required=True)
    assigned_to = serializers.CharField(required=False, allow_blank=True, max_length=20)
    completed = serializers.BooleanField()
    expired = serializers.BooleanField()
    claimed = serializers.BooleanField()
    claimed_by = serializers.CharField(required=False, allow_blank=True, max_length=100)
    '''