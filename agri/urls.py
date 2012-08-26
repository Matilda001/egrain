from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from profiles.forms import RegistrationFormProfile
from profiles import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agri.views.home', name='home'),
    # url(r'^agri/', include('agri.foo.urls')),
    url(r'^$', 'egrain.views.map_view', name='show_map'),
    url(r'^show_history/(?P<crop_id>\d+)/$', 'egrain.views.history_view', name='show_history'),
    url(r'^add_history/$', 'egrain.views.history_add', name='add_history'),
    url(r'^add_agriculture/$', 'egrain.views.agriculture_add', name='add_agriculture'),
    url(r'^add_manure/$', 'egrain.views.manure_add', name='add_manure'),
    url(r'^add_cornfield/$', 'egrain.views.database_add', name='add_cornfield'),

    url(r'^accounts/login/$', 'egrain.views.login', {}, 'login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}, 'logout'),
    #url(r'^$', 'twitter.views.logout_view'),
    url(r'^accounts/register/$', 'registration.views.register', {'form_class': RegistrationFormProfile, 'backend': 'registration.backends.default.DefaultBackend',}, name='registration_register'),
    url(r'^accounts/', include('registration.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^accounts/profile/(?P<username>\w+)/$', views.edit_profile, name='profiles_edit_profile'),
    (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)