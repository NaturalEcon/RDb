from django.db import models
from commonmodels import *
from basemodels import *
from managers import *
from types import infotypes
"""
NE Descriptive Models:
Django model and form classes for the descriptive half of RDb.
Created on Tue Jan  7 12:55:59 2014

:author: acumen
"""

#class ResourceForm(ModelForm):
#    class Meta:
#        model = NEResource
#        fields = ['name', 'short_name', 'long_name','description']

class NEProcessIO(ABOUT,VALUE):
    """
    NEProcessIO: Adjacency table for NEProcesses.
    :param arg_type: The type of entry on this row (Inputs and outputs occupy separate rows).
    :const argtypes: The choices for arg_type (Input or Output only)
    """
    argtypes = (('I','Input'),('O','Output'))
    arg_type = models.CharField(max_length=1,choices=argtypes,verbose_name='Argument type')
    
    class Meta:
        verbose_name = 'Process IO'
        verbose_name_plural = 'Process IO'
        app_label='RDb'
        db_table = 'RDb_neprocessio'
    
    def __repr__(self):
        return '%s: %f x %s' % (self.name,self.value,self.resource.name)
        
    def __unicode__(self):
        return self.__repr__()


class NECapital(ABOUT):
    """
    NECapital: An adjancency table that associates NEProcesses with NEResources.
    :param resource: The capital resource associated with the process.
    :param process: The process enabled by this capital.
    """
    
    class Meta:
        verbose_name = 'Capital'
        verbose_name_plural = 'Capitals'
        app_label='RDb'
        db_table = 'RDb_necapital'


class NEProperty(DESCRIPTION,ABOUT,VALUE):
    """
    NEProperty: A quantified description of an NEOBJECT.
    :param error: The error range of the property.
    :type error: An up to 64-character string.
    """
    valuetype = None
    error = models.CharField(max_length=64,blank=True,null=True)
    effects = models.ManyToManyField('NEProperty',through='NEEffect',
                                     related_name='affected_by',symmetrical=False)
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        app_label='RDb'
        db_table = 'RDb_neproperty'
        

class NEEffect(DESCRIPTION,VALUE):
    """
    NEEffect: Describes the interaction of properties.
    :param sub: The subject property in the relationship, or 'A' in 'A affects B'.
    :param obj: The object property in the relationship, or 'B' in 'A affects B'.
    """
    subject_property = models.ForeignKey(NEProperty,related_name='obj_property')
    # affects:
    object_property = models.ForeignKey(NEProperty,related_name='subj_property')
    # (by VALUE)
    
    class Meta:
        verbose_name = 'Affectation'
        app_label='RDb'
        db_table = 'RDb_neaffectation'
    
    def __repr__(self):
        return "%s affects %s by %5.2f %s per %s" % (self.primary,self.secondary,self.value,self.primary.unit,self.secondary.unit)
    def __unicode__(self):
        return self.__repr__()


class NECollectionMembers(ABOUT):
    """
    NECollectionMembers: The adjacency table for NECollections
    :param cid: The primary key of the parent collection.
    """
    cid = models.ForeignKey('NECollection',related_name='collection_members')
    objects = ABOUTManager()    
    
    class Meta:
        verbose_name= 'Collection Member'
        verbose_name_plural = 'Collection Members'
        app_label='RDb'
        db_table = 'RDb_necollectionmembers'
        
    def __repr__(self):
        output = '#%i:' % self.cid
        if self.resource is not None:
            output += ' %s ' % self.resource
        if self.process is not None:
            output += ' %s ' % self.process
        if self.actor is not None:
            output += ' %s ' % self.actor
        return output
        
    def __unicode__(self):
        return self.__repr__()



class NEDependency(DESCRIPTION,VALUE):
    """
    NEDependency: An ajacency map for the composition non-trivial NEResources.
    :param parent_resource: The subject of this dependency.
    :param dependency: The object for this dependency.
    """
    parent_resource = models.ForeignKey('NEResource',related_name='backward_dependencies',
                                        related_query_name='backward_dependency')
    dependency = models.ForeignKey('NEResource',related_name='forward_dependencies',
                                        related_query_name='forward_dependency')
    
    class Meta:
        verbose_name = 'Dependency'
        verbose_name_plural = 'Dependencies'
        unique_together = (('parent_resource','dependency'),)
        app_label='RDb'
        db_table = 'RDb_nedependency'
    
    def __repr__(self):
        return "%s requires %5.2f x %s" % (self.parent_resource,self.dependency_mult,self.dependency)
    def __unicode__(self):
        return self.__repr__()

        
class NESurvey(ABOUT,VALUE,DESCRIPTION):
    """
    NESurvey: An abstract class for collection of data about an NEOBJECT.    
    :param sub: The subject of the survey.
    :param obj: If this field is not null, it is the object of the survey, in the sense, "value obj valuetype by sub".
    :param survey_date: The date on which the survey was taken or entered into the database (the former should have precedence).
    :param source: The location about which the survey is concerned (not where it was taken).
    """
    sub   = models.CharField(max_length=1)
    obj = models.CharField(max_length=1,blank=True,null=True)
    #
    survey_date = models.DateField(auto_now_add=True,blank=True,null=True)
    source = models.TextField(verbose_name='Location')
    
    dataframe = DataFrameManager()    

    class Meta:
        abstract=True
        app_label='RDb'


class NESurveyValue(NESurvey):
    """
    NESurveyValue: A single-datum survey value about a singular NEOBJECT (i.e., not a collection).
    :param date: The date on which the datum was observed.
    :param reference: Where the datum came from.
    """
    date = models.DateField(auto_now_add=True,blank=True,null=True)
    reference = models.ForeignKey('NECitation',verbose_name='Citation',null=True,blank=True)
    
    class Meta:
        verbose_name = 'Survey Value'
        app_label='RDb'
        db_table = 'RDb_nesurveyvalue'
        
    def __repr__(self):
        output = ''
        if self.resource is not None:
            output = '%s of %s: %5.2f %s' % (self.get_valuetype_display(),self.resource,self.value,self.unit)
        elif self.process is not None:
            output = '%s of %s: %5.2f %s' % (self.get_valuetype_display(),self.process,self.value,self.unit)
        elif self.actor is not None:
            output = '%s of %s: %5.2f %s' % (self.get_valuetype_display(),self.actor,self.value,self.unit)
        else:
            'Ambiguous survey.  Please delete or re-enter.'
        return output  
    def __unicode__(self):
        return self.__repr__()
   

class NESurveyInfo(NESurvey):
    """
    NESurveyInfo: A survey entry that incorporates multiple data points, such as a meta-study, forecast, or statistical analysis.
    :param infotype: The type of collection of data.  Choices can be found in commonmodels.
    :param start_date: The earliest data point.
    :param end_date: The latest data point.
    :param records: A many-to-many field for data sources.
    """
    infotype = models.CharField(max_length=1,choices=infotypes,default="u") # Specifies the type of quantification.

    start_date = models.DateField(auto_now_add=True,blank=True,null=True)
    end_date = models.DateField(auto_now_add=True,blank=True,null=True)
    # M2M
    records = models.ManyToManyField('NECitation',through='NEInfoCitation',
                                     related_name='cited_by',symmetrical=True)    
    class Meta:
        verbose_name = 'Survey Info'
        verbose_name_plural = 'Survey Info' 
        app_label='RDb'
        db_table = 'RDb_nesurveyinfo'
    
    def __repr__(self):
        output = ''
        if self.collection is not None and self.resource is not None:
            output = '%s of %s %s %s: %5.2f %s' % (self.get_valuetype_display(),self.resource,self.relationship,self.collection,self.value,self.unit)
        elif self.collection is not None and self.process is not None:
            output = '%s of %s %s %s: %5.2f %s' % (self.get_valuetype_display(),self.process,self.relationship,self.collection,self.value,self.unit)
        elif self.collection is not None and self.actor is not None:
            output = '%s of %s %s %s: %5.2f %s' % (self.get_valuetype_display(),self.actor,self.relationship,self.collection,self.value,self.unit)
        elif self.resource is not None:
            output = '%s of %s: %5.2f %s' % (self.get_valuetype_display(),self.resource,self.value,self.unit)
        elif self.process is not None:
            output = '%s of %s: %5.2f %s' % (self.get_valuetype_display(),self.process,self.value,self.unit)
        elif actor is not None:
            output = '%s of %s: %5.2f %s' % (self.get_valuetype_display(),self.actor,self.value,self.unit)
        else:
            'Ambiguous survey.  Please delete or re-enter.'
        return output
    def __unicode__(self):
        return self.__repr__()


class NEInfoCitation(ABOUT):
    """
    NEInfoCitation: A collection of NECitations for NESurveyInfo.
    :param iid: The NESurveyInfo entry this item is associated with.
    :param cid: An NECitation in the collection for IID.
    """
    iid = models.ForeignKey(NESurveyInfo,related_name='survey_info')
    cid = models.ForeignKey('NECitation',related_name='citation')
    class Meta:
        verbose_name = 'Info Citation'
        app_label='RDb'
        db_table = 'RDb_neinfocitation'