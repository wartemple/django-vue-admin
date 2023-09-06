
from label.models import Dataset
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)

class DatasetSerializer(CustomModelSerializer):
    result_count = serializers.SerializerMethodField(read_only=True)

    def get_result_count(self, instance):
        return instance.label_results.count()
    
    class Meta:
        model = Dataset
        fields = '__all__'
        read_only_fields = ["id"]


class DatasetViewSet(CustomModelViewSet):
    """
    标注数据接口
    统计接口：仅统计已标注完成的记录
    同步数据集接口： sync,同步所有数据集当前已标注和未标注的数据
    """
    permission_classes = []
    queryset = Dataset.objects.all()
    extra_filter_backends = []
    serializer_class = DatasetSerializer
    create_serializer_class = DatasetSerializer
