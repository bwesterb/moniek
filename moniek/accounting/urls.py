from django.conf.urls.defaults import *

import moniek.accounting.views as views

urlpatterns = patterns('',
    url(r'^/?$', views.home, name='home'),
    url(r'^accounts/?$', views.accounts, name='accounts'),
    # Example:
    # (r'^moniek/', include('moniek.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
