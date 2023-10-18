
from label.models import Dataset
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import serializers
from dvadmin.utils.json_response import DetailResponse
from django.db import transaction
from dvadmin.utils.import_export import import_to_data
from label.views.label_results import LabelResultsSerializer
import logging
from tqdm.contrib import tenumerate


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
    result_import_field_dict = {
        "domain": "领域", "power": "权能", "lang": "语言", "source": "来源",
        "prompt": "提示词", "input": "输入文本", "output": "输出文本",
        "new_prompt": "标注提示词", "new_input": "标注输入文本", "new_output": "标注输出文本"
    }

    @action(methods=['post'], detail=True)
    @transaction.atomic  # Django 事务,防止出错
    def import_results(self, request: Request, *args, **kwargs):
        """标注任务导入样本数据"""
        dataset = self.get_object()
        # if dataset.samples.count() > 0:
        #     raise ValueError('暂不支持追加样本')
        import_field_dict = {'id':'更新主键(勿改)',**self.result_import_field_dict}
        data = import_to_data(request.data.get("file"), import_field_dict)
        for index, item in tenumerate(data):
            item['dataset'] = dataset.id
            item['sample_id'] = f"custom-{dataset.id}-{index}"
            for key in self.result_import_field_dict.keys():
                if not item.get(key):
                    item[key] = '无'
            serializer = LabelResultsSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return DetailResponse(msg="导入成功！")