from django.urls import path
from rest_framework import routers

from label.views.records import RecordsViewSet
from label.views.label_datasets import LabelDatasetsViewSet

system_url = routers.SimpleRouter()
system_url.register(r'records', RecordsViewSet, basename='records')
system_url.register(r'datasets', LabelDatasetsViewSet, basename='datasets')
urlpatterns = [
]
urlpatterns += system_url.urls
