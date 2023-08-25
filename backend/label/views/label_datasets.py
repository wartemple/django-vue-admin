from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from rest_framework.decorators import action
from django.db import transaction
from label.models import LabelDatasets
from dvadmin.utils.json_response import SuccessResponse
from rest_framework.request import Request
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.json_response import DetailResponse, SuccessResponse
from dvadmin.utils.permission import AnonymousUserPermission


class LabelDatasetsSerializer(CustomModelSerializer):
    class Meta:
        model = LabelDatasets
        fields = '__all__'
        read_only_fields = ["id"]


class LabelDatasetsViewSet(CustomModelViewSet):
    """
    标注数据接口
    统计接口：仅统计已标注完成的记录
    同步数据集接口： sync,同步所有数据集当前已标注和未标注的数据
    """
    permission_classes = []
    queryset = LabelDatasets.objects.all()
    extra_filter_backends = []
    serializer_class = LabelDatasetsSerializer
    create_serializer_class = LabelDatasetsSerializer

    @action(methods=['get'], detail=True)
    @transaction.atomic  # Django 事务,防止出错
    def sync_argilla(self, request: Request, *args, **kwargs):
        """同步 argilla的数据
        1. 初始化dataset
        2. 实时获取records状态
        3. 新增records
        """
        dataset = self.get_object()
        dataset.records.all()
        argilla_dataset = dataset.argilla_instance()

    @action(methods=["GET"], detail=False, permission_classes=[AnonymousUserPermission])
    def statistics(self, request, *args, **kwargs):
        """以领域和任务为唯一值进行统计"""
        return DetailResponse(data={}, msg="获取成功")