from django.contrib import admin
from .models import *

admin.site.register(Species)
admin.site.register(Color)
admin.site.register(Size)


class BugAdmin(admin.ModelAdmin):
    list_display=('id','name','species','status')
    list_editable=('status',)
admin.site.register(Bug,BugAdmin)

#Bug Attribute
class BugAttributeAdmin(admin.ModelAdmin):
    list_display=('id','bug','species','color','size')
admin.site.register(BugAttribute,BugAttributeAdmin)