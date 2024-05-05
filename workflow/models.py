from django.db import models
from django.utils.translation import gettext_lazy as _

from common.core.models import DbAuditModel, DbUuidModel


class WorkflowType(DbAuditModel, DbUuidModel):
    name = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    icon = models.CharField(verbose_name="图标", max_length=256, null=True, blank=True)
    order_id = models.IntegerField(verbose_name="排序", default=9999)

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
    icon = models.CharField(verbose_name="图标", max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "工作流"
        verbose_name_plural = "工作流"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.name}"


class FieldTab(DbAuditModel, DbUuidModel):
    to_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="所属工作流", null=True, blank=True
    )
    name = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    icon = models.CharField(verbose_name="图标", max_length=256, null=True, blank=True)

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

    class Meta:
        verbose_name = "字段Row"
        verbose_name_plural = "字段Row"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.name}"


class FieldCol(DbAuditModel, DbUuidModel):
    to_field_tab = models.ForeignKey(
        to='FieldRow', on_delete=models.SET_NULL, verbose_name="所属字段Row", null=True, blank=True
    )
    name = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    order_id = models.IntegerField(verbose_name="排序", default=9999)
    icon = models.CharField(verbose_name="图标", max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "字段Col"
        verbose_name_plural = "字段Col"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.name}"


class WorkFlowView(DbAuditModel, DbUuidModel):

    class ViewChoices(models.IntegerChoices):
        SYSTEM = 0, _("系统视图")
        PROJECT = 1, _("项目视图")
        PERSON = 2, _("用户视图")

    class SearchModeChoices(models.IntegerChoices):
        NO = 0, _("系统视图")
        ADV = 1, _("项目视图")

    to_workflow = models.ForeignKey(
        to='Workflow', on_delete=models.SET_NULL, verbose_name="所属工作流", null=True, blank=True
    )
    view_type = models.SmallIntegerField(choices=ViewChoices, default=ViewChoices.PERSON, verbose_name="视图类型")
    search_mode = models.SmallIntegerField(choices=ViewChoices, default=ViewChoices.PERSON, verbose_name="视图类型")
    name = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    order_id = models.IntegerField(verbose_name="工作流ID", default=9999)
    order_field = models.CharField(verbose_name="排序", max_length=256, null=True, blank=True)
    order_type = models.CharField(verbose_name="名称", max_length=256, null=True, blank=True)
    icon = models.CharField(verbose_name="图标", max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "字段Col"
        verbose_name_plural = "字段Col"
        ordering = ("-created_time",)

    def __str__(self):
        return f"{self.name}"
