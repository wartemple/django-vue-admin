from django.urls import path
from rest_framework import routers

from label.views.samples import SampleViewSet
from label.views.tasks import TasksViewSet
from label.views.dataset import DatasetViewSet
from label.views.label_results import LabelResultsViewSet

system_url = routers.SimpleRouter()
system_url.register(r'samples', SampleViewSet, basename='samples')
system_url.register(r'tasks', TasksViewSet, basename='tasks')
system_url.register(r'datasets', DatasetViewSet, basename='datasets')
system_url.register(r'label_results', LabelResultsViewSet, basename='label_results')
urlpatterns = [
]
urlpatterns += system_url.urls
