from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('dashboard.urls')),
    path('ticket/',include('tickets.urls')),
    path('account/',include('users.urls')),
]
