__author__ = 'Philip'

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^$', views.ChoreList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.ChoreDetail.as_view()),
    url(r'^assign/(?P<pk>[0-9]+)/$', views.AssignChore.as_view()),
    url(r'^complete/(?P<pk>[0-9]+)/$', views.CompleteChore.as_view()),
    url(r'^delete_all/$', views.DeleteAllChores.as_view()),
    url(r'^remove_assignments/$', views.RemoveAllAssignments.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)