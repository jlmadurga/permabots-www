from django import forms
from permabots.models import (Bot, Handler, Hook, Request, EnvironmentVar, UrlParam, HeaderParam, TelegramRecipient, 
                              State, TelegramBot, KikBot, KikRecipient, MessengerBot, MessengerRecipient)
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, HTML
from permabots import validators


class BaseCrispyForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BaseCrispyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False      

class BotCreateForm(BaseCrispyForm):
    
    class Meta:
        model = Bot
        fields = ('name', )
        
class BotUpdateForm(BaseCrispyForm):
       
    class Meta:
        model = Bot
        fields = ('name', )


class TelegramBotCreateForm(BaseCrispyForm):
    enabled = forms.BooleanField(label="", required=False)
     
    class Meta:
        model = TelegramBot
        fields = ('token', 'enabled')
        
    def __init__(self, *args, **kwargs):
        bot = kwargs.pop("bot")  # noqa
        super(TelegramBotCreateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('enabled', css_class="bt-switch", data_on_color="success", data_off_color="danger"),
            Field('token', placeholder="telegram token"),
        )
        
class TelegramBotUpdateForm(BaseCrispyForm):
    enabled = forms.BooleanField(label="", required=False)
        
    class Meta:
        model = Bot
        fields = ('enabled', )
        
    def __init__(self, *args, **kwargs):
        super(TelegramBotUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('enabled', css_class="bt-switch", data_on_color="success", data_off_color="danger"),
        )

class KikBotCreateForm(BaseCrispyForm):
    enabled = forms.BooleanField(label="", required=False)
     
    class Meta:
        model = KikBot
        fields = ('username', 'api_key', 'enabled')
        
    def __init__(self, *args, **kwargs):
        bot = kwargs.pop("bot")  # noqa
        super(KikBotCreateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('enabled', css_class="bt-switch", data_on_color="success", data_off_color="danger"),
            Field('username', placeholder="kik username"),
            Field('api_key', placeholder="kik api_key"),
        )
        
class KikBotUpdateForm(BaseCrispyForm):
    enabled = forms.BooleanField(label="", required=False)
        
    class Meta:
        model = Bot
        fields = ('enabled', )
        
    def __init__(self, *args, **kwargs):
        super(KikBotUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('enabled', css_class="bt-switch", data_on_color="success", data_off_color="danger"),
        )

class MessengerBotCreateForm(BaseCrispyForm):
    enabled = forms.BooleanField(label="", required=False)
     
    class Meta:
        model = MessengerBot
        fields = ('token', 'enabled')
        
    def __init__(self, *args, **kwargs):
        bot = kwargs.pop("bot")  # noqa
        super(MessengerBotCreateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('enabled', css_class="bt-switch", data_on_color="success", data_off_color="danger"),
            Field('token', placeholder="facebook messenger token"),
        )
        
class MessengerBotUpdateForm(BaseCrispyForm):
    enabled = forms.BooleanField(label="", required=False)
        
    class Meta:
        model = Bot
        fields = ('enabled', )
        
    def __init__(self, *args, **kwargs):
        super(MessengerBotUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('enabled', css_class="bt-switch", data_on_color="success", data_off_color="danger"),
        )

class HandlerCreationForm(BaseCrispyForm):
    name = forms.CharField(label=_("Name"))
    pattern = forms.CharField(label=_("Pattern"), validators=[validators.validate_pattern],
                              help_text=_('''Handler matches a <a href="https://docs.python.org/2/library/re.html#regular-expression-syntax">
                              regular expression syntax</a>''')
                              ) 
    url_template = forms.CharField(label=_("Url template"), required=False,
                                   validators=[validators.validate_template],
                                   help_text='''In <a href="http://jinja.pocoo.org/">jinja2</a> format. Context: <code>pattern</code>, 
                                            <code>env</code>, <code>message</code>, <code>state_context</code>.''')
    method = forms.ChoiceField(label=_("Method"), widget=forms.RadioSelect, choices=Request.METHOD_CHOICES, required=False)
    data = forms.CharField(label=_("Data"), required=False, widget=forms.Textarea,
                           help_text=_('''Define JSON template. In <a href="http://jinja.pocoo.org/">jinja2</a> format. Context: 
                                       <code>pattern</code>,<code>env</code>, <code>message</code>, <code>state_context</code>.'''))
    text_template = forms.CharField(label=_("Text template"), widget=forms.Textarea,
                                    validators=[validators.validate_template, validators.validate_telegram_text_html],
                                    help_text=_('''Text template. In <a href="http://jinja.pocoo.org/">jinja2</a> format. 
                                                Context: <code>pattern</code>,<code>env</code>, <code>message</code>, 
                                                <code>state_context</code>, <code>response</code>, <code>emoji</code>.''')
                                    )
    keyboard_template = forms.CharField(label=_("Keyboard template"), widget=forms.Textarea, required=False,
                                        validators=[validators.validate_template, validators.validate_telegram_keyboard],
                                        help_text=_('''<a href="https://core.telegram.org/bots/api#replykeyboardmarkup">Telegram keyboard</a> template. 
                                                    In <a href="http://jinja.pocoo.org/">jinja2</a> format. 
                                                    Context: <code>pattern</code>,<code>env</code>, <code>message</code>, <code>state_context</code>, 
                                                    <code>response</code>, <code>emoji</code>.'''))
    source_states = forms.ModelMultipleChoiceField(queryset=State.objects.all(), required=False,
                                                   help_text=_("In one of these states to execute"))
    enabled = forms.BooleanField(label="", required=False)
      
    class Meta:
        model = Handler
        fields = ('name', 'pattern', 'enabled', 'target_state', 'priority')
                
    def __init__(self, *args, **kwargs):
        bot = kwargs.pop("bot")
        super(HandlerCreationForm, self).__init__(*args, **kwargs)
        self.fields["source_states"].queryset = State.objects.filter(bot=bot)
        self.fields['target_state'].queryset = State.objects.filter(bot=bot)
        self.helper.layout = Layout(
            HTML('''<div id="processTabs">
                        <ul class="process-steps bottommargin clearfix">
                            <li>
                                <a href="#pattern" class="i-circled i-bordered i-alt divcenter">1</a>
                                <h5>Pattern</h5>
                            </li>
                            <li>
                                <a href="#request" class="i-circled i-bordered i-alt divcenter">2</a>
                                <h5>Request</h5>
                            </li>
                            <li>
                                <a href="#response" class="i-circled i-bordered i-alt divcenter">3</a>
                                <h5>Response</h5>
                            </li>
                         </ul>
                    <div>'''),
            HTML('<div id="pattern">'),
            Fieldset(
                'Info',
                Field('enabled', css_class="bt-switch", data_on_color="success", data_off_color="danger"),
                Field('name', placeholder="my handler name"),
                css_class="col-sm-4" 
            ),
            Fieldset(
                'Pattern',
                Field('pattern', placeholder="(?P<username>\w+)"),
                Field('priority'),
                css_class="col-sm-4" 
            ),
            Fieldset(
                'States',
                Field('source_states', css_class="select-tags"),
                Field('target_state', css_class="selectpicker", data_live_search="true"),
                css_class="col-sm-4"
            ),
            HTML('<a href="#" class="button button-small button-border button-rounded fright tab-linker" rel="2">Next</a></div><div id="request">'),
            Fieldset(
                'Request',
                Field('url_template', placeholder='https://api.github.com/users/{{pattern.username}}'),
                Field('method'),
                css_class="col-sm-4"
            ),
            Fieldset(
                'Data',
                Field('data', placeholder='''{"context_pattern": "{{ pattern.name }}", "context_env": "{{env.description}}", 
                    "homepage": "https://github.com","private": false, "has_issues": true, "has_wiki": true, "has_downloads": true}'''),
                css_class="col-sm-8"
            ),
            HTML('<a href="#" class="button button-small button-border button-rounded fright tab-linker" rel="3">Next</a></div><div id="response">'),
            Fieldset(
                'Response',
                Field('text_template', placeholder='''For example you can loop a list from context: 
                    {% for repository in response.data %}<b>{{ respository.name }}</b>{% endfor %}
                    Or check request status {{ response.status }} or anything in context {{env.variable}}'''),
                Field('keyboard_template', placeholder='[["{{response.data.menu1}}"],["menu2"]]'),
                css_class="col-sm-12"                         
            )
        )
    
    def clean(self):
        cleaned_data = super(HandlerCreationForm, self).clean()
        url_template = self.cleaned_data.get('url_template', None)
        if url_template and not self.cleaned_data['method']:
            self.cleaned_data['method'] = Request.GET
        return cleaned_data
        
        
class HookCreationForm(BaseCrispyForm):
    enabled = forms.BooleanField(label="", required=False)
    text_template = forms.CharField(label=_("Text template"), widget=forms.Textarea,
                                    validators=[validators.validate_template, validators.validate_telegram_text_html],
                                    help_text=_('''Text template. In <a href="http://jinja.pocoo.org/">jinja2</a> format. 
                                                Context: <code>env</code>, <code>data</code>, <code>emoji</code>.'''))
    keyboard_template = forms.CharField(label=_("Keyboard template"), widget=forms.Textarea, required=False,
                                        validators=[validators.validate_template, validators.validate_telegram_keyboard],
                                        help_text=_('''<a href="https://core.telegram.org/bots/api#replykeyboardmarkup">Telegram keyboard</a> template. 
                                                    In <a href="http://jinja.pocoo.org/">jinja2</a> format. Context: <code>env</code>, <code>data</code>, 
                                                    <code>emoji</code>.'''))

    class Meta:
        model = Hook
        fields = ('name', 'enabled', )
        
    def __init__(self, *args, **kwargs):
        super(HookCreationForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                'Info',
                Field('enabled', css_class="bt-switch", data_on_color="success", data_off_color="danger"),
                Field('name', placeholder="my hook name"),
                css_class="col-sm-3"
            ),
            Fieldset(
                'Response',
                Field('text_template', placeholder='''For example you can loop a list from context: 
                    {% for repository in data %}<b>{{ respository.name }}</b>{% endfor %}
                    Or anything in context {{env.variable}}'''),
                Field('keyboard_template', placeholder='[["{{data.menu_1}}"],["menu2"]]'),
                css_class="col-sm-9",                       
            ),
        )
        
class EnvironmentVarForm(BaseCrispyForm):
    
    class Meta:
        model = EnvironmentVar
        fields = ('key', 'value')
        
class UrlParameterForm(BaseCrispyForm):   

    class Meta:
        model = UrlParam
        fields = ('key', 'value_template')
        
class HeaderParameterForm(BaseCrispyForm):
    
    class Meta:
        model = HeaderParam
        fields = ('key', 'value_template')
        
class TelegramRecipientForm(BaseCrispyForm):
    
    class Meta:
        model = TelegramRecipient
        fields = ('name', 'chat_id')   

class KikRecipientForm(BaseCrispyForm):
    
    class Meta:
        model = KikRecipient
        fields = ('name', 'chat_id', 'username')     

class MessengerRecipientForm(BaseCrispyForm):
    
    class Meta:
        model = MessengerRecipient
        fields = ('name', 'chat_id')     

class StateForm(BaseCrispyForm):
    
    class Meta:
        model = State
        fields = ('name',)
