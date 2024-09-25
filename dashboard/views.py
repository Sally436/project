from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . models import FarmerToAggregatorTransaction, FarmerToProcessorTransaction, AggregatorToProcessorTransaction, ProcessorToDistributorTransaction, DistributorToRetailerTransaction
from .forms import FarmerToAggregatorTransactionForm, FarmerToAggregatorTransactionConfirmForm, FarmerToProcessorTransactionForm, FarmerToProcessorTransactionFormConfirmForm, AggregatorToProcessorTransactionForm, ProcessorToDistributorTransactionForm, DistributorToRetailerTransactionForm, ProcessorToDistributorTransactionFormConfirmForm, AggregatorToProcessorTransactionFormConfirmForm
from django.core.paginator import Paginator
import folium
from folium.plugins import Fullscreen
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, A1, HALF_LETTER, C7
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm




# Create your views here.
@login_required
def index(request):
    farmer_to_aggregator_pending_transaction_count = FarmerToAggregatorTransaction.objects.filter(aggregator=request.user, accepted=False).count()
    farmer_to_aggregator_accepted_transaction_count = FarmerToAggregatorTransaction.objects.filter(aggregator=request.user, accepted=True).count()
    context = {
        'farmer_to_aggregator_pending_transaction_count':farmer_to_aggregator_pending_transaction_count,
        'farmer_to_aggregator_accepted_transaction_count': farmer_to_aggregator_accepted_transaction_count,
    }
    return render(request, 'dashboard/index.html', context)

def farmer_aggregator(request): 
    if request.method == 'POST':
        form = FarmerToAggregatorTransactionForm(request.POST)
        if form.is_valid():
            farmer_group = form.save(commit=False)
            # Set the user field to the current user
            farmer_group.farmer = request.user
            # Save the FarmerGroup object
            farmer_group.save()
            return redirect('farmer-aggregator')
    else:
        form = FarmerToAggregatorTransactionForm()

    data = FarmerToAggregatorTransaction.objects.all().order_by('-timestamp')
    
    context = {
        'data': data,
        'form': form,
               }
    return render(request, 'dashboard/farmer/farmer_aggregator.html', context)

def farm_product_detail_view(request, pk):
    # items = FarmerGroup.objects.all()
    
    obj = get_object_or_404(FarmerToAggregatorTransaction, id=pk)
    transaction_map = folium.Map(location=[7.9, 1.0], zoom_start=6)
    Fullscreen(position='topright', title='Full Screen', title_cancel='Exit Full Screen').add_to(transaction_map)
    folium.Marker([obj.farmer.profile.latitude, obj.farmer.profile.longitude], tooltip='Farmer', popup=f'{obj.farmer.username}:{obj.farmer.profile.address}', icon=folium.Icon(color='green')).add_to(transaction_map)
    folium.Marker([obj.aggregator.profile.latitude, obj.aggregator.profile.longitude], tooltip='Aggregator', popup=f'{obj.aggregator.username}:{obj.aggregator.profile.address}').add_to(transaction_map)

    transaction_map = transaction_map._repr_html_()
    context = {
        'obj': obj,
        'transaction_map': transaction_map
    }
    return render(request, 'dashboard/farmer/farm_aggregator_detail.html', context)

def generate_pdf(obj):
    # Create a HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="new.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=C7)
    width, height = C7

    # Draw the data on the PDF.
    if obj.qr_code:
        # Get the absolute path of the image file
        image_path = obj.qr_code.path
        p.drawImage(image_path, 60, height - 210, width=200, height=200)

    p.drawString(110, height - 215, f"Scan QR Code")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    return response

def download_data(request, pk):
    obj = get_object_or_404(FarmerToAggregatorTransaction, pk=pk)
    return generate_pdf(obj)


def aggregator_transaction(request):
    data = FarmerToAggregatorTransaction.objects.all()
    
    context = {
        'data': data,
    }
    return render(request, 'dashboard/aggregator/aggregator_transaction.html', context)

def aggregator_completed_all_transactions(request):
    data = FarmerToAggregatorTransaction.objects.all()
    context = {
        'data': data,
    }
    return render(request, 'dashboard/aggregator_completed_all_transactions.html', context)

def aggregator_transaction_confirm(request, pk):
    item = FarmerToAggregatorTransaction.objects.get(id=pk)
    if request.method == 'POST':
        form = FarmerToAggregatorTransactionConfirmForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('aggregator-transaction')
    else:
        form = FarmerToAggregatorTransactionConfirmForm(instance=item)
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'dashboard/aggregator/aggregator_transaction_confirm.html', context)



def farmer_processor(request):
    if request.method == 'POST':
        form = FarmerToProcessorTransactionForm(request.POST)
        if form.is_valid():
            farmer_group = form.save(commit=False)
            # Set the user field to the current user
            farmer_group.farmer = request.user
            # Save the FarmerGroup object
            farmer_group.save()
            return redirect('farmer-processor')
    else:
        form = FarmerToProcessorTransactionForm()

    data = FarmerToProcessorTransaction.objects.all()
    
    context = {
        'data': data,
        'form': form,
               }
    return render(request, 'dashboard/farmer/farmer_processor.html', context)

def farm_processor_detail_view(request, pk):
    # items = FarmerGroup.objects.all()
    obj = get_object_or_404(FarmerToProcessorTransaction, id=pk)
    transaction_map = folium.Map(location=[7.9, 1.0], zoom_start=6)
    Fullscreen(position='topright', title='Full Screen', title_cancel='Exit Full Screen').add_to(transaction_map)

    transaction_map = transaction_map._repr_html_()
    context = {
        'obj': obj,
        'transaction_map': transaction_map
    }
    return render(request, 'dashboard/farmer/farm_processor_detail.html', context)


# Aggregator -> Processor
def aggregator_processor(request):
    if request.method == 'POST':
        form = AggregatorToProcessorTransactionForm(request.POST)
        if form.is_valid():
            aggregator_group = form.save(commit=False)
            # Set the user field to the current user
            aggregator_group.aggregator = request.user
            # Save the FarmerGroup object
            aggregator_group.save()
            return redirect('aggregator-processor')
    else:
        form = AggregatorToProcessorTransactionForm()

    data = AggregatorToProcessorTransaction.objects.all()
    
    context = {
        'data': data,
        'form': form,
               }
    return render(request, 'dashboard/aggregator/aggregator_processor.html', context)

def processor_distributor_detail_view(request, pk):
    # items = FarmerGroup.objects.all()
    obj = get_object_or_404(ProcessorToDistributorTransaction, id=pk)
    transaction_map = folium.Map(location=[7.9, 1.0], zoom_start=6)
    Fullscreen(position='topright', title='Full Screen', title_cancel='Exit Full Screen').add_to(transaction_map)

    transaction_map = transaction_map._repr_html_()
    context = {
        'obj': obj,
        'transaction_map': transaction_map
    }
    return render(request, 'dashboard/processor/processor_distributor_detail.html', context)


# Processor -> Distributor
def processor_distributor(request):
    if request.method == 'POST':
        form = ProcessorToDistributorTransactionForm(request.POST)
        if form.is_valid():
            processor_group = form.save(commit=False)
            # Set the user field to the current user
            processor_group.processor = request.user
            # Save the FarmerGroup object
            processor_group.save()
            return redirect('processor-distributor')
    else:
        form = ProcessorToDistributorTransactionForm()

    data = ProcessorToDistributorTransaction.objects.all()
    
    context = {
        'data': data,
        'form': form,
               }
    return render(request, 'dashboard/processor/processor_distributor.html', context)

def distributor_transaction(request):
    data = ProcessorToDistributorTransaction.objects.all()
    
    context = {
        'data': data,
    }
    return render(request, 'dashboard/distributor/distributor_transaction.html', context)


def distributor_transaction_confirm(request, pk):
    item = ProcessorToDistributorTransaction.objects.get(id=pk)
    if request.method == 'POST':
        form = ProcessorToDistributorTransactionFormConfirmForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('distributor-transaction')
    else:
        form = ProcessorToDistributorTransactionFormConfirmForm(instance=item)
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'dashboard/distributor/distributor_transaction_confirm.html', context)


def farmer_processor_transaction(request):
    data = FarmerToProcessorTransaction.objects.all()
    
    context = {
        'data': data,
    }
    return render(request, 'dashboard/processor/farmer_processor_transaction.html', context)


def farmer_processor_transaction_confirm(request, pk):
    item = FarmerToProcessorTransaction.objects.get(id=pk)
    if request.method == 'POST':
        form = FarmerToProcessorTransactionFormConfirmForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('farmer-processor-transaction')
    else:
        form = FarmerToProcessorTransactionFormConfirmForm(instance=item)
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'dashboard/processor/farmer_processor_transaction_confirm.html', context)



def aggregator_processor_transaction(request):
    data = AggregatorToProcessorTransaction.objects.all()
    
    context = {
        'data': data,
    }
    return render(request, 'dashboard/processor/aggregator_processor_transaction.html', context)


def aggregator_processor_transaction_confirm(request, pk):
    item = AggregatorToProcessorTransaction.objects.get(id=pk)
    if request.method == 'POST':
        form = AggregatorToProcessorTransactionFormConfirmForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('aggregator-processor-transaction')
    else:
        form = AggregatorToProcessorTransactionFormConfirmForm(instance=item)
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'dashboard/processor/aggregator_processor_transaction_confirm.html', context)




# Distributor -> Retailer
def distributor_retailer(request):
    if request.method == 'POST':
        form = DistributorToRetailerTransactionForm(request.POST)
        if form.is_valid():
            distributor_group = form.save(commit=False)
            # Set the user field to the current user
            distributor_group.distributor = request.user
            # Save the FarmerGroup object
            distributor_group.save()
            return redirect('distributor-retailer')
    else:
        form = DistributorToRetailerTransactionForm()

    data = DistributorToRetailerTransaction.objects.all()
    
    context = {
        'data': data,
        'form': form,
               }
    return render(request, 'dashboard/distributor/distributor_retailer.html', context)

def distributor_retailer_detail_view(request, pk):
    # items = FarmerGroup.objects.all()
    obj = get_object_or_404(DistributorToRetailerTransaction, id=pk)
    transaction_map = folium.Map(location=[7.9, 1.0], zoom_start=6)
    Fullscreen(position='topright', title='Full Screen', title_cancel='Exit Full Screen').add_to(transaction_map)
    folium.Marker([obj.distributor.profile.latitude, obj.distributor.profile.longitude], tooltip='Distributor', popup=f'{obj.distributor.username}:{obj.distributor.profile.address}', icon=folium.Icon(color='green')).add_to(transaction_map)
    folium.Marker([obj.retailer.profile.latitude, obj.retailer.profile.longitude], tooltip='Retailer', popup=f'{obj.retailer.username}:{obj.retailer.profile.address}').add_to(transaction_map)

    transaction_map = transaction_map._repr_html_()
    context = {
        'obj': obj,
        'transaction_map': transaction_map
    }
    return render(request, 'dashboard/distributor/distributor_retailer_detail.html', context)

