from microbot.models import Bot, Handler, Hook, EnvironmentVar, Request, Response, UrlParam, HeaderParam, TelegramRecipient, \
    State, TelegramBot, KikBot, KikRecipient
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from permabots import forms
from django.http import Http404


class BaseBotView(LoginRequiredMixin):
    success_msg = None
    
    def get_queryset(self):
        return Bot.objects.filter(owner=self.request.user)
    
    def get_success_url(self):
        messages.info(self.request, self.success_msg)
        return reverse_lazy('bot-list')

class BotListView(BaseBotView, generic.ListView):
    model = Bot
    template_name = "bots/list.html"
    
class BotCreateView(BaseBotView, generic.CreateView):
    model = Bot
    template_name = "bots/create.html"
    success_msg = _("Bot created")
    form_class = forms.BotCreateForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()  
        return HttpResponseRedirect(self.get_success_url())

class BotDeleteView(BaseBotView, generic.DeleteView):
    model = Bot
    template_name = 'bots/confirm_delete.html'
    success_msg = _("Bot deleted")
    
class BotUpdateView(BaseBotView, generic.UpdateView):
    model = Bot
    template_name = 'bots/edit.html'
    success_msg = _("Bot updated")
    form_class = forms.BotUpdateForm   
    
class BotDetailView(BaseBotView, generic.DetailView):
    model = Bot
    template_name = "bots/detail.html"
    super_class = generic.DetailView
    
    
class BaseWithBotView(LoginRequiredMixin):
    super_class = None
    success_msg = None
    sucess_url = None
    
    def get_kwargs(self):
        return {'bot_pk': self.kwargs['bot_pk']}
    
    def get_context_data(self, **kwargs):
        ctx = super(self.super_class, self).get_context_data(**kwargs)
        ctx['bot'] = Bot.objects.get(pk=self.kwargs['bot_pk'])
        return ctx
    
    def get_queryset(self):
        bot_pk = self.kwargs['bot_pk']
        return self.model.objects.filter(bot__pk=bot_pk, bot__owner=self.request.user)
    
    def get_success_url(self):
        messages.info(self.request, self.success_msg)
        return reverse_lazy(self.success_url, kwargs=self.get_kwargs())
    
    def form_invalid(self, form):
        messages.error(self.request, _("Please check your errors"))
        return super(self.super_class, self).form_invalid(form)


class TelegramBotCreateView(BaseWithBotView, generic.CreateView):
    model = TelegramBot
    template_name = "bots/telegram/create.html"
    super_class = generic.CreateView
    success_msg = _("Telegram Bot created")
    form_class = forms.TelegramBotCreateForm
    success_url = 'bot-detail'
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
    def get_form_kwargs(self):
        kwargs = super(TelegramBotCreateView, self).get_form_kwargs()
        kwargs['bot'] = Bot.objects.get(pk=self.kwargs['bot_pk'])
        return kwargs
       
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        try:
            obj.save()
        except:
            form.add_error('token', 'Telegram Error. Check Token or try later.')
            return self.form_invalid(form)
        else:
            bot = Bot.objects.get(pk=self.kwargs['bot_pk'])
            bot.telegram_bot = obj
            bot.save()
            return HttpResponseRedirect(self.get_success_url())

class TelegramBotDeleteView(BaseWithBotView, generic.DeleteView):
    model = TelegramBot
    template_name = 'bots/telegram/confirm_delete.html'
    success_msg = _("Telegram Bot deleted")
    super_class = generic.DeleteView
    success_url = 'bot-detail'
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
class TelegramBotUpdateView(BaseWithBotView, generic.UpdateView):
    model = TelegramBot
    template_name = 'bots/telegram/edit.html'
    success_msg = _("Telegram Bot updated")
    form_class = forms.TelegramBotUpdateForm   
    success_url = 'bot-detail'
    super_class = generic.UpdateView
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
class KikBotCreateView(BaseWithBotView, generic.CreateView):
    model = KikBot
    template_name = "bots/kik/create.html"
    super_class = generic.CreateView
    success_msg = _("Kik Bot created")
    form_class = forms.KikBotCreateForm
    success_url = 'bot-detail'
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
    def get_form_kwargs(self):
        kwargs = super(KikBotCreateView, self).get_form_kwargs()
        kwargs['bot'] = Bot.objects.get(pk=self.kwargs['bot_pk'])
        return kwargs
       
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        try:
            obj.save()
        except:
            form.add_error('username', 'Kik Error. Check Kik username or try later.')
            form.add_error('api_key', 'Kik Error. Check Kik API key or try later.')
            return self.form_invalid(form)
        else:
            bot = Bot.objects.get(pk=self.kwargs['bot_pk'])
            bot.kik_bot = obj
            bot.save()
            return HttpResponseRedirect(self.get_success_url())

class KikBotDeleteView(BaseWithBotView, generic.DeleteView):
    model = KikBot
    template_name = 'bots/kik/confirm_delete.html'
    success_msg = _("Kik Bot deleted")
    super_class = generic.DeleteView
    success_url = 'bot-detail'
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
class KikBotUpdateView(BaseWithBotView, generic.UpdateView):
    model = KikBot
    template_name = 'bots/kik/edit.html'
    success_msg = _("Kik Bot updated")
    form_class = forms.KikBotUpdateForm   
    success_url = 'bot-detail'
    super_class = generic.UpdateView
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}

class HandlerListView(BaseWithBotView, generic.ListView):
    model = Handler
    template_name = "bots/handlers/list.html" 
    super_class = generic.ListView

class HandlerCreateView(BaseWithBotView, generic.FormView):
    form_class = forms.HandlerCreationForm
    template_name = "bots/handlers/create.html"
    super_class = generic.FormView
    success_msg = _("Handler created")
    success_url = 'handler-list'
    
    def get_form_kwargs(self):
        kwargs = super(HandlerCreateView, self).get_form_kwargs()
        kwargs['bot'] = Bot.objects.get(pk=self.kwargs['bot_pk'])
        return kwargs
       
    def form_valid(self, form):
        obj = form.save(commit=False)
        bot_pk = self.kwargs['bot_pk']
        obj.bot = Bot.objects.get(pk=bot_pk)
        if 'url_template' and 'method'in form.cleaned_data and form.cleaned_data['url_template']: 
            
            obj.request = Request.objects.create(url_template=form.cleaned_data['url_template'],
                                                 method=form.cleaned_data['method'],
                                                 data=form.cleaned_data['data'])
        obj.response = Response.objects.create(text_template=form.cleaned_data['text_template'],
                                               keyboard_template=form.cleaned_data['keyboard_template'])
        obj.save()     
        
        return HttpResponseRedirect(self.get_success_url())
    
class HandlerDeleteView(BaseWithBotView, generic.DeleteView):
    model = Handler
    template_name = 'bots/handlers/confirm_delete.html'
    super_class = generic.DeleteView
    success_msg = _("Handler deleted")
    success_url = 'handler-list'
    
class HandlerUpdateView(BaseWithBotView, generic.FormView):
    
    template_name = 'bots/handlers/edit.html'
    form_class = forms.HandlerCreationForm
    super_class = generic.FormView
    success_msg = _("Handler updated")
    success_url = 'handler-list'   
    
    def get_context_data(self, **kwargs):
        ctx = super(HandlerUpdateView, self).get_context_data(**kwargs)
        ctx['object'] = Handler.objects.get(pk=self.kwargs['pk'])
        return ctx
    
    def get_form_kwargs(self):
        kwargs = super(HandlerUpdateView, self).get_form_kwargs()
        kwargs['bot'] = Bot.objects.get(pk=self.kwargs['bot_pk'])
        return kwargs

    def get_initial(self):
        handler = Handler.objects.get(pk=self.kwargs['pk'], 
                                      bot__pk=self.kwargs['bot_pk'], 
                                      bot__owner=self.request.user)

        initial = {'pattern': handler.pattern,
                   'enabled': handler.enabled,
                   'name': handler.name,
                   'priority': handler.priority,
                   'target_state': handler.target_state,
                   'source_states': handler.source_states.all(),
                   'text_template': handler.response.text_template,
                   'keyboard_template': handler.response.keyboard_template}
        if handler.request:
            initial.update({'method': handler.request.method,
                            'url_template': handler.request.url_template,
                            'data': handler.request.data, })
        else:
            initial.update({'method': Request.GET})
        return initial
    
    def get_object(self):
        try:
            return Handler.objects.get(pk=self.kwargs['pk'], bot__pk=self.kwargs['bot_pk'], bot__owner=self.request.user)
        except Handler.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': Handler._meta.verbose_name})
    
    def form_valid(self, form):
        self.object = self.get_object()
        self.object.pattern = form.cleaned_data['pattern']
        self.object.enabled = form.cleaned_data['enabled']
        self.object.name = form.cleaned_data['name']
        self.object.priority = form.cleaned_data['priority']
        self.object.target_state = form.cleaned_data['target_state']
        if not form.cleaned_data['url_template']:
            self.object.request = None
        else:
            if not self.object.request:
                self.object.request = Request.objects.create(url_template=form.cleaned_data['url_template'],
                                                             method=form.cleaned_data['method'],
                                                             data=form.cleaned_data['data'])
            else:
                request = self.object.request
                request.url_template = form.cleaned_data['url_template']
                request.method = form.cleaned_data['method']
                request.data = form.cleaned_data['data']
                request.save()
        
        response = self.object.response
        response.text_template = form.cleaned_data['text_template']
        response.keyboard_template = form.cleaned_data['keyboard_template']
        if not form.cleaned_data['source_states']:
            for state in self.object.source_states.all():
                self.object.source_states.remove(state)
        else:
            for state in form.cleaned_data['source_states']:
                self.object.source_states.add(state)
            
        response.save()
        self.object.save()     
        
        return HttpResponseRedirect(self.get_success_url())
    
class HandlerDetailView(BaseWithBotView, generic.DetailView):
    model = Handler
    template_name = "bots/handlers/detail.html"
    super_class = generic.DetailView
    
    
class HookListView(BaseWithBotView, generic.ListView):
    model = Hook
    template_name = "bots/hooks/list.html"
    super_class = generic.ListView
    
class HookCreateView(BaseWithBotView, generic.CreateView):
    form_class = forms.HookCreationForm
    template_name = "bots/hooks/create.html"
    super_class = generic.CreateView
    success_msg = _("Hook created")
    success_url = 'hook-list'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        bot_pk = self.kwargs['bot_pk']
        obj.bot = Bot.objects.get(pk=bot_pk)
        obj.response = Response.objects.create(text_template=form.cleaned_data['text_template'],
                                               keyboard_template=form.cleaned_data['keyboard_template'])
        obj.save()     
        return HttpResponseRedirect(self.get_success_url())
    
class HookDeleteView(BaseWithBotView, generic.DeleteView):
    model = Hook
    template_name = 'bots/hooks/confirm_delete.html'
    super_class = generic.DeleteView
    success_url = 'hook-list'
    success_msg = _("Hook deleted")
    
class HookUpdateView(BaseWithBotView, generic.FormView):

    template_name = 'bots/hooks/edit.html'
    form_class = forms.HookCreationForm
    super_class = generic.FormView
    success_msg = _("Hook updated")
    success_url = 'hook-list'
    
    def get_context_data(self, **kwargs):
        ctx = super(HookUpdateView, self).get_context_data(**kwargs)
        ctx['object'] = Hook.objects.get(pk=self.kwargs['pk'])
        return ctx
    
    def get_object(self):
        try:
            return Hook.objects.get(pk=self.kwargs['pk'], 
                                    bot__pk=self.kwargs['bot_pk'], 
                                    bot__owner=self.request.user)
        except Hook.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': Hook._meta.verbose_name})
    
    def get_initial(self):
        object = self.get_object()

        initial = {'enabled': object.enabled,
                   'name': object.name,
                   'text_template': object.response.text_template,
                   'keyboard_tempate': object.response.keyboard_template}
        return initial
    
    def form_valid(self, form):
        object = self.get_object()
        object.enabled = form.cleaned_data['enabled']
        
        response = object.response
        response.text_template = form.cleaned_data['text_template']
        response.keyboard_template = form.cleaned_data['keyboard_template']
        response.save()
        object.save()     
        
        return HttpResponseRedirect(self.get_success_url())
   
class HookDetailView(BaseWithBotView, generic.DetailView):
    model = Hook
    template_name = "bots/hooks/detail.html"
    super_class = generic.DetailView
    
class EnvironmentVarListView(BaseWithBotView, generic.ListView):
    model = EnvironmentVar
    template_name = "bots/env_vars/list.html"
    super_class = generic.ListView
    
class EnvironmentVarCreateView(BaseWithBotView, generic.CreateView):
    model = EnvironmentVar
    form_class = forms.EnvironmentVarForm
    template_name = "bots/env_vars/create.html"
    super_class = generic.CreateView
    success_msg = _("Environment Var created")
    success_url = 'bot-detail'

    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        bot_pk = self.kwargs['bot_pk']
        obj.bot = Bot.objects.get(pk=bot_pk)
        obj.save()     
        return HttpResponseRedirect(self.get_success_url())
    
class EnvironmentVarDeleteView(BaseWithBotView, generic.DeleteView):
    model = EnvironmentVar
    template_name = 'bots/env_vars/confirm_delete.html'
    super_class = generic.DeleteView
    success_url = 'bot-detail'
    success_msg = _("Environment Variable deleted")
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
class EnvironmentVarUpdateView(BaseWithBotView, generic.UpdateView):
    model = EnvironmentVar
    template_name = 'bots/env_vars/edit.html'
    form_class = forms.EnvironmentVarForm
    super_class = generic.UpdateView
    success_url = 'bot-detail'
    success_msg = _("Environment Variable updated")
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
class EnvironmentVarDetailView(BaseWithBotView, generic.DetailView):
    model = EnvironmentVar
    template_name = "bots/env_vars/detail.html"
    super_class = generic.DetailView
    
    
class BaseWithHandlerBotView(BaseWithBotView):
    super_class = None
    success_msg = None
    sucess_url = None
    
    def get_context_data(self, **kwargs):
        ctx = super(BaseWithHandlerBotView, self).get_context_data(**kwargs)
        ctx['handler'] = Handler.objects.get(pk=self.kwargs['handler_pk'])
        return ctx
    
    def get_queryset(self):
        bot_pk = self.kwargs['bot_pk']
        handler_pk = self.kwargs['handler_pk']
        return self.model.objects.filter(request__handler__bot__pk=bot_pk, 
                                         request__handler__bot__owner=self.request.user, 
                                         request__handler__pk=handler_pk)
    
    def get_success_url(self):
        messages.info(self.request, self.success_msg)
        return reverse_lazy(self.success_url, kwargs={'bot_pk': self.kwargs['bot_pk'],
                                                      'pk': self.kwargs['handler_pk']})
        
class UrlParameterCreateView(BaseWithHandlerBotView, generic.CreateView):
    model = UrlParam
    form_class = forms.UrlParameterForm
    template_name = "bots/handlers/urlparameters/create.html"
    super_class = generic.CreateView
    success_msg = _("Url parameter created")
    success_url = 'handler-detail'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        handler_pk = self.kwargs['handler_pk']
        handler = Handler.objects.get(pk=handler_pk)
        if handler.request:
            obj.request = Handler.objects.get(pk=handler_pk).request
            obj.save()     
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, _('No request for this handler'))
            return reverse_lazy(self.success_url, kwargs={'bot_pk': self.kwargs['bot_pk'],
                                                          'pk': self.kwargs['handler_pk']})            
    
class UrlParameterDeleteView(BaseWithHandlerBotView, generic.DeleteView):
    model = UrlParam
    template_name = 'bots/handlers/urlparameters/confirm_delete.html'
    super_class = generic.DeleteView
    success_url = 'handler-detail'
    success_msg = _("Url Parameter deleted")
    
class UrlParameterUpdateView(BaseWithHandlerBotView, generic.UpdateView):
    model = UrlParam
    template_name = 'bots/handlers/urlparameters/edit.html'
    form_class = forms.UrlParameterForm
    super_class = generic.UpdateView
    success_url = 'handler-detail'
    success_msg = _("Url Parameter updated")
    
    
class HeaderParameterCreateView(BaseWithHandlerBotView, generic.CreateView):
    model = HeaderParam
    form_class = forms.HeaderParameterForm
    template_name = "bots/handlers/headerparameters/create.html"
    super_class = generic.CreateView
    success_msg = _("Header Parameter created")
    success_url = 'handler-detail'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        handler_pk = self.kwargs['handler_pk']
        handler = Handler.objects.get(pk=handler_pk)
        if handler.request:
            obj.request = Handler.objects.get(pk=handler_pk).request
            obj.save()     
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, _('No request for this handler'))
            return reverse_lazy(self.success_url, kwargs={'bot_pk': self.kwargs['bot_pk'],
                                                          'pk': self.kwargs['handler_pk']}) 
    
class HeaderParameterDeleteView(BaseWithHandlerBotView, generic.DeleteView):
    model = HeaderParam
    template_name = 'bots/handlers/headerparameters/confirm_delete.html'
    super_class = generic.DeleteView
    success_url = 'handler-detail'
    success_msg = _("Header Parameter deleted")
    
class HeaderParameterUpdateView(BaseWithHandlerBotView, generic.UpdateView):
    model = HeaderParam
    template_name = 'bots/handlers/headerparameters/edit.html'
    form_class = forms.HeaderParameterForm
    super_class = generic.UpdateView
    success_url = 'handler-detail'
    success_msg = _("Header Parameter updated")   
    
    
class BaseWithHookBotView(BaseWithBotView):
    super_class = None
    success_msg = None
    sucess_url = None
    
    def get_context_data(self, **kwargs):
        ctx = super(BaseWithHookBotView, self).get_context_data(**kwargs)
        ctx['hook'] = Hook.objects.get(pk=self.kwargs['hook_pk'])
        return ctx
    
    def get_queryset(self):
        bot_pk = self.kwargs['bot_pk']
        hook_pk = self.kwargs['hook_pk']
        return self.model.objects.filter(hook__bot__pk=bot_pk, 
                                         hook__bot__owner=self.request.user, 
                                         hook__pk=hook_pk)
    
    def get_success_url(self):
        messages.info(self.request, self.success_msg)
        return reverse_lazy(self.success_url, kwargs={'bot_pk': self.kwargs['bot_pk'],
                                                      'pk': self.kwargs['hook_pk']})


class TelegramRecipientCreateView(BaseWithHookBotView, generic.CreateView):
    model = TelegramRecipient
    form_class = forms.TelegramRecipientForm
    template_name = "bots/hooks/recipients/telegram/create.html"
    super_class = generic.CreateView
    success_msg = _("Hook Telegram Recipient created")
    success_url = 'hook-detail'
    
    def form_invalid(self, form):
        return super(TelegramRecipientCreateView, self).form_invalid(form)
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        hook_pk = self.kwargs['hook_pk']
        obj.hook = Hook.objects.get(pk=hook_pk)
        obj.save()     
        return HttpResponseRedirect(self.get_success_url())
    
class TelegramRecipientDeleteView(BaseWithHookBotView, generic.DeleteView):
    model = TelegramRecipient
    template_name = 'bots/hooks/recipients/telegram/confirm_delete.html'
    super_class = generic.DeleteView
    success_url = 'hook-detail'
    success_msg = _("Hook Telegram Recipient deleted")
    
class TelegramRecipientUpdateView(BaseWithHookBotView, generic.UpdateView):
    model = TelegramRecipient
    template_name = 'bots/hooks/recipients/telegram/edit.html'
    form_class = forms.TelegramRecipientForm
    super_class = generic.UpdateView
    success_url = 'hook-detail'
    success_msg = _("Hook Telegram Recipient updated")
    
    
class KikRecipientCreateView(BaseWithHookBotView, generic.CreateView):
    model = KikRecipient
    form_class = forms.KikRecipientForm
    template_name = "bots/hooks/recipients/kik/create.html"
    super_class = generic.CreateView
    success_msg = _("Hook Kik Recipient created")
    success_url = 'hook-detail'
    
    def form_invalid(self, form):
        return super(KikRecipientCreateView, self).form_invalid(form)
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        hook_pk = self.kwargs['hook_pk']
        obj.hook = Hook.objects.get(pk=hook_pk)
        obj.save()     
        return HttpResponseRedirect(self.get_success_url())
    
class KikRecipientDeleteView(BaseWithHookBotView, generic.DeleteView):
    model = KikRecipient
    template_name = 'bots/hooks/recipients/kik/confirm_delete.html'
    super_class = generic.DeleteView
    success_url = 'hook-detail'
    success_msg = _("Hook Kik Recipient deleted")
    
class KikRecipientUpdateView(BaseWithHookBotView, generic.UpdateView):
    model = KikRecipient
    template_name = 'bots/hooks/recipients/kik/edit.html'
    form_class = forms.KikRecipientForm
    super_class = generic.UpdateView
    success_url = 'hook-detail'
    success_msg = _("Hook Kik Recipient updated")
    
class StateCreateView(BaseWithBotView, generic.CreateView):
    model = State
    form_class = forms.StateForm
    template_name = "bots/states/create.html"
    super_class = generic.CreateView
    success_msg = _("State created")
    success_url = 'bot-detail'
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        bot_pk = self.kwargs['bot_pk']
        obj.bot = Bot.objects.get(pk=bot_pk)
        obj.save()     
        return HttpResponseRedirect(self.get_success_url())
    
class StateDeleteView(BaseWithBotView, generic.DeleteView):
    model = State
    template_name = 'bots/states/confirm_delete.html'
    super_class = generic.DeleteView
    success_url = 'bot-detail'
    success_msg = _("State deleted")
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}
    
class StateUpdateView(BaseWithBotView, generic.UpdateView):
    model = State
    template_name = 'bots/states/edit.html'
    form_class = forms.StateForm
    super_class = generic.UpdateView
    success_url = 'bot-detail'
    success_msg = _("State updated")
    
    def get_kwargs(self):
        return {'pk': self.kwargs['bot_pk']}