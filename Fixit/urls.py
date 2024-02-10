from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Users.urls')),
    path('ticket/',include('Ticket.urls')),
    path('api_auth/', include('rest_framework.urls')),
    # path('rest-auth/', include('rest_auth.urls'))
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)