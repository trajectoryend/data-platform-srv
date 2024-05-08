# Register your models here.
from django.contrib import admin

# Register your models here.
from workflow.models import *

admin.site.register(WorkflowType)
admin.site.register(Workflow)
admin.site.register(TicketValidation)
admin.site.register(WorkflowRelation)
admin.site.register(TicketRelation)
admin.site.register(TicketCollection)
admin.site.register(FieldTab)
admin.site.register(FieldRow)
admin.site.register(View)
