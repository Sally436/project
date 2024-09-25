from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard-index'),
    path('farmer_aggregator/', views.farmer_aggregator, name='farmer-aggregator'),
    path('farmer_aggregator/<int:pk>/', views.farm_product_detail_view, name='farm-product-detail'),
    path('farmer_processor/<int:pk>/', views.farm_processor_detail_view, name='farmer-processor-detail'),
    path('aggregator_transaction/', views.aggregator_transaction, name='aggregator-transaction'),
    path('farmer_processor_transaction/', views.farmer_processor_transaction, name='farmer-processor-transaction'),
    path('farmer_processor_transaction_confirm/<int:pk>/', views.farmer_processor_transaction_confirm, name='farmer-processor-transaction-confirm'),
    path('aggregator_processor_transaction/', views.aggregator_processor_transaction, name='aggregator-processor-transaction'),
    path('aggregator_processor_transaction_confirm/<int:pk>/', views.aggregator_processor_transaction_confirm, name='aggregator-processor-transaction-confirm'),
    
    path('aggregator_completed_all_transactions/', views.aggregator_completed_all_transactions, name='aggregator-completed-all-transactions'),
    path('aggregator_transaction_confirm/<int:pk>/', views.aggregator_transaction_confirm, name='aggregator-transaction-confirm'),
    path('distributor_transaction_confirm/<int:pk>/', views.distributor_transaction_confirm, name='distributor-transaction-confirm'),
    path('distributor_transaction/', views.distributor_transaction, name='distributor-transaction'),

    path('farmer_processor/', views.farmer_processor, name='farmer-processor'),
    path('aggregator_processor/', views.aggregator_processor, name='aggregator-processor'),
    path('processor_distributor/', views.processor_distributor, name='processor-distributor'),
    path('distributor_retailer/', views.distributor_retailer, name='distributor-retailer'),
    path('distributor_retailer/<int:pk>/', views.distributor_retailer_detail_view, name='distributor-retailer-detail'),
    path('processor_distributor/<int:pk>/', views.processor_distributor_detail_view, name='processor-distributor-detail'),

    path('download/<int:pk>/', views.download_data, name='download_data'),

]