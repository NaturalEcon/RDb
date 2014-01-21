from django.shortcuts import render
from RDb.models import NEResource
from django.http import HttpResponse

def index(request):
    resource_list = NEResource.objects.order_by('name')
    output = ', <br/>'.join([r.name + ': ' + r.description for r in resource_list])
    return HttpResponse(output)