from RDb.models.basemodels import *
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

"""
Created on Tue Feb  4 12:19:47 2014

@author: acumen
"""

class ResourceDetailView(DetailView):
    """ResourceDetailView: The detail view for NEResource."""
    model = NEResource
    template_name = 'RDb/resource_detail.html'
    qs = None
    survey_data = None
    survey_info = None
    properties  = None
    dependencies= None
    
    def get_obj(self):
        self.obj = super(ResourceDetailView, self).get_object()
        self.survey_data =  NESurveyValue.objects.filter(resource__exact=self.obj).all()
        self.survey_info =  NESurveyInfo.objects.filter(resource__exact=self.obj).all()
        self.properties =   NEProperty.objects.first()#filter(resource__exact=ner_uuid)
        self.dependencies = NEDependency.objects.filter(parent_resource__exact=self.obj).all()
        
        
    def get_context_data(self, **kwargs):
        context = super(ResourceDetailView, self).get_context_data(**kwargs)
        self.get_obj()
        context['survey_data'] = self.survey_data
        context['survey_info'] = self.survey_info
        context['properties'] = self.properties
        context['dependencies'] = self.dependencies
        return context

        
class ActorDetailView(DetailView):
    """ActorDetailView: The detail view for NEActor."""
    model = NEActor
    template_name = 'RDb/actor_detail.html'
   
class ProcessDetailView(DetailView):
    """ProcessDetailView: The detail view for NEProcess."""
    model = NEProcess
    template_name = 'RDb/process_detail.html'
    
class ResourceListView(ListView):
    """ResourceListView: The list view for NEResource."""
    model = NEResource
    template_name = 'RDb/resource_list.html'
    
    #sorts the list of resources into bins, in the following data structure:
    #  [{'a':'FIRST_LETTER','b':[LIST_OF_RESOURCES_BEGINNING_WITH_LETTER]},...]
    def resource_list(self):
        resource_list = NEResource.objects.order_by('name')
        char_list = []
        indices = []
        c = 0
        for r in resource_list:
            name = r.name
            if name is u'':
                pass
            elif name[0] not in char_list:
                char_list += [name[0]]
                indices += [c]
            c += 1
        i = indices[0]
        split_resource_list = []
        for j in indices[1:]:
            split_resource_list += [resource_list[i:j]]
            i = j
        final_list = [] 
        for i in range(len(char_list)-1):
            final_list+=[dict(zip(('a','b'),[char_list[i],split_resource_list[i]]))]
        return final_list
    
    def get_context_data(self, **kwargs):
        resource_list = self.resource_list()
        context = super(ResourceListView, self).get_context_data(**kwargs)
        context['resource_list'] = resource_list
        return context
   
class ActorListView(ListView):
    """ActorListView: The list view for NEActor."""
    model = NEActor
    template_name = 'RDb/actor_detail.html'
   
class ProcessListView(ListView):
    """ProcessListView: The list view for NEProcess."""
    model = NEProcess
    template_name = 'RDb/process_detail.html'