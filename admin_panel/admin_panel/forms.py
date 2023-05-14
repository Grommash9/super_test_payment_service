from django import forms


class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16)
    expiration_date = forms.CharField(label='Expiration Date', max_length=7)
    cvv_code = forms.CharField(label='CVV Code', max_length=3)
