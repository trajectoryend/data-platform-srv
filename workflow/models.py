from django.db import models
from django.utils.translation import gettext_lazy as _

from common.core.models import DbAuditModel, DbUuidModel


class WorkflowType(DbAuditModel, DbUuidModel):
    name = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    icon = models.CharField(verbose_name="图标", max_length=256, null=True, blank=True)
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工作流类型"
        verbose_name_plural = "工作流类型"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.name}"


class Workflow(DbAuditModel, DbUuidModel):
    to_workflow_type = models.ForeignKey(
        to='WorkflowType', on_delete=models.SET_NULL, verbose_name="所属工作流类型", null=True, blank=True
    )
    name = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    workflow_id = models.IntegerField(verbose_name="工作流ID")
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工作流"
        verbose_name_plural = "工作流"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.name}"


class TicketValidation(DbAuditModel, DbUuidModel):
    to_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="所属工作流", null=True, blank=True
    )
    unique_together = models.CharField(verbose_name="唯一值校验字段，使用逗号隔开", max_length=256, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工单唯一值校验"
        verbose_name_plural = "工单唯一值校验"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.to_workflow.name}"


class WorkflowRelation(DbAuditModel, DbUuidModel):
    class RelationChoices(models.IntegerChoices):
        ONE2ONE = 0, _("1 - 1")
        ONE2MANY = 1, _("1 - N")
        MANY2MANY = 2, _("N - N")

    src_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="源工作流", null=True, blank=True
    )
    dst_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="目工作流", null=True, blank=True
    )
    dst_ticket_search_params = models.TextField(verbose_name="目标工单搜索参数", null=True, blank=True)
    src_ticket_search_params = models.TextField(verbose_name="源工单搜索参数", null=True, blank=True)
    src_to_dst_relation = models.SmallIntegerField(
        choices=RelationChoices, default=RelationChoices.ONE2MANY, verbose_name="源-目标约束"
    )
    src_to_dst_description = models.CharField(verbose_name="源-目标描述", max_length=256, null=True, blank=True)
    dst_to_src_description = models.CharField(verbose_name="目标-源描述", max_length=256, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工作流关系"
        verbose_name_plural = "工作流关系"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.src_workflow.name} - {self.dst_workflow.name}"


class TicketRelation(DbAuditModel, DbUuidModel):

    to_workflow_relation = models.ForeignKey(
        to='WorkflowRelation', on_delete=models.SET_NULL, verbose_name="所属工作流关系", null=True, blank=True
    )
    src_ticket_id = models.IntegerField(verbose_name="源工单ID")
    dst_ticket_id = models.IntegerField(verbose_name="目标工单ID")
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "工单关系"
        verbose_name_plural = "工单关系"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.to_workflow_relation.src_workflow.name}-（{self.src_ticket_id}）至 {self.to_workflow_relation.dst_workflow.name}-（{self.dst_ticket_id}）"


class TicketCollection(DbAuditModel, DbUuidModel):
    to_user_info = models.ForeignKey(
        to='system.UserInfo', on_delete=models.SET_NULL, verbose_name="所属用户", null=True, blank=True
    )
    ticket_id = models.IntegerField(verbose_name="工单ID")
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "用户收藏的工单"
        verbose_name_plural = "用户收藏的工单"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.to_user_info.nickname} - {self.ticket_id}"


class FieldTab(DbAuditModel, DbUuidModel):
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
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.name}"


class FieldRow(DbAuditModel, DbUuidModel):
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
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.name}"


class WorkFlowView(DbAuditModel, DbUuidModel):

    class ViewChoices(models.IntegerChoices):
        SYSTEM = 0, _("系统视图")
        PERSON = 2, _("用户视图")

    class SearchModeChoices(models.IntegerChoices):
        BASIC = 0, _("基础搜索")
        ADVANCED = 1, _("高级搜索")

    class SearchModeChoices(models.IntegerChoices):
        BASIC = 0, _("基础搜索")
        ADVANCED = 1, _("高级搜索")

    class OrderTypeChoices(models.TextChoices):
        ASC = 'ASC', _("升序")
        DESC = 'DESC', _("降序")

    to_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="所属工作流", null=True, blank=True
    )
    view_type = models.SmallIntegerField(choices=ViewChoices, default=ViewChoices.PERSON, verbose_name="视图类型")
    search_mode = models.SmallIntegerField(
        choices=SearchModeChoices, default=SearchModeChoices.BASIC, verbose_name="搜索类型"
    )
    name = models.CharField(verbose_name="名称", max_length=256)
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    order_field = models.CharField(verbose_name="排序字段", max_length=256, null=True, blank=True)
    order_type = models.CharField(
        choices=OrderTypeChoices, default=OrderTypeChoices.DESC, verbose_name="排序方式", max_length=4
    )
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "视图"
        verbose_name_plural = "视图"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.name}"
