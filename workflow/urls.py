from rest_framework.routers import SimpleRouter

from workflow.views.workflow import WorkflowTypeView, WorkflowView, WorkflowCustomFieldView, WorkflowInitStateView, \
    ViewView
from workflow.views.ticket import SearchTicketView, TicketView, TicketTransitionView, TicketFlowlogView

router = SimpleRouter(False)

# workflow相关路由
router.register('workflow-type', WorkflowTypeView, basename='workflow-type')
router.register('workflow', WorkflowView, basename='workflow')
router.register('view', ViewView, basename='view')


router.register('workflow-custom-field', WorkflowCustomFieldView, basename='workflow-custom-field')
router.register('workflow-init-state', WorkflowInitStateView, basename='workflow-init-state')

# 工单相关相关路由
router.register('search-ticket', SearchTicketView, basename='search-ticket')
router.register('ticket', TicketView, basename='ticket')
router.register('ticket-transition', TicketTransitionView, basename='ticket-transition')
router.register('ticket-flowlog', TicketFlowlogView, basename='ticket-flowlog')

urlpatterns = router.get_urls()
