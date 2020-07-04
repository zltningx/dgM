"""dragonM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from apps.backend import views as backend_views
from apps.vulmannager import views as vul_views


router_v1 = DefaultRouter()

router_v1.register('penetration_ticket', vul_views.PenetrationTestViewSet,
                   base_name='penetration_ticket')
router_v1.register('penetration_ticket_result',
                   vul_views.PenetrationTestTicketResultViewSet,
                   base_name='penetration_ticket_result')
router_v1.register('penetration_ticket_sub_workflow',
                   vul_views.PenetrationTestTicketSubWorkflowViewSet,
                   base_name='penetration_ticket_sub_workflow')
router_v1.register('vulnerability', vul_views.VulnerabilityViewSet,
                   base_name='vulnerability')
router_v1.register('vul_workflow', vul_views.VulWorkflowViewSet,
                   base_name='vul_workflow')
router_v1.register('vul_sub_workflow', vul_views.VulSubWorkflowViewSet,
                   base_name='vul_sub_workflow')
router_v1.register('user', backend_views.AuthManager,
                   base_name='auth_manger')
router_v1.register('read_user', backend_views.UserReadOnlyViewSet,
                   base_name='read_user')
router_v1.register('penetration_ticket_manager', vul_views.PenetrationTestTicketManager,
                   base_name='penetration_ticket_manager')
router_v1.register('asset', vul_views.AssetViewSet,
                   base_name='asset')
router_v1.register('port', vul_views.PortViewSet,
                   base_name='port')
router_v1.register('smtp', backend_views.SMTPConfigViewSet,
                   base_name='config')
router_v1.register('notify', backend_views.Notify,
                   base_name='notify')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router_v1.urls)),
    # auth
    path(r'api/v1/', include([
        path(r'token/obtain/', backend_views.ObtainJWT.as_view(), name='token-get'),
    ])),
]
