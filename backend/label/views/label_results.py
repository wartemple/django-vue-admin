
from label.models import LabelResults
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from dvadmin.utils.json_response import SuccessResponse
from django.db.models import Count
import logging

logger = logging.getLogger(__name__)

class LabelResultsSerializer(CustomModelSerializer):
    class Meta:
        model = LabelResults
        fields = '__all__'
        read_only_fields = ["id"]


class LabelResultsViewSet(CustomModelViewSet):
    """
    标注数据接口
    统计接口：仅统计已标注完成的记录
    同步数据集接口： sync,同步所有数据集当前已标注和未标注的数据
    """
    permission_classes = []
    queryset = LabelResults.objects.all()
    extra_filter_backends = []
    serializer_class = LabelResultsSerializer
    export_serializer_class = LabelResultsSerializer
    create_serializer_class = LabelResultsSerializer
    filter_fields = ['dataset', ]
    import_field_dict = {
        "domain": "领域", "power": "权能", "lang": "语言", "source": "来源",
        "prompt": "提示词", "input": "输入文本", "output": "输出文本",
        "new_prompt": "标注提示词", "new_input": "标注输入文本", "new_output": "标注输出文本"
    }

    export_field_label = {
        "domain": "领域", "power": "权能", "lang": "语言", "source": "来源",
        "prompt": "提示词", "input": "输入文本", "output": "输出文本",
        "new_prompt": "标注提示词", "new_input": "标注输入文本", "new_output": "标注输出文本"
    }

    @action(methods=['get'], detail=False)
    def statistics(self, request: Request, *args, **kwargs):
        result = self.queryset.order_by('sample_id').values('domain', 'power').order_by().annotate(count=Count('sample_id', distinct=True))
        return SuccessResponse(data=[{"value": _['count'], "name": f"{_['domain']}-{_['power']}"} for _ in result])
