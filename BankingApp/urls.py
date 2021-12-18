from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('',include('clientApp.urls')),
    path('admin/', admin.site.urls),
    path('plaidApp/', include('plaidApp.urls')),
]
