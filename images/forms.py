from django import forms
from .models import Image
from django.core.files.base import ContentFile
from .utils import slugify
import requests


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('Данный url не совпадает с валидными расширениями картинок.')
        return url

    def save(self,
             force_insert=False,
             force_update=False,
             commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.split('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        #Скачиваеем изображение с url адреса
        response = requests.get(image_url)
        image.image.save(image_name,
                         ContentFile(response.content),
                         save=False)
        if commit:
            image.save()
        return image
