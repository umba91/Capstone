from django.contrib import admin
from .models import *

admin.site.register(Specie)
admin.site.register(Color)
admin.site.register(Size)


class BugAdmin(admin.ModelAdmin):
    list_display=('id','title','species','color','size','status')
    list_editable=('status',)
admin.site.register(Bug,BugAdmin)

#Bug Attribute
class BugAttributeAdmin(admin.ModelAdmin):
    list_display=('id','bug','species','color','size')
admin.site.register(BugAttribute,BugAttributeAdmin)