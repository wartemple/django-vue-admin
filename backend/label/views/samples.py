
from label.models import Samples
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer

import logging

logger = logging.getLogger(__name__)

class SampleSerializer(CustomModelSerializer):
    class Meta:
        model = Samples
        fields = '__all__'
        read_only_fields = ["id"]


class SampleImportSerializer(CustomModelSerializer):

    def is_valid(self, *, raise_exception=False):
        self.initial_data['dataset'] = self.request.data.get('dataset')
        return super().is_valid(raise_exception=raise_exception)

    class Meta:
        model = Samples
        fields = '__all__'
        read_only_fields = ["id"]


class SampleViewSet(CustomModelViewSet):
    """
    标注数据接口
    统计接口：仅统计已标注完成的记录
    同步数据集接口： sync,同步所有数据集当前已标注和未标注的数据
    """
    permission_classes = []
    queryset = Samples.objects.all()
    extra_filter_backends = []
    serializer_class = SampleSerializer
    create_serializer_class = SampleSerializer
    export_serializer_class = SampleSerializer
    import_serializer_class = SampleImportSerializer
    filter_fields = ['task',]
    export_field_label = {
        "domain": "领域", "task": "任务类型", "lang": "语言", "prompt": "提示词",
        "input": "输入文本", "output": "输出文本", "source": "来源"
    }
    import_field_dict = {
        "domain": "领域", "task": "任务类型", "lang": "语言", "prompt": "提示词",
        "input": "输入文本", "output": "输出文本", "source": "来源"
    }
