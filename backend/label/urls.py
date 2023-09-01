from django.urls import path
from rest_framework import routers

from label.views.samples import SampleViewSet
from label.views.tasks import TasksViewSet

system_url = routers.SimpleRouter()
system_url.register(r'samples', SampleViewSet, basename='samples')
system_url.register(r'tasks', TasksViewSet, basename='tasks')
urlpatterns = [
]
urlpatterns += system_url.urls
