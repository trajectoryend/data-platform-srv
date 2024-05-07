from rest_framework.routers import SimpleRouter

from workflow.views.workflow import WorkflowTypeView, WorkflowsCustomFieldsView

router = SimpleRouter(False)

# 系统设置相关路由
router.register('workflow-type', WorkflowTypeView, basename='workflow-type')
router.register('workflow-custom-fields', WorkflowsCustomFieldsView, basename='workflow-custom-fields')


urlpatterns = router.get_urls()
