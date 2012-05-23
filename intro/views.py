from django.template.response import TemplateResponse
from photo.models import Photo

def home(request):
    values = {
        'name': 'Sweetie!',
        'photos': Photo.objects.all(),
    }
    return TemplateResponse(request,'base.html',values)
