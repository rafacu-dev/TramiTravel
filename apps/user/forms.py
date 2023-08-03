
from django import forms
from django.forms import ModelForm

from apps.user.models import Agency


class AgencyForm(ModelForm):
    class Meta:
        model = Agency

        exclude = ['license','credit','actived','revenue']

        styles = 'p-2.5 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-itravel-500 focus:ring-itravel-500 sm:text-sm mb-6'
        
        widgets = {
            'name': forms.TextInput(attrs={'class':styles}),
            'logo': forms.FileInput(attrs={'class':'hidden'}),
            'address': forms.TextInput(attrs={'class':styles}),
            'email': forms.EmailInput(attrs={'class':styles}),
            'phone': forms.TextInput(attrs={'class':styles}),
            'fax': forms.TextInput(attrs={'class':styles}),
            'fei_ein_number': forms.TextInput(attrs={'class':styles}),
            'seller_travel_number': forms.TextInput(attrs={'class':styles}),

            'contact_name': forms.TextInput(attrs={'class':styles}),
            'contact_email': forms.EmailInput(attrs={'class':styles}),
            'contact_phone': forms.TextInput(attrs={'class':styles}),

            #'revenue': forms.NumberInput(attrs={'class':styles}),
        }

