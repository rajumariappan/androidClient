from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from notary_client import NotaryException
from kivy.uix.label import Label
from notarization_view import MasterDetailView
import webbrowser


def initFlow(m_app, ui_test):
    global notary_app
    global ui_test_mode
    ui_test_mode = ui_test
    notary_app = m_app


class CreateWalletScreen(Screen):
    password = ObjectProperty(None)
    retype_password = ObjectProperty(None)

    def go_home(self):
        webbrowser.open("https://www.waitingforsatoshi.com")

    def create_wallet_callback(self):
        print('create wallet callback called')
        if ui_test_mode:
            notary_app.sm.current = "registerwallet"
            return
        from notary_client import NotaryClient
        password_value = self.ids.password.text
        retyped_value = self.ids.retype_password.text
        if password_value == retyped_value:
            notary_app.notary_obj = NotaryClient("notaryconfig.ini", password_value)
            notary_app.sm.current = 'registerwallet'
        else:
            popup = Popup(title='Password Mismatch', content=Label(text='Passwords does not match'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()


class RegisterWalletScreen(Screen):
    email = ObjectProperty(None)

    def register_wallet_callback(self):
        print('register wallet callback called')
        if ui_test_mode:
            notary_app.sm.current = "confirmemail"
            return
        email_value = self.ids.email.text
        notary_app.notary_obj.register_user(email_value)
        notary_app.sm.current = 'confirmemail'


class PasswordScreen(Screen):
    password = ObjectProperty(None)

    def go_home(self):
        webbrowser.open("https://www.waitingforsatoshi.com")

    def open_wallet_callback(self):
        print('open wallet callback called')
        if ui_test_mode:
            notary_app.sm.current = "landingpage"
            return
        from notary_client import NotaryClient, NotaryException
        import simplecrypt
        password_value = self.ids.password.text
        if password_value is None:
            popup = Popup(title='Wrong Password', content=Label(text='Wrong password'), size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            return
        if len(password_value) is 0:
            popup = Popup(title='Wrong Password', content=Label(text='Wrong password'), size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            return

        try:
            notary_app.notary_obj = NotaryClient("notaryconfig.ini", password_value)
            account = notary_app.notary_obj.get_account()
            notary_app.sm.current = 'landingpage'
        except NotaryException as e:
            print("Code %s " % e.error_code)
            print(e.message)
            if e.error_code == 404:
                notary_app.sm.current = 'registerwallet'
            elif e.error_code == 403:
                notary_app.sm.current = 'confirmemail'
        except ValueError as e:
            print("ValueError ")
            print(e.message)
            popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'),
                          size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            notary_app.sm.current = 'confirmemail'
        except simplecrypt.DecryptionException as e:
            print e.message
            popup = Popup(title='Wrong Password', content=Label(text='Wrong password'), size_hint=(None, None),
                          size=(400, 200))
            popup.open()


class ConfirmScreen(Screen):

    def go_home(self):
        webbrowser.open("https://www.waitingforsatoshi.com")

    def confirm_email_callback(self):
        print('confirm email callback called')
        if ui_test_mode:
            notary_app.sm.current = "landingpage"
            return
        from notary_client import NotaryException
        # print notary_obj.register_user_status()
        try:
            account = notary_app.notary_obj.get_account()
            notary_app.sm.current = 'landingpage'
        except ValueError as e:
            print("ValueError ")
            print(e.message)
            popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'),
                          size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            notary_app.sm.current = "confirmemail"
        except NotaryException as e:
            if e.error_code == 404 or e.error_code == 403:
                popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'),
                              size_hint=(None, None),
                              size=(400, 200))
                popup.open()
                notary_app.sm.current = 'confirmemail'

class ViewClaimsScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def go_home(self):
        webbrowser.open("https://www.waitingforsatoshi.com")

    def get_items(self, notarizations):
        items = dict()
        for notarization in notarizations:
            items[notarization['title']] = {}
            items[notarization['title']] = \
                    dict({'name': notarization['title'],
                          'transaction': notarization['transaction_hash'],
                          'document_hash': notarization['document_hash']})
        return items

    def on_enter_event(self):
        try:
            message = notary_app.notary_obj.get_notarizations()
            myitems = self.get_items(message)
            print (myitems.keys())
            if len(message) > 0:
                view = MasterDetailView(items=myitems, notary=notary_app.notary_obj)
                self.ids.claimsgrid.add_widget(view)

        except NotaryException as e:
            print("Code %s " % e.error_code)
            print(e.message)

    def on_leave_event(self):
            self.ids.claimsgrid.clear_widgets()
