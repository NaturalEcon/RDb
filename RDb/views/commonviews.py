from RDb.models.commonmodels import *
from RDb.models.basemodels import *
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
"""
Created on Tue Feb  4 12:19:45 2014

@author: acumen
"""

def index(request):
    resource_list = NEResource.objects.order_by('name')
    
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'resource_list': resource_list
    })
    return HttpResponse(template.render(context))

class NEOBJECTDetailView(DetailView):
    model = NEOBJECT