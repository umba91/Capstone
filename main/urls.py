from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('',views.home,name='home'),
    path('category-list',views.category_list,name='category-list'),
    path('bug-entry/<str:name>',views.bug_entry,name='bug-entry'),

    path('placeholder.html',views.placeholder,name='placeholder'),
    path('bug_pages/',views.placeholder,name='placeholder'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    from django.conf import settings


