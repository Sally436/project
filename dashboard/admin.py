from django.contrib import admin
from .models import  FarmerToAggregatorTransaction, FarmerToProcessorTransaction, AggregatorToProcessorTransaction, ProcessorToDistributorTransaction, DistributorToRetailerTransaction
# Register your models here.

class FarmerToAggregatorTransactionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'aggregator', 'qr_code', 'batch_number', 'timestamp']

admin.site.register(FarmerToAggregatorTransaction, FarmerToAggregatorTransactionAdmin)

class AggregatorToProcessorTransactionAdmin(admin.ModelAdmin):
    list_display = ['aggregator', 'processor', 'qr_code', 'batch_number', 'timestamp']

admin.site.register(AggregatorToProcessorTransaction, AggregatorToProcessorTransactionAdmin)


class FarmerToProcessorTransactionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'processor', 'qr_code', 'batch_number', 'timestamp']

admin.site.register(FarmerToProcessorTransaction, FarmerToProcessorTransactionAdmin)

class ProcessorToDistributorTransactionAdmin(admin.ModelAdmin):
    list_display = ['processor', 'distributor', 'qr_code', 'batch_number', 'timestamp']

admin.site.register(ProcessorToDistributorTransaction, ProcessorToDistributorTransactionAdmin)

class DistributorToRetailerTransactionAdmin(admin.ModelAdmin):
    list_display = ['distributor', 'retailer', 'qr_code', 'batch_number', 'timestamp']

admin.site.register(DistributorToRetailerTransaction, DistributorToRetailerTransactionAdmin)