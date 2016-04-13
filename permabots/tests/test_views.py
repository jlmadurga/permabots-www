from django.test import RequestFactory
from test_plus.test import TestCase
from microbot.test.factories import BotFactory, HandlerFactory, HookFactory, UrlParamFactory, \
    HeaderParamFactory, RecipientFactory, StateFactory
from microbot.models import EnvironmentVar, Bot, Handler, Hook, UrlParam, HeaderParam, Recipient, State
from microbot.models import User as UserAPI
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django_webtest import WebTest
from django.contrib.auth import get_user_model

try:
    from unittest import mock
except ImportError:
    import mock  # noqa
User = get_user_model()

@override_settings(LOGIN_URL=reverse('account_login'))
class BaseBotTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()
        self.bot = BotFactory(owner=self.user)     
    
    def assertRedirectsLogin(self, response):
        self.assertRedirects(response, reverse('account_login')+'?next=' + self.url(), 302, 200)   
        
class BaseListView(BaseBotTestCase):
    url_name = None
    url_kwargs = {}
    
    def url(self):
        return reverse(self.url_name, kwargs=self.url_kwargs)
    
    def assertObject(self, obj):
        raise NotImplementedError        
    
    def _test_not_auth_redirected(self, **kwargs):
        self.assertLoginRequired(self.url_name, **self.url_kwargs)
        
    def _test_list_ok(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 200)
        objects = response.context['object_list']
        self.assertEqual(1, len(objects))
        self.assertObject(objects[0])
        
    def _test_list_empty(self):
        other_user = self.make_user('other')
        self.client.force_login(other_user)
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 200)
        objects = response.context['object_list']
        self.assertEqual(0, len(objects))

class TestBotListView(BaseListView):
    url_name = 'bot-list'

    def setUp(self):
        super(TestBotListView, self).setUp()
        self.object = self.bot
    
    def assertObject(self, obj):
        self.assertEqual(self.object.token, obj.token)

    def test_not_auth_redirected(self):
        self._test_not_auth_redirected()
        
    def test_list_ok(self):
        self._test_list_ok()
        
    def test_list_empty(self):
        self._test_list_empty()
        
class TestHandlersListView(BaseListView):
    url_name = 'handler-list'
    
    def setUp(self):
        super(TestHandlersListView, self).setUp()
        self.object = HandlerFactory(bot=self.bot)
        self.url_kwargs = {'bot_pk': self.bot.pk}
    
    def assertObject(self, obj):
        self.assertEqual(self.object.pattern, obj.pattern)
        self.assertEqual(self.object.name, obj.name)

    def test_not_auth_redirected(self):
        self._test_not_auth_redirected()
        
    def test_list_ok(self):
        self._test_list_ok()
        
    def test_list_empty(self):
        self._test_list_empty()
        
class TestHookListView(BaseListView):
    url_name = 'hook-list'
    
    def setUp(self):
        super(TestHookListView, self).setUp()
        self.object = HookFactory(bot=self.bot)
        self.url_kwargs = {'bot_pk': self.bot.pk}
    
    def assertObject(self, obj):
        self.assertEqual(self.object.key, obj.key)
        self.assertEqual(self.object.name, obj.name)

    def test_not_auth_redirected(self):
        self._test_not_auth_redirected()
        
    def test_list_ok(self):
        self._test_list_ok()
        
    def test_list_empty(self):
        self._test_list_empty()
        
class TestEnvListView(BaseListView):
    url_name = 'env-list'
    
    def setUp(self):
        super(TestEnvListView, self).setUp()
        self.object = EnvironmentVar.objects.create(bot=self.bot,
                                                    key='key', 
                                                    value='value')
        self.url_kwargs = {'bot_pk': self.bot.pk}
    
    def assertObject(self, obj):
        self.assertEqual(self.object.key, obj.key)
        self.assertEqual(self.object.value, obj.value)

    def test_not_auth_redirected(self):
        self._test_not_auth_redirected()
        
    def test_list_ok(self):
        self._test_list_ok()
        
    def test_list_empty(self):
        self._test_list_empty()
        
class BaseManageTest(WebTest):
    url_name_create = None
    url_kwargs_create = {}
    url_name_delete = None
    url_kwargs_delete = {}
    url_name_update = None
    url_kwargs_update = {}
    model = None
    
    def setUp(self):
        self.user = self.create_user()
        with mock.patch("telegram.bot.Bot.setWebhook", callable=mock.MagicMock()):
            with mock.patch("telegram.bot.Bot.getMe", callable=mock.MagicMock()) as mock_get_me:
                user_dict = {'username': u'Microbot_test_bot', 'first_name': u'Microbot_test', 'id': 204840063}
                mock_get_me.return_value = UserAPI(**user_dict)
                self.bot = BotFactory(owner=self.user)
        
    def create_user(self, username="username", password="password"):
        test_user = User.objects.create_user(username,
                                             '{0}@example.com'.format(username),
                                             password,
                                             )
        return test_user  
               
    def url_create(self):
        return reverse(self.url_name_create, kwargs=self.url_kwargs_create)
    
    def url_delete(self):
        return reverse(self.url_name_delete, kwargs=self.url_kwargs_delete)
    
    def url_update(self):
        return reverse(self.url_name_update, kwargs=self.url_kwargs_update)
    
    def fill_form(self, form, create=False):
        raise NotImplemented
    
    def assertObject(self, obj):
        raise NotImplementedError
    
    def get_form(self, page, name=None):
        if name:
            return page.forms[name]
        return page.forms[0]
    
    def assertCreation(self, response):
        self.assertEqual(1, self.model.objects.count())
        self.assertObject(self.model.objects.all()[0])
        
    def assertDeletion(self, response):
        self.assertEqual(0, self.model.objects.count())
        
    def assertUpdate(self, response):
        self.assertEqual(1, self.model.objects.count())
        self.assertObject(self.model.objects.all()[0])
    
    def _test_create_ok(self):
        create_page = self.app.get(self.url_create(), user=self.user)
        form = self.get_form(create_page)
        self.fill_form(form, create=True)
        response = form.submit().follow()
        self.assertEqual(response.status_code, 200)
        self.assertCreation(response)
        
    def _test_create_validation_error(self, error):
        create_page = self.app.get(self.url_create(), user=self.user)
        form = self.get_form(create_page)
        self.fill_form(form, create=True)
        response = form.submit()
        self.assertEqual(response.status_code, 200)
        self.assertIn(error, response)    
        
    def _test_not_auth_create_redirected(self):
        response = self.app.get(self.url_create())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('account_login')+'?next=' + self.url_create())
        
    def _test_delete_ok(self):
        deletion_page = self.app.get(self.url_delete(), user=self.user)
        form = self.get_form(deletion_page)
        response = form.submit().follow()
        self.assertEqual(response.status_code, 200)
        self.assertDeletion(response)
        
    def _test_not_auth_delete_redirected(self):
        response = self.app.get(self.url_delete())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('account_login')+'?next=' + self.url_delete())
                
    def _test_update_ok(self):
        update_page = self.app.get(self.url_update(), user=self.user)
        form = self.get_form(update_page)
        self.fill_form(form)
        response = form.submit().follow()
        self.assertEqual(response.status_code, 200)
        self.assertUpdate(response)
                
    def _test_update_validation_error(self, error):
        update_page = self.app.get(self.url_update(), user=self.user)
        form = self.get_form(update_page)
        self.fill_form(form)
        response = form.submit()
        self.assertEqual(response.status_code, 200)
        self.assertIn(error, response)    
        
    def _test_not_auth_update_redirected(self):
        response = self.app.get(self.url_update())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('account_login')+'?next=' + self.url_update())       

        
class TestManageBot(BaseManageTest):
    url_name_create = 'bot-create'
    url_name_delete = 'bot-delete'
    url_name_update = 'bot-update'
    model = Bot
    
    def setUp(self):
        super(TestManageBot, self).setUp()
        self.url_kwargs_delete = {'pk': self.bot.pk}
        self.url_kwargs_update = {'pk': self.bot.pk}
        
    def fill_form(self, form, create=False):
        if create:
            form['token'] = self.bot.token
        form['enabled'] = self.bot.enabled
        
    def assertObject(self, obj):
        self.assertEqual(self.bot.token, obj.token)
    
    def test_create_ok(self):
        self.bot.delete()
        self.assertEqual(0, Bot.objects.count())
        self._test_create_ok()
        
    def test_not_auth_create_redirected(self):
        self._test_not_auth_create_redirected()
        
    def test_delete_ok(self):
        self._test_delete_ok()
        
    def test_not_auth_delete_redirected(self):
        self._test_not_auth_delete_redirected()
        
    def test_update_ok(self):
        self.bot.enabled = False
        self._test_update_ok()
        
    def test_not_auth_update_redirected(self):
        self._test_not_auth_update_redirected()
        
class TestManageEnvVar(BaseManageTest):
    model = EnvironmentVar
    url_name_create = 'env-create'
    url_name_delete = 'env-delete'
    url_name_update = 'env-update'
    
    def setUp(self):
        super(TestManageEnvVar, self).setUp()
        self.url_kwargs_create = {'bot_pk': self.bot.pk}
        self.envvar = EnvironmentVar.objects.create(bot=self.bot,
                                                    key='key', 
                                                    value='value')
        self.url_kwargs_delete = self.url_kwargs_update = {'bot_pk': self.bot.pk,
                                                           'pk': self.envvar.pk}
        
    def fill_form(self, form, create=False):
        form['key'] = 'key'
        form['value'] = 'value'
        
    def assertObject(self, obj):
        self.assertEqual(obj.key, 'key')
        self.assertEqual(obj.value, 'value')
        self.assertEqual(obj.bot, self.bot)        
        
    def test_create_ok(self):
        self.envvar.delete()
        self._test_create_ok()
        
    def test_not_auth_create_redirected(self):
        self._test_not_auth_create_redirected()
        
    def test_delete_ok(self):
        self._test_delete_ok()
        
    def test_not_auth_delete_redirected(self):
        self._test_not_auth_delete_redirected()
        
    def test_update_ok(self):
        self.envvar.value = 'newvalue'
        self._test_update_ok()
        
    def test_not_auth_update_redirected(self):
        self._test_not_auth_update_redirected()
        
class TestManageHandler(BaseManageTest):
    model = Handler
    url_name_create = 'handler-create'
    url_name_delete = 'handler-delete'
    url_name_update = 'handler-update'
    
    def setUp(self):
        super(TestManageHandler, self).setUp()
        self.url_kwargs_create = {'bot_pk': self.bot.pk}
        self.handler = HandlerFactory(bot=self.bot)
        self.state = StateFactory(bot=self.bot,
                                  name='name1')
        self.handler.target_state = self.state
        self.handler.save()
        self.handler.source_states.add(self.state)
        self.source_states = self.handler.source_states.all()
        self.url_kwargs_delete = self.url_kwargs_update = {'bot_pk': self.bot.pk,
                                                           'pk': self.handler.pk}  
        
    def fill_form(self, form, create=False):
        form['name'] = self.handler.name
        form['pattern'] = self.handler.pattern
        form['enabled'] = self.handler.enabled
        form['url_template'] = self.handler.request.url_template        
        form['method'] = self.handler.request.method
        form['data'] = self.handler.request.data
        form['priority'] = self.handler.priority
        form['text_template'] = self.handler.response.text_template
        form['keyboard_template'] = self.handler.response.keyboard_template
        form['target_state'] = self.handler.target_state.id
        form['source_states'] = [state.id for state in self.source_states]
        
    def assertObject(self, obj):
        self.assertEqual(obj.bot, self.bot)
        self.assertEqual(obj.name, self.handler.name)
        self.assertEqual(obj.pattern, self.handler.pattern)
        self.assertEqual(obj.enabled, self.handler.enabled)
        self.assertEqual(obj.priority, self.handler.priority)
        self.assertEqual(obj.request.method, self.handler.request.method)
        self.assertEqual(obj.request.url_template, self.handler.request.url_template)
        self.assertEqual(obj.target_state, self.handler.target_state)
        self.assertEqual(obj.source_states.count(), len(self.source_states))
        for state in self.source_states:
            obj.source_states.get(name=state.name)
        
    def test_create_ok(self):
        self.handler.delete()
        self._test_create_ok()
        
    def test_create_validation_error_pattern(self):
        self.handler.delete()
        self.handler.pattern = '(?P<username>\w+'
        self._test_create_validation_error('Not correct Regex')
        
    def test_create_validation_error_text_template(self):
        self.handler.delete()
        self.handler.response.text_template = '<b>{{a}}'
        self._test_create_validation_error('Not correct')
        
    def test_create_validation_error_keyboard_template(self):
        self.handler.delete()
        self.handler.response.keyboard_template = '[["{{a}","asd"]]'
        self._test_create_validation_error('Not correct')
               
    def test_not_auth_create_redirected(self):
        self._test_not_auth_create_redirected()
        
    def test_delete_ok(self):
        self._test_delete_ok()
        
    def test_not_auth_delete_redirected(self):
        self._test_not_auth_delete_redirected()
        
    def test_update_ok(self):
        self.handler.enabled = False
        self._test_update_ok()
        
    def test_update_validation_error_pattern(self):
        self.handler.pattern = '(?P<username>\w+'
        self._test_update_validation_error('Not correct Regex')
        
    def test_update_validation_error_text_template(self):
        self.handler.response.text_template = '<b>{{a}}'
        self._test_update_validation_error('Not correct')
        
    def test_update_validation_error_keyboard_template(self):
        self.handler.response.keyboard_template = '[["{{a}","asd"]]'
        self._test_update_validation_error('Not correct')
               
    def test_not_auth_update_redirected(self):
        self._test_not_auth_update_redirected()
        
        
class TestManageHook(BaseManageTest):
    model = Hook
    url_name_create = 'hook-create'
    url_name_delete = 'hook-delete'
    url_name_update = 'hook-update'
    
    def setUp(self):
        super(TestManageHook, self).setUp()
        self.url_kwargs_create = {'bot_pk': self.bot.pk}
        self.hook = HookFactory(bot=self.bot)
        self.url_kwargs_delete = self.url_kwargs_update = {'bot_pk': self.bot.pk,
                                                           'pk': self.hook.pk}        
        
    def fill_form(self, form, create=False):
        form['name'] = self.hook.name
        form['enabled'] = self.hook.enabled
        form['text_template'] = self.hook.response.text_template
        form['keyboard_template'] = self.hook.response.keyboard_template
        
    def assertObject(self, obj):
        self.assertEqual(obj.bot, self.bot)
        self.assertEqual(obj.name, self.hook.name)
        self.assertEqual(obj.enabled, self.hook.enabled)
        self.assertEqual(obj.response.text_template, self.hook.response.text_template)  
        self.assertEqual(obj.response.keyboard_template, self.hook.response.keyboard_template)  
        
    def test_create_ok(self):
        self.hook.delete()
        self._test_create_ok()
        
    def test_create_validation_error_text_template(self):
        self.hook.delete()
        self.hook.response.text_template = '<b>{{a}}'
        self._test_create_validation_error('Not correct')
        
    def test_create_validation_error_keyboard_template(self):
        self.hook.delete()
        self.hook.response.keyboard_template = '[["{{a}","asd"]]'
        self._test_create_validation_error('Not correct')
        
    def test_not_auth_create_redirected(self):
        self._test_not_auth_create_redirected()

    def test_delete_ok(self):
        self._test_delete_ok()
        
    def test_not_auth_delete_redirected(self):
        self._test_not_auth_delete_redirected()
        
    def test_update_ok(self):
        self.hook.enabled = False
        self._test_update_ok()
        
    def test_update_validation_error_text_template(self):
        self.hook.response.text_template = '<b>{{a}}'
        self._test_update_validation_error('Not correct')
        
    def test_update_validation_error_keyboard_template(self):
        self.hook.response.keyboard_template = '[["{{a}","asd"]]'
        self._test_update_validation_error('Not correct')
        
    def test_not_auth_update_redirected(self):
        self._test_not_auth_update_redirected()
        
        
class TestManageHandlerUrlParam(BaseManageTest):
    model = UrlParam
    url_name_create = 'handler-urlparameter-create'
    url_name_delete = 'handler-urlparameter-delete'
    url_name_update = 'handler-urlparameter-update'
    
    def setUp(self):
        super(TestManageHandlerUrlParam, self).setUp()
        self.handler = HandlerFactory(bot=self.bot)
        self.url_kwargs_create = {'bot_pk': self.bot.pk,
                                  'handler_pk': self.handler.pk}
        self.url_param = UrlParamFactory(request=self.handler.request)
        self.url_kwargs_delete = self.url_kwargs_update = {'bot_pk': self.bot.pk,
                                                           'handler_pk': self.handler.pk,
                                                           'pk': self.url_param.pk}  
        
    def fill_form(self, form, create=False):
        form['key'] = self.url_param.key
        form['value_template'] = self.url_param.value_template
               
    def assertObject(self, obj):
        self.assertEqual(obj.request, self.url_param.request)
        self.assertEqual(obj.key, self.url_param.key)
        self.assertEqual(obj.value_template, self.url_param.value_template)        
        
    def test_create_ok(self):
        self.url_param.delete()
        self._test_create_ok()
        
    def test_create_validation_error(self):
        self.url_param.delete()
        self.url_param.value_template = "{{a}"
        self._test_create_validation_error("Not correct")
               
    def test_not_auth_create_redirected(self):
        self._test_not_auth_create_redirected()
        
    def test_delete_ok(self):
        self._test_delete_ok()
        
    def test_not_auth_delete_redirected(self):
        self._test_not_auth_delete_redirected()
        
    def test_update_ok(self):
        self.url_param.value_template = 'new_value_template'
        self._test_update_ok()
        
    def test_update_validation_error(self):
        self.url_param.value_template = "{{a}"
        self._test_update_validation_error("Not correct")
               
    def test_not_auth_update_redirected(self):
        self._test_not_auth_update_redirected()
        
        
class TestManageHandlerHeaderParam(BaseManageTest):
    model = HeaderParam
    url_name_create = 'handler-headerparameter-create'
    url_name_delete = 'handler-headerparameter-delete'
    url_name_update = 'handler-headerparameter-update'
    
    def setUp(self):
        super(TestManageHandlerHeaderParam, self).setUp()
        self.handler = HandlerFactory(bot=self.bot)
        self.url_kwargs_create = {'bot_pk': self.bot.pk,
                                  'handler_pk': self.handler.pk}
        self.header_param = HeaderParamFactory(request=self.handler.request)
        self.url_kwargs_delete = self.url_kwargs_update = {'bot_pk': self.bot.pk,
                                                           'handler_pk': self.handler.pk,
                                                           'pk': self.header_param.pk}  
        
    def fill_form(self, form, create=False):
        form['key'] = self.header_param.key
        form['value_template'] = self.header_param.value_template
               
    def assertObject(self, obj):
        self.assertEqual(obj.request, self.header_param.request)
        self.assertEqual(obj.key, self.header_param.key)
        self.assertEqual(obj.value_template, self.header_param.value_template)        
        
    def test_create_ok(self):
        self.header_param.delete()
        self._test_create_ok()
        
    def test_create_validation_error(self):
        self.header_param.delete()
        self.header_param.value_template = "{{a}"
        self._test_create_validation_error("Not correct")
               
    def test_not_auth_create_redirected(self):
        self._test_not_auth_create_redirected()
        
    def test_delete_ok(self):
        self._test_delete_ok()
        
    def test_not_auth_delete_redirected(self):
        self._test_not_auth_delete_redirected()
        
    def test_update_ok(self):
        self.header_param.value_template = 'new_value_template'
        self._test_update_ok()
        
    def test_update_validation_error(self):
        self.header_param.value_template = '{{a}'
        self._test_update_validation_error('Not correct')
               
    def test_not_auth_update_redirected(self):
        self._test_not_auth_update_redirected()
        
        
class TestManageHookRecipient(BaseManageTest):
    model = Recipient
    url_name_create = 'hook-recipient-create'
    url_name_delete = 'hook-recipient-delete'
    url_name_update = 'hook-recipient-update'
    
    def setUp(self):
        super(TestManageHookRecipient, self).setUp()
        self.hook = HookFactory(bot=self.bot)
        self.url_kwargs_create = {'bot_pk': self.bot.pk,
                                  'hook_pk': self.hook.pk}
        self.recipient_id = 12334234
        self.recipient = RecipientFactory(hook=self.hook,
                                          chat_id=self.recipient_id)
        self.url_kwargs_delete = self.url_kwargs_update = {'bot_pk': self.bot.pk,
                                                           'hook_pk': self.hook.pk,
                                                           'pk': self.recipient.pk}  
        
    def fill_form(self, form, create=False):
        form['chat_id'] = self.recipient.chat_id
        form['name'] = self.recipient.name     
        
    def assertObject(self, obj):
        self.assertEqual(obj.hook, self.hook)
        self.assertEqual(obj.chat_id, self.recipient.chat_id)
        self.assertEqual(obj.name, self.recipient.name)     
        
    def test_create_ok(self):
        self.recipient.delete()
        self._test_create_ok()
               
    def test_not_auth_create_redirected(self):
        self._test_not_auth_create_redirected()
        
    def test_delete_ok(self):
        self._test_delete_ok()
        
    def test_not_auth_delete_redirected(self):
        self._test_not_auth_delete_redirected()

    def test_update_ok(self):
        self.recipient.chat_id = 234234234
        self._test_update_ok()
                
    def test_not_auth_update_redirected(self):
        self._test_not_auth_update_redirected()

class TestManageState(BaseManageTest):
    model = State
    url_name_create = 'state-create'
    url_name_delete = 'state-delete'
    url_name_update = 'state-update'
    
    def setUp(self):
        super(TestManageState, self).setUp()
        self.url_kwargs_create = {'bot_pk': self.bot.pk}
        self.state = StateFactory(bot=self.bot,
                                  name='name1')
        self.url_kwargs_delete = self.url_kwargs_update = {'bot_pk': self.bot.pk,
                                                           'pk': self.state.pk}

    def fill_form(self, form, create=False):
        form['name'] = self.state.name
        
    def assertObject(self, obj):
        self.assertEqual(obj.name, self.state.name)
        self.assertEqual(obj.bot, self.bot)        
        
    def test_create_ok(self):
        self.state.delete()
        self._test_create_ok()
        
    def test_not_auth_create_redirected(self):
        self._test_not_auth_create_redirected()
        
    def test_delete_ok(self):
        self._test_delete_ok()
        
    def test_not_auth_delete_redirected(self):
        self._test_not_auth_delete_redirected()
        
    def test_update_ok(self):
        self.state.name = 'name2'
        self._test_update_ok()
        
    def test_not_auth_update_redirected(self):
        self._test_not_auth_update_redirected()    