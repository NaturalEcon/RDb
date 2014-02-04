from RDb.models.commonmodels import *
from RDb.models.basemodels import *
from RDb.models.descriptivemodels import *
from django.contrib import admin

# Register your models here.
class DependencyInline(admin.TabularInline):
    model = NEDependency
    fk_name = 'parent_resource'
    extra = 2
class CitationInline(admin.TabularInline):
    model = NECitation
    
class ProcessIOInline(admin.TabularInline):
    model = NEProcessIO
     
class NESurveyValueAdmin(admin.ModelAdmin):
    list_display = ('resource','date','value_type','value','unit','source')
    #inlines = [CitationInline]
    fk_name = 'resource'
    extra = 1
class NEResourceAdmin(admin.ModelAdmin):
    list_display = ('name','short_name','description')
    
class NESurveyInfoAdmin(admin.ModelAdmin):
    list_display = ('resource','start_date','value','unit','value_type','source')
   
class NEProcessAdmin(admin.ModelAdmin):
    list_display = ('name','ptype')
    
class NERSubclassAdmin(admin.ModelAdmin):
    list_display = ('parent_class','child_class')
    
class NECollectionAdmin(admin.ModelAdmin):
    list_display = ('name','description')    
    
admin.site.register(NEResource,NEResourceAdmin)
admin.site.register(NERSubclass,NERSubclassAdmin)
admin.site.register(NECollection,NECollectionAdmin)
admin.site.register(NEDependency)
admin.site.register(NEActor)
admin.site.register(NECitation)
admin.site.register(NEProcess,NEProcessAdmin)
admin.site.register(NESurveyValue,NESurveyValueAdmin)
admin.site.register(NEInfoCitation)
admin.site.register(NESurveyInfo,NESurveyInfoAdmin)
admin.site.register(NEProperty)