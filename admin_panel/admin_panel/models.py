from django.db import models


class PaymentStatus(models.Model):
    record_id = models.AutoField(unique=True, null=False, primary_key=True)
    code = models.CharField(max_length=20, unique=True)


class Payment(models.Model):
    record_id = models.AutoField(unique=True, null=False, primary_key=True)
    uuid = models.CharField(max_length=200, unique=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=20)
    callback_url = models.CharField(max_length=200, null=True, blank=True)
    status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)


class PaymentCallbackSendLog(models.Model):
    record_id = models.AutoField(unique=True, null=False, primary_key=True)
    payment_associated = models.ForeignKey(Payment, on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    sent_date = models.DateTimeField(null=True, blank=True)
    send_status = models.CharField(max_length=10, blank=True, null=True)
    sent_result = models.CharField(max_length=2000, blank=True, null=True)


