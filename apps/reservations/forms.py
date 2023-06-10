from django import forms
from django.forms import ModelForm

from apps.reservations.models import Flight

class FlightForm(ModelForm):
    class Meta:
        model = Flight

        #fields = '__all__'
        exclude = ['date','departure','arrival','ability','priceAdult','revenueAdult','priceChildren','revenueChildren','priceInfant','revenueInfant','class_type']

        styles = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-itravel-500 focus:ring-itravel-500 sm:text-sm mb-6'
        
        widgets = {
            'begin': forms.Select(attrs={'class': styles}),
            'to': forms.Select(attrs={'class': styles}),
            'gate': forms.TextInput(attrs={'class': styles}),
            'charter': forms.Select(attrs={'class': styles}),
            'aircraft': forms.Select(attrs={'class': styles}),
            'number': forms.TextInput(attrs={'class': styles}),
            'checkinMoment': forms.NumberInput(attrs={'class': styles}),
            'departure': forms.TimeInput(attrs={'class': styles}),
            'arrival': forms.TimeInput(attrs={'class': styles}),
            'agencyCommission': forms.NumberInput(attrs={'class': styles}),
            #'date': forms.DateInput(attrs={'class': styles}),
            #'ability': forms.NumberInput(attrs={'class': styles}),
            #'priceAdult': forms.NumberInput(attrs={'class': styles}),
            #'revenueAdult': forms.NumberInput(attrs={'class': styles}),
            #'priceChildren': forms.NumberInput(attrs={'class': styles}),
            #'revenueChildren': forms.NumberInput(attrs={'class': styles}),
            #'priceInfant': forms.NumberInput(attrs={'class': styles}),
            #'revenueInfant': forms.NumberInput(attrs={'class': styles}),
            #'baggagePolicy': forms.Select(attrs={'class': styles}),
            'actived': forms.CheckboxInput(attrs={'class': 'hidden'}),
        }


        
class EditFlightForm(ModelForm):
    class Meta:
        model = Flight

        #fields = '__all__'
        exclude = ['date','departure','arrival','actived']

        styles = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-itravel-500 focus:ring-itravel-500 sm:text-sm mb-6'
        
        widgets = {
            'begin': forms.Select(attrs={'class': styles}),
            'to': forms.Select(attrs={'class': styles}),
            'gate': forms.TextInput(attrs={'class': styles}),
            'charter': forms.Select(attrs={'class': styles}),
            'aircraft': forms.Select(attrs={'class': styles}),
            'number': forms.TextInput(attrs={'class': styles}),
            'checkinMoment': forms.NumberInput(attrs={'class': styles}),
            #'departure': forms.TimeInput(attrs={'class': styles}),
            #'arrival': forms.TimeInput(attrs={'class': styles}),
            'agencyCommission': forms.NumberInput(attrs={'class': styles}),
            #'date': forms.DateInput(attrs={'class': styles}),
            'ability': forms.NumberInput(attrs={'class': styles}),
            'priceAdult': forms.NumberInput(attrs={'class': styles}),
            'revenueAdult': forms.NumberInput(attrs={'class': styles}),
            'priceChildren': forms.NumberInput(attrs={'class': styles}),
            'revenueChildren': forms.NumberInput(attrs={'class': styles}),
            'priceInfant': forms.NumberInput(attrs={'class': styles}),
            'revenueInfant': forms.NumberInput(attrs={'class': styles}),
            'baggagePolicy': forms.Select(attrs={'class': styles}),
            'class_type': forms.Select(attrs={'class': styles}),
            #'actived': forms.CheckboxInput(attrs={'class': ''}),
        }