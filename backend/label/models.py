import logging
import datetime
import argilla as rg
from django.conf import settings
from django.db import models
from dvadmin.utils.models import CoreModel

logger = logging.getLogger(__name__)

AG_QUESTION_CONFIGS = [
    {"name": "new-prompt", "title": "纠正提示词", "description": "若提示词错误，直接进行更新，若无错误直接复制原始提示词即可", "use_markdown": True},
    {"name": "new-input", "title": "纠正输入文本", "description": "若输入文本错误，直接进行更新，若无错误直接复制原始输入文本即可", "use_markdown": True},
    {"name": "new-output", "title": "纠正输出文本", "description": "若输出文本错误，直接进行更新，若无错误直接复制原始输出文本即可", "use_markdown": True},
]

AG_FIELD_CONFIGS = [
    {"name": "id", "title": "记录id", "required": True},
    {"name": "domain", "title": "领域类型", "required": False},
    {"name": "power", "title": "权能", "required": False},
    {"name": "lang", "title": "语言类型", "required": False},
    {"name": "prompt", "title": "提示词", "required": True},
    {"name": "input", "title": "输入文本", "required": True},
    {"name": "output", "title": "输出文本", "required": True},
    {"name": "source", "title": "语料来源", "required": False},
]
try:
    rg.init(api_url=settings.ARGILLA_API_URL, api_key=settings.ARGILLA_API_KEY)
except Exception:
    pass


class Tasks(CoreModel):
    name = models.CharField(verbose_name="标注任务名称", max_length=128, null=False, unique=True)
    # status is SerializerField
    submitted_count = models.IntegerField(verbose_name="标注完成个数", default=0)
    sample_sum = models.IntegerField(verbose_name="样本总和", default=0)

    question_configs = AG_QUESTION_CONFIGS
    field_configs = AG_FIELD_CONFIGS
    guidelines = '开始标注把！'

    def delete_ag(self):
        rg.active_client().client.delete(f'api/v1/datasets/{self.argilla_instance.id}')
        rg.delete(name=self.name)


    def init_ag(self):
        dataset = rg.FeedbackDataset(
            guidelines=self.guidelines,
            fields=[rg.TextField(**_) for _ in self.field_configs],
            questions=[rg.TextQuestion(**_) for _ in self.question_configs]
        )
        return dataset

    @property
    def argilla_instance(self, init_when_not_exists=True):
        try:
            dataset = rg.FeedbackDataset.from_argilla(self.name)
            return dataset
        except Exception:
            logger.info(f'not exists feedback {self.name}')
        if init_when_not_exists:
            return self.init_ag()

    def push_records(self):
        dataset = self.argilla_instance
        records = [rg.FeedbackRecord(fields={
            "id": _.id,
            "domain": _.domain,
            "lang": _.lang,
            "power": _.power,
            "prompt": _.prompt,
            "input": _.input,
            "output": _.output,
            "source": _.source,
        }) for _ in self.samples.filter(label_status='no_action')]
        dataset.add_records(records)
        dataset.push_to_argilla(name=self.name)

    class Meta:
        db_table = "label_datasets"
        verbose_name = '标注数据集'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Samples(CoreModel):
    LABEL_STATUS_CHOICES = [
        ('submitted', '已标注'),
        ('no_action', '未标注')
    ]
    domain = models.CharField(verbose_name='领域', max_length=64)
    power = models.CharField(verbose_name='权能', max_length=32)
    lang = models.CharField(verbose_name="语言", max_length=16, default='ch')
    prompt = models.TextField(verbose_name="提示词")
    input = models.TextField(verbose_name="输入文本")
    output = models.TextField(verbose_name="输出文本")
    source = models.CharField(verbose_name="来源", max_length=512)
    new_prompt = models.TextField(verbose_name="提示词", default="")
    new_input = models.TextField(verbose_name="输入文本", default="")
    new_output = models.TextField(verbose_name="输出文本", default="")
    label_status = models.CharField(verbose_name="标注状态", max_length=16, default='no_action', choices=LABEL_STATUS_CHOICES)
    task = models.ForeignKey(to=Tasks, on_delete=models.CASCADE, related_name='samples')

    class Meta:
        db_table = "samples"
        verbose_name = '标注样本'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class LabelResults(CoreModel):
    sample_id = models.CharField(verbose_name='样例id', max_length=64)
    domain = models.CharField(verbose_name='领域', max_length=64)
    power = models.CharField(verbose_name='权能', max_length=32)
    lang = models.CharField(verbose_name="语言", max_length=16, default='ch')
    prompt = models.TextField(verbose_name="提示词")
    input = models.TextField(verbose_name="输入文本")
    output = models.TextField(verbose_name="输出文本")
    source = models.CharField(verbose_name="来源", max_length=512)
    new_prompt = models.TextField(verbose_name="提示词", default="")
    new_input = models.TextField(verbose_name="输入文本", default="")
    new_output = models.TextField(verbose_name="输出文本", default="")
    dataset = models.ForeignKey(to='Dataset', on_delete=models.CASCADE, related_name='label_results')

    class Meta:
        db_table = "label_results"
        verbose_name = '标注结果'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Dataset(CoreModel):
    name = models.CharField(verbose_name="数据集名称", max_length=64)

    @classmethod
    def _copy_from_task(cls, task):
        dataset = cls(name=f'{datetime.datetime.now()}-{task.name}')
        dataset.save()
        for sample in task.samples.all():
            LabelResults.objects.create(
                sample_id=sample.id, domain=sample.domain, power=sample.power, lang=sample.lang,
                prompt=sample.prompt, input=sample.input, output=sample.output,
                source=sample.source, new_prompt=sample.new_prompt, new_input=sample.new_input,
                new_output=sample.new_output, dataset=dataset
            )

    class Meta:
        db_table = "dataset"
        verbose_name = '数据集'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

