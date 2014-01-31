from django.db import models
from commonmodels import *
from django.forms import ModelForm
from managers import *

"""
NE Descriptive Models:
Django model and form classes for the descriptive half of RDb.
Created on Tue Jan  7 12:55:59 2014

:author: acumen
:attr ctypes: Types of sources that can be cited.
"""
ctypes = (
    ('J','Journal article'),('R','Report'),('P','Personal communication'),
    ('B','Book'),('M','Memo')
)

class NEResource(DESCRIPTION,NEOBJECT):
    """
    NEResource: NEOBJECT for materials and energy.
    :param dependencies: A many-to-many field for the resources this one is composed of or depend on to exist.
    :param subclasses: A many-to-many field for the resources that are more specialized cases of this one.
    """
    dependencies = models.ManyToManyField('NEResource', related_name='fdeps',related_query_name='fdep', 
                                          through='NEDependency', symmetrical=False)
    subclasses   = models.ManyToManyField('NEResource', related_name='superclasses', related_query_name='superclass', 
                                          through='NESubclass', symmetrical=False)
    
    class Meta:
        verbose_name = 'Resource'
    
    def __repr__(self):
        return self.name
    def __unicode__(self):
        return self.__repr__()

class ResourceForm(ModelForm):
    class Meta:
        model = NEResource
        fields = ['name', 'short_name', 'long_name','description']


class NEActor(NEOBJECT,DESCRIPTION):
    """
    NEActor: An NEOBJECT representing active systems, organisms, or other complexes with agency (externally).
    :param children: A many-to-many field for the children of this actor.
    :param atype: The type of actor that this is.  See the common models for the choices.
    """
    children = models.ManyToManyField('NEActor',related_name='actor_parents',blank=True,null=True)
    atype = models.CharField(max_length=3,choices=atypes)

    class Meta:
        verbose_name = 'Actor'


class NEProcess(NEOBJECT,DESCRIPTION):
    """
    NEProcess: An NEOBJECT representing an interaction that results in a change from one set of NEOBJECTS to another.
    :param ptype: The type of process this is.  See the common models for the choices.
    :param io: A many-to-many field for the inputs and outputs of this process.
    """
    ptype = models.CharField(max_length=2,choices=ptypes,verbose_name='Process type')
    
    io = models.ManyToManyField( NEResource,through='NEProcessIO',symmetrical=False,
                                verbose_name='Inputs/Outputs',related_name='relevant_processes')
     
    class Meta:
        verbose_name = 'Process'
        verbose_name_plural = 'Processes'

    def __repr__(self):
        return "%s (Type %s)\n Inputs: %s \n Outputs: %s" % (self.pname,self.get_ptype_display(),self.inputs,self.outputs)


class NEProcessIO(DESCRIPTION,ABOUT,VALUE):
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
    
    def __repr__(self):
        return '%s: %f x %s' % (self.name,self.arg_weight,self.resource.name)
    def __unicode__(self):
        return self.__repr__()


class NEProperty(DESCRIPTION,ABOUT,VALUE):
    """
    NEProperty: A quantified description of an NEOBJECT.
    :param error: The error range of the property.
    :type error: An up to 64-character string.
    """
    error = models.CharField(max_length=64,blank=True,null=True)
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        

class NEAffectation(DESCRIPTION,VALUE):
    """
    NEAffectation: Describes the interaction of properties.
    :param sub: The subject property in the relationship, or 'A' in 'A affects B'.
    :param obj: The object property in the relationship, or 'B' in 'A affects B'.
    """
    sub = models.ForeignKey(NEProperty)
    # affects:
    obj = models.ForeignKey(NEProperty)
    # (by VALUE)
    
    def __repr__(self):
        return "%s affects %s by %5.2f %s per %s" % (self.primary,self.secondary,self.value,self.primary.unit,self.secondary.unit)
    def __unicode__(self):
        return self.__repr__()


class NECollection(NEOBJECT,ABOUT,DESCRIPTION):
    """
    NECollection: A group of heterogeneous NEOBJECTS.
    :param collection_id: The idea of the collection.  Separate from the primary key.
    """
    collection_id = models.IntegerField(verbose_name='Collection ID')
    
    class Meta:
        verbose_name= 'Collection'
        verbose_name_plural = 'Collections'
        
    def __repr__(self):
        output = '#%i:' % self.collection_id
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
    parent_resource = models.ForeignKey(NEResource,related_name='backward_dependencies',
                                        related_query_name='backward_dependency')
    dependency = models.ForeignKey(NEResource,related_name='forward_dependencies',
                                        related_query_name='forward_dependency')
    
    class Meta:
        verbose_name = 'Dependency'
        verbose_name_plural = 'Dependencies'
        unique_together = (('parent_resource','dependency'),)
    
    def __repr__(self):
        return "%s requires %5.2f x %s" % (self.parent_resource,self.dependency_mult,self.dependency)
    def __unicode__(self):
        return self.__repr__()


class NESubclass(DESCRIPTION):
    """
    NESubclass: Qualitative subgroup of NEResources.
    :param parent_class: The superclass in the relationship.
    :param child_class: The subclass in the relationship.
    """
    parent_class = models.ForeignKey(NEResource,related_name='parent_classes',
                                     related_query_name='parent_class')
    
    child_class = models.ForeignKey(NEResource,related_name='child_classes',
                                     related_query_name='child_class')
    
    class Meta:
        verbose_name = 'Subclass'
        verbose_name_plural = 'Subclasses'
    
    def __repr__(self):
        return 'Superclass: %s\nSubclass: %s' % (self.parent_class,self.child_class)
        
       
class NECitation(models.Model):
    """
    NECitation: A rudimentary citation data structure.
    :param title: The title of the cited work.
    :param author: The author of the cited work.
    :param date: The date on which the work was published.
    :param doi: The Document Object Identifier (DOI) for the work (optional).
    :param isbn: The International Standard Book Number (ISBN) for the work (optional).
    :param ctype: The type of work being cited.
    """
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50,blank=True,default='Unknown Author')
    date = models.DateField(blank=True,auto_now_add=True)
    doi = models.CharField(max_length=30,blank=True,default='',verbose_name='DOI')
    isbn = models.CharField(max_length=13,blank=True,default='',verbose_name='ISBN')
    ctype = models.CharField(max_length=1,choices=ctypes,verbose_name='Citation type')
    
    objects = models.Manager()
    dataframe = DataFrameManager()    
    
    class Meta:
        verbose_name = 'Citation'
    
    def __repr__(self):
        output = ""
        if self.title is not None: output += self.title + ""
        if self.author is not None: 
            output += self.author + "."
        if self.doi is not None: output += self.doi + " "
        return output

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


class NESurveyValue(NESurvey):
    """
    NESurveyValue: A single-datum survey value about a singular NEOBJECT (i.e., not a collection).
    :param date: The date on which the datum was observed.
    :param reference: Where the datum came from.
    """
    date = models.DateField(auto_now_add=True,blank=True,null=True)
    reference = models.ForeignKey(NECitation,verbose_name='Citation')
    
    class Meta:
        verbose_name = 'Survey Value'
        
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
   

class NESurveyInfo(models.Model):
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


class NEInfoCitation(models.Model):
    description = models.TextField(blank=True,default='')
    iid = models.ForeignKey(NESurveyInfo,related_name='info_citation')
    cid = models.ForeignKey(NECitation,related_name='meta_study')
    class Meta:
        verbose_name = 'Info Citation'
        