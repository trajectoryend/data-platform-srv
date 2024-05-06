from django.urls import path, include

# 路由配置，当添加APP完成时候，会自动注入路由到总服务
URLPATTERNS = [
    path('api/workflow/', include('workflow.urls')),
]

# 请求白名单，支持正则表达式，可参考settings.py里面的 PERMISSION_WHITE_URL
PERMISSION_WHITE_REURL = []
