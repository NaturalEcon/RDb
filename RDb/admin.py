from RDb.models import NEResource,NECollection,NEDependency,NESubclass,NEActor
from RDb.models import NECitation,NEProcess,NEProcessIO,NESurveyValue,NEInfoCitation,NESurveyInfo,NEProperty
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
    list_display = ('resource','date','valuetype','value','unit','location')
    #inlines = [CitationInline]
    fk_name = 'resource'
    extra = 1
class NEResourceAdmin(admin.ModelAdmin):
    list_display = ('name','short_name','description')
    
class NESurveyInfoAdmin(admin.ModelAdmin):
    list_display = ('resource','startdate','value','unit','valuetype','location')
   
class NEProcessAdmin(admin.ModelAdmin):
    list_display = ('name','ptype')
    
class NESubclassAdmin(admin.ModelAdmin):
    list_display = ('parent_class','child_class')
    
class NECollectionAdmin(admin.ModelAdmin):
    list_display = ('collection_name','resource','actor','process')    
    
admin.site.register(NEResource,NEResourceAdmin)
admin.site.register(NESubclass,NESubclassAdmin)
admin.site.register(NECollection,NECollectionAdmin)
admin.site.register(NEDependency)
admin.site.register(NEActor)
admin.site.register(NECitation)
admin.site.register(NEProcess,NEProcessAdmin)
admin.site.register(NESurveyValue,NESurveyValueAdmin)
admin.site.register(NEInfoCitation)
admin.site.register(NESurveyInfo,NESurveyInfoAdmin)
admin.site.register(NEProperty)