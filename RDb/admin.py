from RDb.models import NEResource,Dependency,NEMaterial,NEProduct,NEMaterialClass,NEProductClass,NEActor
from RDb.models import NECitation,NEProcess,NEProcessIO,NESurveyValue,NEInfoCitation,NESurveyInfo,NEProperty,NEPropertyClass
from django.contrib import admin

# Register your models here.
class DependencyInline(admin.TabularInline):
    model = Dependency
class CitationInline(admin.TabularInline):
    model = NECitation
class ProcessIOInline(admin.TabularInline):
    model = NEProcessIO
class ResourceInline(admin.TabularInline):
    model = NEResource
class NEResourceAdmin(admin.ModelAdmin):
    inlines = [DependencyInline]
class NESurveyValueAdmin(admin.ModelAdmin):
    inlines = [CitationInline]
    fk_name = 'resource'
    extra = 1
class NEProcessAdmin(admin.ModelAdmin):
    inlines = [ProcessIOInline]
class NEMaterialAdmin(admin.ModelAdmin):
    inlines = [ResourceInline]
class NEProductAdmin(admin.ModelAdmin):
    inlines = [ResourceInline]    

admin.site.register(NEResource,NEResourceAdmin)
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