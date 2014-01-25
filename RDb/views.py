from django.shortcuts import render
from RDb.descriptivemodels import *
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


def index(request):
    resource_list = NEResource.objects.order_by('name')
    
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'resource_list': resource_list
    })
    return HttpResponse(template.render(context))

class ResourceDetailView(DetailView):
    model = NEResource
    template_name = 'RDb/resource_detail.html'
    qs = None
    survey_data = None
    survey_info = None
    properties  = None
    dependencies= None
    
    def get_qs(self):
        self.qs = super(ResourceDetailView, self).get_queryset()
        self.survey_data =  NESurveyValue.objects.filter(resource__exact=self.qs.first())
        self.survey_info =  NESurveyInfo.objects.filter(resource__exact=self.qs.first())
        self.properties =   NEProperty.objects.first()#filter(resource__exact=ner_uuid)
        self.dependencies = NEDependency.objects.filter(parent_resource__exact=self.qs.first())        
        
        
    def get_context_data(self, **kwargs):
        self.get_qs()
        context = super(ResourceDetailView, self).get_context_data(**kwargs)
        context['survey_data'] = self.survey_data
        context['survey_info'] = self.survey_info
        context['properties'] = self.properties
        context['dependencies'] = self.dependencies
        return context
        
class ActorDetailView(DetailView):
    model = NEActor
    template_name = 'RDb/actor_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ActorDetailView, self).get_context_data(**kwargs)
        return context
   
class ProcessDetailView(DetailView):
    model = NEProcess
    template_name = 'RDb/process_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ProcessDetailView, self).get_context_data(**kwargs)
        return context
   
class ResourceListView(ListView):
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
    model = NEActor
    template_name = 'RDb/actor_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ActorListView, self).get_context_data(**kwargs)
        
        return context
   
class ProcessListView(ListView):
    model = NEProcess
    template_name = 'RDb/process_detail.html'
    def get_context_data(self, **kwargs):
        return context
   
