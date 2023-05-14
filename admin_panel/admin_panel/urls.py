from django.contrib import admin
from django.urls import path
from django_otp.admin import OTPAdminSite
from . import settings


if not settings.DEBUG:
    admin.site.__class__ = OTPAdminSite


from . views import index, payment_get, payment_processing, payment_failed, payment_success


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('payment_get/<str:uuid>', payment_get),
    path('payment_processing/', payment_processing),
    path('payment_success/', payment_success),
    path('payment_failed/', payment_failed)
]
