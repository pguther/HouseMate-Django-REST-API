from django.db import models

class Chore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='', blank=True)
    owner = models.ForeignKey('auth.User', related_name='chores')
    assigned_to = models.ForeignKey('auth.User', related_name='assigned_to', blank=True, null=True)
    assigned = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    due_day = models.TextField(max_length=10, default='')
    expired = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    claimed_by = models.ForeignKey('auth.User', related_name='assigned_chores')

    '''
    group_id = models.IntegerField()
    weekday = models.IntegerField()
    day = models.CharField(max_length=20)
    description = models.TextField()
    completed = models.BooleanField()
    expired = models.BooleanField()
    claimed = models.BooleanField()
    claimed_by = models.CharField(max_length=100)
    '''

    class Meta:
        ordering = ['created']


class Group(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey('auth.User')
