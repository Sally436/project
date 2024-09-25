from django.db import models
import uuid
from . utils import create_new_ref_number
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import DatePickerInput
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

# Create your models here.
class FarmerToAggregatorTransaction(models.Model): # 1
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Farmer'}, related_name='farmer_aggregator')
    aggregator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Aggregator', 'profile__address__isnull': False},  related_name='farmer_to_aggregator')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True, help_text='This is an optional field to add a description to the products')
    batch_number = models.CharField(max_length = 1000, blank=True, unique=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    haverst_date = models.DateTimeField()
    accepted = models.BooleanField(default=False, verbose_name='Accepted Status')
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    product_url = models.URLField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Transaction from {self.farmer} to {self.aggregator}"
    
    
    def save(self, *args, **kwargs):
        # Check if the object has an id (i.e., if it has been saved)
        if not self.id:
            # Save the object to get an id
            super().save(*args, **kwargs)
        # Generate the product URL based on the id
        self.product_url = f'http://127.0.0.1:8000/farmer_aggregator/{self.id}/'

        # Generate QR code using the qrcode library
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'{self.product_url}\n\nFarmer: {self.farmer.username}\nAggregator: {self.aggregator.username}\nQuantity: {self.quantity}\nDate: {self.timestamp}\nBatch Number: {self.batch_number}')
        qr.make(fit=True)

        # Create an image from the QR code and save it to BytesIO
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Save the QR code image to the model's ImageField
        self.qr_code.save(f'qr_code_{self.id}.png', ContentFile(buffer.read()), save=False)
        self.total = self.unit_price * self.quantity
        if not self.batch_number:
            self.batch_number = str(uuid.uuid4())
        # Save the object again to update the product_url and qrcode fields
        super().save(*args, **kwargs)


class FarmerToProcessorTransaction(models.Model): # 2
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Farmer'}, related_name='farmer_processor')
    processor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Processor', 'profile__address__isnull': False}, related_name='farmer_to_processor')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True, help_text='This is an optional field to add a description to the products')
    batch_number = models.CharField(max_length = 1000, blank=True, unique=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    haverst_date = models.DateTimeField()
    accepted = models.BooleanField(default=False, verbose_name='Accepted Status')
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    product_url = models.URLField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Transaction from {self.farmer} to {self.processor}"
    
    def save(self, *args, **kwargs):
        # Check if the object has an id (i.e., if it has been saved)
        if not self.id:
            # Save the object to get an id
            super().save(*args, **kwargs)
        # Generate the product URL based on the id
        self.product_url = f'http://127.0.0.1:8000/product/{self.id}/'

        # Generate QR code using the qrcode library
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'{self.product_url}\n\nFarmer: {self.farmer.username}\nProcessor: {self.processor.username}\nQuantity: {self.quantity}\nDate: {self.timestamp}\nBatch Number: {self.batch_number}')
        qr.make(fit=True)

        # Create an image from the QR code and save it to BytesIO
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Save the QR code image to the model's ImageField
        self.qr_code.save(f'qr_code_{self.id}.png', ContentFile(buffer.read()), save=False)
        self.total = self.unit_price * self.quantity
        if not self.batch_number:
            self.batch_number = str(uuid.uuid4())
        # Save the object again to update the product_url and qrcode fields
        super().save(*args, **kwargs)


class AggregatorToProcessorTransaction(models.Model): # 3
    aggregator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Aggregator'}, related_name='aggregator_processor')
    processor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Processor', 'profile__address__isnull': False}, related_name='aggregator_to_processor')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True, help_text='This is an optional field to add a description to the products')
    batch_number = models.CharField(max_length = 1000, blank=True, unique=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    accepted = models.BooleanField(default=False, verbose_name='Accepted Status')
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    product_url = models.URLField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Transaction from {self.aggregator} to {self.processor}"
    
    def save(self, *args, **kwargs):
        # Check if the object has an id (i.e., if it has been saved)
        if not self.id:
            # Save the object to get an id
            super().save(*args, **kwargs)
        # Generate the product URL based on the id
        self.product_url = f'http://127.0.0.1:8000/product/{self.id}/'

        # Generate QR code using the qrcode library
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'{self.product_url}\n\nAggregator: {self.aggregator.username}\nProcessor: {self.processor.username}\nQuantity: {self.quantity}\nDate: {self.timestamp}\nBatch Number: {self.batch_number}')
        qr.make(fit=True)

        # Create an image from the QR code and save it to BytesIO
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Save the QR code image to the model's ImageField
        self.qr_code.save(f'qr_code_{self.id}.png', ContentFile(buffer.read()), save=False)
        self.total = self.unit_price * self.quantity
        if not self.batch_number:
            self.batch_number = str(uuid.uuid4())
        # Save the object again to update the product_url and qrcode fields
        super().save(*args, **kwargs)


class ProcessorToDistributorTransaction(models.Model): # 4
    processor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Processor'}, related_name='processor_distributor')
    distributor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Distributor', 'profile__address__isnull': False}, related_name='processor_to_distributor')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True, help_text='This is an optional field to add a description to the products')
    batch_number = models.CharField(max_length = 1000, blank=True, unique=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    haverst_date = models.DateTimeField(verbose_name='Production Date')
    expiration_date = models.DateTimeField()
    accepted = models.BooleanField(default=False, verbose_name='Accepted Status')
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    product_url = models.URLField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Transaction from {self.processor} to {self.distributor}"
    
    def save(self, *args, **kwargs):
        # Check if the object has an id (i.e., if it has been saved)
        if not self.id:
            # Save the object to get an id
            super().save(*args, **kwargs)
        # Generate the product URL based on the id
        self.product_url = f'http://127.0.0.1:8000/processor_distributor/{self.id}/'

        # Generate QR code using the qrcode library
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'{self.product_url}\n\nProcessor: {self.processor.username}\nDistributor: {self.distributor.username}\nQuantity: {self.quantity}\nDate: {self.timestamp}\nBatch Number: {self.batch_number}')
        qr.make(fit=True)

        # Create an image from the QR code and save it to BytesIO
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Save the QR code image to the model's ImageField
        self.qr_code.save(f'qr_code_{self.id}.png', ContentFile(buffer.read()), save=False)
        self.total = self.unit_price * self.quantity
        if not self.batch_number:
            self.batch_number = str(uuid.uuid4())
        # Save the object again to update the product_url and qrcode fields
        super().save(*args, **kwargs)


class DistributorToRetailerTransaction(models.Model): # 5
    distributor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Distributor'}, related_name='distributor_retailer')
    retailer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Retailer', 'profile__address__isnull': False}, related_name='distributor_to_retailer')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True, help_text='This is an optional field to add a description to the products')
    batch_number = models.CharField(max_length = 1000, blank=True, unique=True, null=True)
    accepted = models.BooleanField(default=False, verbose_name='Accepted Status')
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    product_url = models.URLField(blank=True)
    
    def __str__(self):
        return f"Transaction from {self.distributor} to {self.retailer}"
    
    def save(self, *args, **kwargs):
        # Check if the object has an id (i.e., if it has been saved)
        if not self.id:
            # Save the object to get an id
            super().save(*args, **kwargs)
        # Generate the product URL based on the id
        self.product_url = f'http://127.0.0.1:8000/distributor_retailer/{self.id}/'

        # Generate QR code using the qrcode library
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'{self.product_url}\n\nDistributor: {self.distributor.username}\nRetailer: {self.retailer.username}\nQuantity: {self.quantity}\nDate: {self.timestamp}\nBatch Number: {self.batch_number}')
        qr.make(fit=True)

        # Create an image from the QR code and save it to BytesIO
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Save the QR code image to the model's ImageField
        self.qr_code.save(f'qr_code_{self.id}.png', ContentFile(buffer.read()), save=False)
        if not self.batch_number:
            self.batch_number = str(uuid.uuid4())
        # Save the object again to update the product_url and qrcode fields
        super().save(*args, **kwargs)