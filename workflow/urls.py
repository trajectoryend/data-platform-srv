from rest_framework.routers import SimpleRouter

from workflow.views.workflow import WorkflowTypeView

router = SimpleRouter(False)

# 系统设置相关路由
router.register('workflow-type', WorkflowTypeView, basename='workflow-type')

urlpatterns = router.get_urls()
