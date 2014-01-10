from RDb.models import NEResource,NEDependency,NEMaterial,NEProduct,NEMaterialClass,NEProductClass,NEActor
from RDb.models import NECitation,NEProcess,NEProcessIO,NESurveyValue,NEInfoCitation,NESurveyInfo,NEProperty,NEPropertyClass
from django.contrib import admin

# Register your models here.
class DependencyInline(admin.TabularInline):
    model = NEDependency
    extra = 2
class CitationInline(admin.TabularInline):
    model = NECitation
class ProcessIOInline(admin.TabularInline):
    model = NEProcessIO
class ResourceInline(admin.TabularInline):
    model = NEResource
class NESurveyValueAdmin(admin.ModelAdmin):
    list_display = ('resource','date','valuetype','value','unit','loc')
    #inlines = [CitationInline]
    fk_name = 'resource'
    extra = 1
    
class NESurveyInfoAdmin(admin.ModelAdmin):
    list_display = ('resource','starttime','endtime','value','valuetype','infotype')
    
class NEProcessAdmin(admin.ModelAdmin):
    list_display = ('pname','ptype','inputs','outputs')
    inlines = [ProcessIOInline]
    
class NEMaterialAdmin(admin.ModelAdmin):
    list_display = ('name','mclass')
    inlines = [ResourceInline,DependencyInline]
    
class NEProductAdmin(admin.ModelAdmin):
    list_display = ('name','pclass')
    inlines = [ResourceInline]    

admin.site.register(NEResource)
admin.site.register(NEDependency)
admin.site.register(NEMaterial,NEMaterialAdmin)
admin.site.register(NEProduct,NEProductAdmin)
admin.site.register(NEMaterialClass)
admin.site.register(NEProductClass)
admin.site.register(NEActor)
admin.site.register(NECitation)
admin.site.register(NEProcess,NEProcessAdmin)
admin.site.register(NESurveyValue,NESurveyValueAdmin)
admin.site.register(NEInfoCitation)
admin.site.register(NESurveyInfo)
admin.site.register(NEProperty)
admin.site.register(NEPropertyClass)