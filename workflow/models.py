from django.db import models
from django.utils.translation import gettext_lazy as _

from common.core.models import DbAuditModel, DbUuidModel


class WorkflowType(DbUuidModel):
    name = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工作流类型"
        verbose_name_plural = "工作流类型"
        ordering = ("order_id",)

    def __str__(self):
        return f"{self.name}"


class Workflow(DbAuditModel, DbUuidModel):
    to_workflow_type = models.ForeignKey(
        to='WorkflowType', on_delete=models.SET_NULL, verbose_name="所属工作流类型", null=True
    )
    name = models.CharField(verbose_name="名称", max_length=256)
    workflow_id = models.IntegerField(verbose_name="工作流ID")
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工作流"
        verbose_name_plural = "工作流"
        ordering = ("order_id",)

    def __str__(self):
        return f"{self.name}"


class TicketValidation(DbUuidModel):
    to_workflow = models.ForeignKey(to='Workflow', on_delete=models.SET_NULL, verbose_name="所属工作流", null=True)
    unique_together = models.CharField(verbose_name="唯一值校验字段，使用逗号隔开", max_length=256)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工单唯一值校验"
        verbose_name_plural = "工单唯一值校验"

    def __str__(self):
        return f"{self.to_workflow.name}"


class WorkflowRelation(DbAuditModel, DbUuidModel):
    class RelationChoices(models.TextChoices):
        ONE2ONE = 'One2One', _("1 - 1")
        ONE2MANY = 'One2Many', _("1 - N")
        MANY2MANY = 'Many2Many', _("N - N")

    src_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="源工作流", related_name="src_workflow", null=True
    )
    dst_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="目工作流", related_name="dst_workflow", null=True
    )
    dst_ticket_search_params = models.TextField(verbose_name="目标工单搜索参数", null=True, blank=True, default=None)
    src_ticket_search_params = models.TextField(verbose_name="源工单搜索参数", null=True, blank=True, default=None)
    src_to_dst_relation = models.CharField(
        choices=RelationChoices, default=RelationChoices.ONE2ONE, verbose_name="源-目标约束", max_length=9
    )
    src_to_dst_description = models.CharField(
        verbose_name="源-目标描述", max_length=256, null=True, blank=True, default=None
    )
    dst_to_src_description = models.CharField(
        verbose_name="目标-源描述", max_length=256, null=True, blank=True, default=None
    )
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工作流关系"
        verbose_name_plural = "工作流关系"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.src_workflow.name} - {self.dst_workflow.name}"


class TicketRelation(DbAuditModel, DbUuidModel):

    to_workflow_relation = models.ForeignKey(
        to='WorkflowRelation', on_delete=models.SET_NULL, verbose_name="所属工作流关系", null=True
    )
    src_ticket_id = models.IntegerField(verbose_name="源工单ID")
    dst_ticket_id = models.IntegerField(verbose_name="目标工单ID")
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工单关系"
        verbose_name_plural = "工单关系"
        ordering = ("-created_time",)

    def __str__(self):
        return "{}-({}) 至 {}-({})".format(
            self.to_workflow_relation.src_workflow.name,
            str(self.src_ticket_id),
            self.to_workflow_relation.dst_workflow.name,
            str(self.dst_ticket_id)
        )


class TicketCollection(DbAuditModel, DbUuidModel):
    ticket_id = models.IntegerField(verbose_name="工单ID")
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "用户收藏的工单"
        verbose_name_plural = "用户收藏的工单"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.creator.nickname} - {self.ticket_id}"


class FieldTab(DbUuidModel):
    to_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="所属工作流", null=True, blank=True
    )
    name = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    icon = models.CharField(verbose_name="图标", max_length=256, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "TAB签"
        verbose_name_plural = "TAB签"
        ordering = ("order_id",)

    def __str__(self):
        return f"{self.name}"


class FieldRow(DbUuidModel):
    to_field_tab = models.ForeignKey(
        to='FieldTab', on_delete=models.SET_NULL, verbose_name="所属TAB签", null=True, blank=True
    )
    name = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    icon = models.CharField(verbose_name="图标", max_length=256, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "字段Row"
        verbose_name_plural = "字段Row"
        ordering = ("order_id",)

    def __str__(self):
        return f"{self.name}"


class View(DbAuditModel, DbUuidModel):

    class ViewChoices(models.TextChoices):
        SYSTEM = 'SYSTEM', _("系统视图")
        PERSON = 'PERSON', _("用户视图")

    class SearchModeChoices(models.TextChoices):
        BASIC = 'BASIC', _("基础搜索")
        ADVANCED = 'ADVANCED', _("高级搜索")

    class OrderTypeChoices(models.TextChoices):
        ASC = 'ASC', _("升序")
        DESC = 'DESC', _("降序")

    to_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="所属工作流", null=True, blank=True, default=None
    )
    view_type = models.CharField(
        choices=ViewChoices, default=ViewChoices.PERSON, verbose_name="视图类型", max_length=6
    )
    search_mode = models.CharField(
        choices=SearchModeChoices, default=SearchModeChoices.BASIC, verbose_name="搜索类型", max_length=8
    )
    search_params = models.TextField(verbose_name='搜索条件', null=True, blank=True, default=None)
    table_column = models.TextField(verbose_name='表头字段', null=True, blank=True, default=None)
    name = models.CharField(verbose_name="名称", max_length=256)
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    order_field = models.CharField(verbose_name="排序字段", max_length=256, null=True, blank=True, default=None)
    order_type = models.CharField(
        choices=OrderTypeChoices, default=OrderTypeChoices.DESC, verbose_name="排序方式", max_length=4
    )
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "视图"
        verbose_name_plural = "视图"
        ordering = ("order_id",)

    def __str__(self):
        return f"{self.name}"
