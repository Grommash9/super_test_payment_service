from django.contrib import admin
from .models import PaymentStatus, Payment, PaymentCallbackSendLog


@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'code')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'uuid', 'amount', 'currency', 'callback_url', 'status')


@admin.register(PaymentCallbackSendLog)
class PaymentCallbackSendLogAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'payment_associated', 'created_date', 'sent_date', 'send_status', 'sent_result')




