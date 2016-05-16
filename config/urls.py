# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from permabots_www import views
from permabots_www.sitemaps import sitemaps
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
    url(r'^users/', include("permabots_www.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),
    # Your stuff: custom urls includes go here
    url(r'^processing/', include('microbot.urls_processing', namespace="microbot")),
    url(r'^api/v1/', include('microbot.urls_api', namespace="api")),
    url(r'^privacy-policy/$', TemplateView.as_view(template_name='pages/privacy_policy.html'), name="privacy-policy"),
    url(r'^docs/getting-started$', TemplateView.as_view(template_name='pages/getting-started.html'), name="getting-started"),
    url(r'^docs/api/', include('rest_framework_swagger.urls', namespace="swagger")),
    url(r'^bots/$', views.BotListView.as_view(), name="bot-list"),
    url(r'^bots/create/$', views.BotCreateView.as_view(), name="bot-create"),
    url(uuidzy(r'^bots/delete/(?P<pk>%u)/$'), views.BotDeleteView.as_view(), name="bot-delete"),
    url(uuidzy(r'^bots/update/(?P<pk>%u)/$'), views.BotUpdateView.as_view(), name="bot-update"),
    url(uuidzy(r'^bots/(?P<pk>%u)/$'), views.BotDetailView.as_view(), name="bot-detail"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/telegram/create/$'), views.TelegramBotCreateView.as_view(), name="bot-telegram-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/telegram/update/(?P<pk>%u)/$'), views.TelegramBotUpdateView.as_view(), name="bot-telegram-update"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/telegram/delete/(?P<pk>%u)/$'), views.TelegramBotDeleteView.as_view(), name="bot-telegram-delete"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/kik/create/$'), views.KikBotCreateView.as_view(), name="bot-kik-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/kik/update/(?P<pk>%u)/$'), views.KikBotUpdateView.as_view(), name="bot-kik-update"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/kik/delete/(?P<pk>%u)/$'), views.KikBotDeleteView.as_view(), name="bot-kik-delete"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/messenger/create/$'), views.MessengerBotCreateView.as_view(), name="bot-messenger-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/messenger/update/(?P<pk>%u)/$'), views.MessengerBotUpdateView.as_view(), name="bot-messenger-update"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/messenger/delete/(?P<pk>%u)/$'), views.MessengerBotDeleteView.as_view(), name="bot-messenger-delete"),
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
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/telegram/create/$'), views.TelegramRecipientCreateView.as_view(), 
        name="hook-telegram-recipient-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/telegram/update/(?P<pk>%u)/$'), views.TelegramRecipientUpdateView.as_view(), 
        name="hook-telegram-recipient-update"),     
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/telegram/delete/(?P<pk>%u)/$'), views.TelegramRecipientDeleteView.as_view(), 
        name="hook-telegram-recipient-delete"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/kik/create/$'), views.KikRecipientCreateView.as_view(), 
        name="hook-kik-recipient-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/kik/update/(?P<pk>%u)/$'), views.KikRecipientUpdateView.as_view(), 
        name="hook-kik-recipient-update"),     
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/kik/delete/(?P<pk>%u)/$'), views.KikRecipientDeleteView.as_view(), 
        name="hook-kik-recipient-delete"),  
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/messenger/create/$'), views.MessengerRecipientCreateView.as_view(), 
        name="hook-messenger-recipient-create"),
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/messenger/update/(?P<pk>%u)/$'), views.MessengerRecipientUpdateView.as_view(), 
        name="hook-messenger-recipient-update"),     
    url(uuidzy(r'^bots/(?P<bot_pk>%u)/hooks/(?P<hook_pk>%u)/recipients/messenger/delete/(?P<pk>%u)/$'), views.MessengerRecipientDeleteView.as_view(), 
        name="hook-messenger-recipient-delete"),  
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
