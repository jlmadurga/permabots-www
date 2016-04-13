# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from permabots import views
from permabots.sitemaps import sitemaps
from django.contrib.sitemaps.views import sitemap

def uuidzy(url):
    return url.replace('%u', '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',content_type='text/plain')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    # User management
    url(r'^users/', include("permabots.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),
    # Your stuff: custom urls includes go here
    url(r'^processing/', include('microbot.urls_processing', namespace="microbot")),
    url(r'^api/v1/', include('microbot.urls_api', namespace="api")),
    url(r'^docs/getting-started$', TemplateView.as_view(template_name='pages/getting-started.html'), name="getting-started"),
    url(r'^docs/api/', include('rest_framework_swagger.urls', namespace="swagger")),
    url(r'^bots/$', views.BotListView.as_view(), name="bot-list"),
    url(r'^bots/create/$', views.BotCreateView.as_view(), name="bot-create"),
    url(uuidzy(r'^bots/delete/(?P<pk>%u)/$'), views.BotDeleteView.as_view(), name="bot-delete"),
    url(uuidzy(r'^bots/update/(?P<pk>%u)/$'), views.BotUpdateView.as_view(), name="bot-update"),
    url(uuidzy(r'^bots/(?P<pk>%u)/$'), views.BotDetailView.as_view(), name="bot-detail"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/$'), views.HandlerListView.as_view(), name="handler-list"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/create/$'), views.HandlerCreateView.as_view(), name="handler-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/update/(?P<pk>%u)/$'), views.HandlerUpdateView.as_view(), name="handler-update"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/delete/(?P<pk>%u)/$'), views.HandlerDeleteView.as_view(), name="handler-delete"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/(?P<pk>%u)/$'), views.HandlerDetailView.as_view(), name="handler-detail"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/(?P<handler_pk>%u)/urlparams/create/$'), views.UrlParameterCreateView.as_view(), 
        name="handler-urlparameter-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/(?P<handler_pk>%u)/urlparams/update/(?P<pk>%u)/$'), views.UrlParameterUpdateView.as_view(), 
        name="handler-urlparameter-update"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/(?P<handler_pk>%u)/urlparams/delete/(?P<pk>%u)/$'), views.UrlParameterDeleteView.as_view(), 
        name="handler-urlparameter-delete"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/(?P<handler_pk>%u)/headerparams/create/$'), views.HeaderParameterCreateView.as_view(), 
        name="handler-headerparameter-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/(?P<handler_pk>%u)/headerparams/update/(?P<pk>%u)/$'), views.HeaderParameterUpdateView.as_view(), 
        name="handler-headerparameter-update"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/handlers/(?P<handler_pk>%u)/headerparams/delete/(?P<pk>%u)/$'), views.HeaderParameterDeleteView.as_view(), 
        name="handler-headerparameter-delete"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/$'), views.HookListView.as_view(), name="hook-list"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/create/$'), views.HookCreateView.as_view(), name="hook-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/update/(?P<pk>%u)/$'), views.HookUpdateView.as_view(), name="hook-update"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/delete/(?P<pk>%u)/$'), views.HookDeleteView.as_view(), name="hook-delete"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<pk>%u)/$'), views.HookDetailView.as_view(), name="hook-detail"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/create/$'), views.RecipientCreateView.as_view(), 
        name="hook-recipient-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/update/(?P<pk>%u)/$'), views.RecipientUpdateView.as_view(), 
        name="hook-recipient-update"),     
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/delete/(?P<pk>%u)/$'), views.RecipientDeleteView.as_view(), 
        name="hook-recipient-delete"),     
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/env/$'), views.EnvironmentVarListView.as_view(), name="env-list"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/env/create/$'), views.EnvironmentVarCreateView.as_view(), name="env-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/env/update/(?P<pk>%u)/$'), views.EnvironmentVarUpdateView.as_view(), name="env-update"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/env/delete/(?P<pk>%u)/$'), views.EnvironmentVarDeleteView.as_view(), name="env-delete"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/env/(?P<pk>%u)/$'), views.EnvironmentVarDetailView.as_view(), name="env-detail"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/states/create/$'), views.StateCreateView.as_view(), name="state-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/states/update/(?P<pk>%u)/$'), views.StateUpdateView.as_view(), name="state-update"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/states/delete/(?P<pk>%u)/$'), views.StateDeleteView.as_view(), name="state-delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permission Denied")}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]
    
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
