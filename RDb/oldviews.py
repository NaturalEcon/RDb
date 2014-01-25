from django.shortcuts import render
from RDb.descriptivemodels import NEResource, NESurveyValue, NESurveyInfo, NEProperty, NEDependency, \
NEActor, NEProcess, NECitation, valuetypes
from django.template import RequestContext, loader
from django.http import HttpResponse

def index(request):
    resource_list = NEResource.objects.order_by('name')
    
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'resource_list': resource_list
    })
    return HttpResponse(template.render(context))

def resource_view(request,ner_uuid):
    resource = NEResource.objects.filter(rid__exact=ner_uuid).first()
    name = resource.name
    description = resource.description
    survey_data = NESurveyValue.objects.filter(resource__exact=ner_uuid)
    survey_info = NESurveyInfo.objects.filter(resource__exact=ner_uuid)
    properties = NEProperty.objects.first()#filter(resource__exact=ner_uuid)
    dependencies = NEDependency.objects.filter(parent_resource__exact=ner_uuid)
    
    context = RequestContext(request, {
        'resource': resource,
        'name': name,
        'description': description,
        'survey_data': survey_data.all(),
        'survey_info': survey_info.all(),
        'properties': properties,
        'dependencies': dependencies.all(),
    })
    return render(request,'RDb/resource.html',context)

def neactor(request,nea_id):
    actor = NEActor.objects.filter(rid__exact=nea_id).first()
    name = actor.name
    description = actor.description
    survey_data = NESurveyValue.objects.filter(actor__exact=nea_id)
    survey_info = NESurveyInfo.objects.filter(actor__exact=nea_id)
    
    context = RequestContext(request, {
        'resource': actor,
        'name': name,
        'description': description,
        'survey_data': survey_data.all(),
        'survey_info': survey_info.all(),
    })
    return render(request,'RDb/resource.html',context)

def neprocess(request,nep_id):
    process = NEProcess.objects.filter(rid__exact=nep_id).first()
    name = process.name
    description = process.description
    survey_data = NESurveyValue.objects.filter(process__exact=nep_id)
    survey_info = NESurveyInfo.objects.filter(process__exact=nep_id)
    
    context = RequestContext(request, {
        'resource': process,
        'name': name,
        'description': description,
        'survey_data': survey_data.all(),
        'survey_info': survey_info.all(),
    })
    return render(request,'RDb/resource.html',context)    
    
def resource_list(request):
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
    
    ###
    template = loader.get_template('resource_list.html')
    context = RequestContext(request, {
        'indexed_resource_list': final_list
    })
    return HttpResponse(template.render(context))

    
def nesurveyvalue(request,sv_id):
    survey = NESurveyValue.objects.filter(id__exact=sv_id).first()
    citation = NECitation.objects.filter(id__exact=survey.record.id).first()
    cmid = "%s, %s." % (citation.author,citation.date)
    cend = ''
    if citation.doi is not None:
        cend = "%s" % citation.doi
    if citation.isbn is not None:
        cend = "%s" % citation.isbn
        
    resource = survey.resource
    actor = survey.actor
    process = survey.process
    
    about = None
    about_string = ''
    if resource is not None:
        about_string = 'Resource'
        about = resource
    if actor is not None:
        about_string = 'Actor'
        about = actor
    if process is not None:
        about_string = 'Process'
        about = process
        
    value_string = '%s %5.2f%s' % (survey.valuetype,survey.value,survey.unit)
    context = RequestContext(request, {
        'about': about,
        'about_string': about_string,
        'description': survey.description,
        'value_string': value_string,
        'ctitle': citation.title,
        'cmid': cmid,
        'cend': cend,
    })
    return render(request,'RDb/surveyvalue.html',context)
    
def nesurveyinfo(request,si_id):
    survey = NESurveyInfo.objects.filter(id__exact=si_id).first()
    citation = NECitation.objects.filter(id__exact=survey.record.id).first()
    
    cmid = "%s, %s." % (citation.author,citation.date)
    cend = ''
    if citation.doi is not '':
        cend = "%s" % citation.doi
    if citation.isbn is not '':
        cend = "%s" % citation.isbn
        
    resource = survey.resource
    actor = survey.actor
    process = survey.process
    
    about = None
    about_string = ''    
    if resource is not None:
        about_string = 'Resource'
        about = resource
    if actor is not None:
        about_string = 'Actor'
        about = actor
    if process is not None:
        about_string = 'Process'
        about = process
        
    dd_string = '%s on %s:' % (survey.get_valuetype_display().capitalize(),survey.startdate)
    value_string = ' %5.2f%s' % (survey.value,survey.unit)
    context = RequestContext(request, {
        'about': about,
        'about_string': about_string,
        'survey': survey,
        'datadesc': dd_string,
        'value': value_string,
        'valuetypes':valuetypes,
        'ctitle': citation.title,
        'cmid': cmid,
        'cend': cend,
    })
    return render(request,'RDb/surveyvalue.html',context)