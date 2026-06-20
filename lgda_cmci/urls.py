from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('core/', include('core.urls')),
    path('disciples/', include('disciples.urls')),
    path('evangelisation/', include('evangelisation.urls')),
    path('rapports/', include('rapports.urls')),
    path('', dashboard, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'LGDA-CMCI Administration'
admin.site.site_title = 'LGDA-CMCI'
admin.site.index_title = 'Gestion du Disciple'
