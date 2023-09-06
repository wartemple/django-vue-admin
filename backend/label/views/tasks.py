import re

from django.db import transaction
from dvadmin.utils.import_export import import_to_data
from dvadmin.utils.json_response import DetailResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from label.models import Tasks, Samples, Dataset
from label.views.samples import SampleSerializer
# Create your views here.
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.request import Request


class TasksSerializer(CustomModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    schedule = serializers.SerializerMethodField(read_only=True)

    def get_schedule(self, instance):
        return str(instance.submitted_count / instance.samples.count() * 100) if instance.samples.count() != 0 else '0'
        
    def get_status(self, instance):
        if instance.samples.count() == 0:
            return False
        if instance.submitted_count / instance.samples.count() >=1:
            return True
        return False

    def validate_name(self, attrs):
        if not re.search("^(?!-|_)[a-zA-Z0-9-_ ]+$", self.initial_data.get('name')):
            raise serializers.ValidationError("输入数据集名称，不能包含中文")
        return attrs

    class Meta:
        model = Tasks
        fields = '__all__'
        read_only_fields = ["id"]


class TasksViewSet(CustomModelViewSet):
    """
    标注数据接口
    统计接口：仅统计已标注完成的记录
    同步数据集接口： sync,同步所有数据集当前已标注和未标注的数据
    """
    permission_classes = []
    queryset = Tasks.objects.all()
    extra_filter_backends = []
    serializer_class = TasksSerializer
    create_serializer_class = TasksSerializer
    search_fields = ['name']
    filter_fields = ['name',]
    sample_import_field_dict = {
        "domain": "领域", "power": "权能", "lang": "语言", "prompt": "提示词",
        "input": "输入文本", "output": "输出文本", "source": "来源"
    }

    @action(methods=['get'], detail=True)
    @transaction.atomic  # Django 事务,防止出错
    def sync_argilla(self, request: Request, *args, **kwargs):
        """同步 argilla的数据
        1. 初始化dataset
        2. 实时获取records状态
        3. 新增records
        """
        task = self.get_object()
        count = 0
        for ag_record in task.argilla_instance:
            if not ag_record.responses:
                obj = Samples.objects.filter(pk=ag_record.fields['id'])
                obj.update(**{
                    "new_prompt": "",
                    "new_input": "",
                    "new_output": "",
                })
                continue
            response = ag_record.responses[0]
            obj = Samples.objects.filter(pk=ag_record.fields['id'])
            obj.update(**{
                "new_prompt":response.values['new-prompt'].value,
                "new_input":response.values['new-input'].value,
                "new_output":response.values['new-output'].value,
            })
            if response.status == 'submitted':
                count += 1
        task.submitted_count = count
        task.save()
        return DetailResponse(msg="同步成功！")

    @action(methods=['get'], detail=True)
    @transaction.atomic  # Django 事务,防止出错
    def sync_argilla(self, request: Request, *args, **kwargs):
        """同步 argilla的数据
        1. 初始化dataset
        2. 实时获取records状态
        3. 新增records
        """
        task = self.get_object()
        count = 0
        for ag_record in task.argilla_instance:
            if not ag_record.responses:
                obj = Samples.objects.filter(pk=ag_record.fields['id'])
                obj.update(**{
                    "new_prompt": "",
                    "new_input": "",
                    "new_output": "",
                })
                continue
            response = ag_record.responses[0]
            obj = Samples.objects.filter(pk=ag_record.fields['id'])
            obj.update(**{
                "new_prompt":response.values['new-prompt'].value,
                "new_input":response.values['new-input'].value,
                "new_output":response.values['new-output'].value,
            })
            if response.status == 'submitted':
                count += 1
        task.submitted_count = count
        task.save()
        return DetailResponse(msg="同步成功！")
    
    @action(methods=['post'], detail=True)
    @transaction.atomic  # Django 事务,防止出错
    def import_samples(self, request: Request, *args, **kwargs):
        """标注任务导入样本数据"""
        task = self.get_object()
        if task.samples.count() > 0:
            raise ValueError('暂不支持追加样本')
        import_field_dict = {'id':'更新主键(勿改)',**self.sample_import_field_dict}
        data = import_to_data(request.data.get("file"), import_field_dict)
        for item in data:
            item['task'] = task.id
            serializer = SampleSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        task.push_records()
        task.sample_sum = len(data)
        task.save()
        return DetailResponse(msg="导入成功！")

    @action(methods=['get'], detail=True)
    @transaction.atomic  # Django 事务,防止出错
    def publish_dataset(self, request: Request, *args, **kwargs):
        task = self.get_object()
        Dataset._copy_from_task(task)
        return DetailResponse(msg="发布成功！")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        instance.delete_ag()
        return DetailResponse(data=[], msg="删除成功")

