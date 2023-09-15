from django import forms
from PIL import Image
from io import BytesIO
import os.path
import imghdr
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.images import ImageFile
from django.core.files import File

from .models import Item

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image','phone_number','is_sold')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'phone_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
        }

    

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            return None

        # Open the image using Pillow
        img = Image.open(image)

        # Check the image size
        max_size = 100 * 1024  # 100 kB
        if image.size <= max_size:
            return image

        # Convert the image to RGB mode if it's in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        elif img.mode == 'P':
            img = img.convert('RGB')

        # Resize the image
        width, height = img.size
        if width > 1000 or height > 1000:
            if width > height:
                new_width = 1000
                new_height = int((height / width) * 1000)
            else:
                new_height = 1000
                new_width = int((width / height) * 1000)
            img = img.resize((new_width, new_height))

        # Compress the image and save it to a BytesIO object
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=20)

        # Set the file pointer to the beginning of the buffer
        buffer.seek(0)

        # Replace the image file with the compressed file
        new_image = File(buffer, name=image.name)

        return new_image

    def save(self, commit=True):
        item = super().save(commit=False)

        # Get the compressed image file
        compressed_image = self.cleaned_data.get('image')

        if compressed_image:
            item.image = compressed_image

        if commit:
            item.save()

        return item




class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image', 'phone_number')

        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Please, briefly describe your item'
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder':'Number only'
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
                'required': True,
            }),
            'phone_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Optional! for buyers to contact you',
            }),
        }



    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            return None

        # Open the image using Pillow
        img = Image.open(image)

        # Check the image size
        max_size = 100 * 1024  # 100 kB
        if image.size <= max_size:
            return image

        # Convert the image to RGB mode if it's in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        elif img.mode == 'P':
            img = img.convert('RGB')

        # Resize the image
        width, height = img.size
        if width > 1000 or height > 1000:
            if width > height:
                new_width = 1000
                new_height = int((height / width) * 1000)
            else:
                new_height = 1000
                new_width = int((width / height) * 1000)
            img = img.resize((new_width, new_height))

        # Compress the image and save it to a BytesIO object
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=20)

        # Set the file pointer to the beginning of the buffer
        buffer.seek(0)

        # Replace the image file with the compressed file
        new_image = File(buffer, name=image.name)

        return new_image

    def save(self, commit=True):
        item = super().save(commit=False)

        # Get the compressed image file
        compressed_image = self.cleaned_data.get('image')

        if compressed_image:
            item.image = compressed_image

        if commit:
            item.save()

        return item