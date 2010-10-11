from django.conf.urls.defaults import *
from django.conf import settings

from moniek.base.views import direct_to_folder


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounting/', include('moniek.accounting.urls')),
    (r'^media/(?P<subdir>.*)', direct_to_folder,
	    {'root': settings.MEDIA_ROOT}),
)
