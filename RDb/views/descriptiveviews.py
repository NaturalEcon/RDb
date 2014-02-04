from RDb.models.descriptivemodels import *
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
"""
Created on Tue Feb  4 12:19:49 2014

@author: acumen
"""

class SurveyDetailView(DetailView):
    """SurveyDetailView: The detail view for NESurvey."""
    model = NESurvey
    template_name = 'RDb/survey_detail.html'
    
    def format_object(self):
        survey = super(SurveyDetailView, self).get_object()        
        about = None
        about_string = ''
        if survey.resource is not None:
            about_string = 'Resource'
            about = survey.resource
        if survey.actor is not None:
            about_string = 'Actor'
            about = survey.actor
        if survey.process is not None:
            about_string = 'Process'
            about = survey.process                
        citation = survey.record
        cmid = "%s, %s." % (citation.author,citation.date)
        cend = ''
        value = ' %5.2f%s' % (survey.value,survey.unit)
        data_description = '%s on %s from %s:' % (survey.get_valuetype_display().capitalize(),survey.startdate,survey.source)
        if citation.doi is not '':
            cend = "%s" % citation.doi
        if citation.isbn is not '':
            cend = "%s" % citation.isbn
        return {'ctitle':citation.title,'cmid':cmid,'cend':cend,'datadesc':data_description,
                'value': value,'about_string':about_string,'about':about}
    
    def get_context_data(self, **kwargs):
        context = super(SurveyInfoDetailView, self).get_context_data(**kwargs)
        args = self.format_object()
        context['datadesc'] = args['datadesc']
        context['value'] = args['value']
        context['ctitle'] = args['ctitle']
        context['cmid'] = args['cmid']
        context['cend'] = args['cend']
        context['about'] = args['about']
        context['about_string'] = args['about_string']
        return context

        
class SurveyValueDetailView(SurveyDetailView):
    """SurveyValueDetailView: The detail view for NESurveyValue."""
    model = NESurveyValue
    
    
class SurveyInfoDetailView(SurveyDetailView):
    """SurveyInfoDetailView: The detail view for NESurveyInfo."""
    model = NESurveyInfo

class SurveyListView(ListView):
    """SurveyListView: Common base for survey list views."""
    template_name = 'RDb/survey_detail.html'
   
class SurveyValueListView(SurveyListView):
    """SurveyValueListView: The list view for NESurveyValue."""
    model = NESurveyValue

class SurveyInfoListView(SurveyListView):
    """SurveyInfoListView: The list view for NESurveyInfo."""
    model = NESurveyInfo