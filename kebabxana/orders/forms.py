from django import forms

from phonenumber_field.formfields import PhoneNumberField

class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    phone_number = PhoneNumberField(region='RU')
    requires_delivery = forms.ChoiceField(choices=[('0', False),('1', True),],)
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[('0', 'False'),('1', 'True'),],)
    comment = forms.CharField(required=False)

