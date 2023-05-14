import datetime

from django.shortcuts import render
from .models import Payment, PaymentCallbackSendLog, PaymentStatus
from .forms import PaymentForm
from django.shortcuts import render
from django.http import HttpResponseRedirect


def create_callback(payment: Payment):
    if payment.callback_url is None:
        return

    new_callback_obj = PaymentCallbackSendLog(created_date=datetime.datetime.now(), send_status=None, sent_result=None,
                                              payment_associated_id=payment.pk)
    new_callback_obj.save()


def index(request):
    return render(request, 'index.html', context={'user_data': 'data'})


def payment_get(request, uuid):
    form = PaymentForm()
    payment_info: Payment = Payment.objects.select_related('status').get(uuid=uuid)

    if payment_info.status.code == 'failed':
        return render(request, 'payment_failed.html')
    if payment_info.status.code == 'success':
        return render(request, 'payment_success.html')

    return render(request, 'payment.html', {"amount": payment_info.amount,
                                            "currency": payment_info.currency,
                                            "payment_uuid": payment_info.uuid,
                                            'form': form,
                                            'uuid': payment_info.uuid})


def payment_processing(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            expiration_date = form.cleaned_data['expiration_date']
            cvv_code = form.cleaned_data['cvv_code']
            uuid = request.POST.get('uuid')
            print('uuid', uuid)
            payment_info: Payment = Payment.objects.select_related('status').get(uuid=uuid)
            if payment_info.status.code != 'created':
                HttpResponseRedirect('/')

            if card_number.startswith('4441'):
                success_status = PaymentStatus.objects.get(code='success')
                payment_info.status = success_status
                payment_info.save()
                create_callback(payment_info)
                return HttpResponseRedirect('/payment_success')
            else:
                failed_status = PaymentStatus.objects.get(code='failed')
                payment_info.status = failed_status
                payment_info.save()
                create_callback(payment_info)
                return HttpResponseRedirect('/payment_failed')

    return HttpResponseRedirect('/')


def payment_success(request):
    return render(request, 'payment_success.html')


def payment_failed(request):
    return render(request, 'payment_failed.html')
