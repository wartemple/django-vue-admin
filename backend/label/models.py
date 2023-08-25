from django.db import models

from dvadmin.utils.models import CoreModel
import argilla as rg
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

rg.init(api_url=settings.ARGILLA_API_URL, api_key=settings.ARGILLA_API_KEY)

class LabelDatasets(CoreModel):
    name = models.CharField(verbose_name="数据集名称", max_length=128, null=False)

    question_configs = [
        {"name": "new-prompt", "title": "纠正提示词", "description": "若提示词错误，直接进行更新，若无错误直接复制原始提示词即可"},
        {"name": "new-input", "title": "纠正输入文本", "description": "若输入文本错误，直接进行更新，若无错误直接复制原始输入文本即可"},
        {"name": "new-output", "title": "纠正输出文本", "description": "若输出文本错误，直接进行更新，若无错误直接复制原始输出文本即可"},
    ]
    
    field_configs = [
        {"name": "id", "title": "记录id", "required": True},
        {"name": "domain", "title": "领域类型", "required": False},
        {"name": "task", "title": "任务类型", "required": False},
        {"name": "lang", "title": "语言类型", "required": False},
        {"name": "prompt", "title": "提示词", "required": True},
        {"name": "input", "title": "输入文本", "required": True},
        {"name": "output", "title": "输出文本", "required": True},
        {"name": "source", "title": "语料来源", "required": False},
    ]
    guidelines = '开始标注把！'

    @property
    def argilla_instance(self,):
        try:
            dataset = rg.FeedbackDataset.from_argilla(self.name)
            return dataset.pull()
        except Exception:
            logger.info(f'not exists feedback {self.name}')
        dataset = rg.FeedbackDataset(
            guidelines=self.guidelines,
            fields=[rg.TextField(**_) for _ in self.field_configs],
            questions=[rg.TextQuestion(**_) for _ in self.question_configs]
        )
        dataset.push_to_argilla(name=self.name)
        return dataset

    def push_records(self):
        dataset = self.argilla_instance
        records = [rg.FeedbackRecord(fields={
            "id": _.id,
            "domain": _.domain,
            "lang": _.lang,
            "task": _.task,
            "prompt": _.prompt,
            "input": _.input,
            "output": _.output,
            "source": _.source,
        }) for _ in self.records.filter(label_status='no_action')]
        dataset.add_records(records)
        dataset.push_to_argilla()

    def sync_argilla(self):
        for record in self.argilla_instance:
            if not record.responses:
                continue
            response = record.responses[0]
            if response.status != 'submitted':
                continue
            

class Records(CoreModel):
    LABEL_STATUS_CHOICES = [
        ('submitted', '已标注'),
        ('no_action', '未标注')
    ]
    domain = models.CharField(verbose_name='领域', max_length=64)
    task = models.CharField(verbose_name='任务类型', max_length=32)
    lang = models.CharField(verbose_name="语言", max_length=16, default='ch')
    prompt = models.TextField(verbose_name="提示词")
    input = models.TextField(verbose_name="输入文本")
    output = models.TextField(verbose_name="输出文本")
    source = models.CharField(verbose_name="来源", max_length=512)
    activate = models.BooleanField(verbose_name='是否有效')
    label_status = models.CharField(verbose_name="标注状态", max_length=16, default='no_action', choices=LABEL_STATUS_CHOICES)
    dataset = models.ForeignKey(to=LabelDatasets, on_delete=models.CASCADE, related_name='records')
