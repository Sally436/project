from django import forms
from django.contrib.auth.models import User, Group
from django.forms import TextInput
from .models import FarmerToAggregatorTransaction, FarmerToProcessorTransaction, AggregatorToProcessorTransaction, ProcessorToDistributorTransaction, DistributorToRetailerTransaction

class FarmerToAggregatorTransactionForm(forms.ModelForm):
    class Meta:
        model = FarmerToAggregatorTransaction
        fields = ['aggregator', 'quantity', 'unit_price', 'haverst_date', 'description']
        widgets = {
            'haverst_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FarmerToAggregatorTransactionConfirmForm(forms.ModelForm):
    class Meta:
        model = FarmerToAggregatorTransaction
        fields = ['accepted']
        widgets = {
            'aggregator': TextInput(attrs={'disabled': 'disabled'}),
            'quantity': TextInput(attrs={'disabled': 'disabled'}),
        }

class FarmerToProcessorTransactionForm(forms.ModelForm):
    class Meta:
        model = FarmerToProcessorTransaction
        fields = ['processor', 'quantity', 'unit_price', 'haverst_date', 'description']
        widgets = {
            'haverst_date': forms.DateInput(attrs={'type': 'date'}),
        }
        

class FarmerToProcessorTransactionFormConfirmForm(forms.ModelForm):
    class Meta:
        model = FarmerToProcessorTransaction
        fields = ['accepted']
        widgets = {
            'processor': TextInput(attrs={'disabled': 'disabled'}),
            'quantity': TextInput(attrs={'disabled': 'disabled'}),
        }

# Aggregator -> Processor

class AggregatorToProcessorTransactionForm(forms.ModelForm):
    class Meta:
        model = AggregatorToProcessorTransaction
        fields = ['processor', 'quantity', 'unit_price', 'description']
        

# Processor -> Distributor
class ProcessorToDistributorTransactionForm(forms.ModelForm):
    class Meta:
        model = ProcessorToDistributorTransaction
        fields = ['distributor', 'quantity', 'unit_price', 'description', 'haverst_date', 'expiration_date']
        widgets = {
            'haverst_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ProcessorToDistributorTransactionFormConfirmForm(forms.ModelForm):
    class Meta:
        model = ProcessorToDistributorTransaction
        fields = ['accepted']
        widgets = {
            'processor': TextInput(attrs={'disabled': 'disabled'}),
            'quantity': TextInput(attrs={'disabled': 'disabled'}),
        }

class AggregatorToProcessorTransactionFormConfirmForm(forms.ModelForm):
    class Meta:
        model = AggregatorToProcessorTransaction
        fields = ['accepted']
        widgets = {
            'processor': TextInput(attrs={'disabled': 'disabled'}),
            'quantity': TextInput(attrs={'disabled': 'disabled'}),
        }

# Distributor -> Retailer
class DistributorToRetailerTransactionForm(forms.ModelForm):
    class Meta:
        model = DistributorToRetailerTransaction
        fields = ['retailer', 'quantity', 'description']
        
        