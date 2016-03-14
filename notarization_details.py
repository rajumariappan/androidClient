from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from buttons import IconButton
import webbrowser
import os


class NotarizationDetailView(FloatLayout):
    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        kwargs['background_color'] = [0, 0, 0, 1]
        self.title = kwargs.get('title', '')
        super(NotarizationDetailView, self).__init__(**kwargs)
        self.notary = kwargs['notary']
        self.items = kwargs['items']
        if self.title:
            self.redraw()

    def redraw(self, *args):
        self.clear_widgets()
        claim = self.items[self.title]
        if self.title:
            l1 = Label(text='FILENAME', bold=True, font_size='10sp', halign='center', pos_hint={'x': .02, 'y': .48})
            l2 = Label(text=self.title, halign='center', pos_hint={'x': .02, 'y': .45})
            l3 = Label(text='TRANSACTION ID', bold=True, font_size='10sp', halign='center', pos_hint={'x': .125, 'y': .17})
            l4 = Label(text=claim['transaction'], valign='bottom', text_size=[130, None], italic=True, halign='center',
                       pos_hint={'x': .125, 'y': .08})
            self.add_widget(l1)
            self.add_widget(l2)
            self.add_widget(l3)
            self.add_widget(l4)

            self.add_widget(IconButton(source='img/cloud-up.png',
                                       source_pressed='img/cloud-down.png',
                                       allow_stretch=True,
                                       keep_ratio=True,
                                       callback=self.download_callback,
                                       size_hint=[.15, .15],
                                       pos_hint={'x': .32, 'y': .76}))
            self.add_widget(Label(text='download\nfile', halign='center', pos_hint={'x': -.10, 'y': .24}))
            self.add_widget(IconButton(source='img/blockchain.png',
                                       source_pressed='img/blockchaincopy.png',
                                       allow_stretch=True,
                                       keep_ratio=True,
                                       callback=self.status_callback,
                                       size_hint=[.15, .15],
                                       pos_hint={'x': .55, 'y': .76}))
            self.add_widget(Label(text='view on\nblockchain', halign='center', pos_hint={'x': .126, 'y': .24}))

    def item_changed(self, list_adapter, *args):
        if len(list_adapter.selection) == 0:
            self.title = None
        else:
            selected_object = list_adapter.selection[0]

            if type(selected_object) is str:
                self.title = selected_object
            else:
                self.title = selected_object.text

        self.redraw()

    def download_callback(self):
        document_hash = self.items[self.title]['document_hash']
        self.notary.download_file_decrypted(document_hash, self.title)
        cwd = os.getcwd()
        webbrowser.open("file:///"+cwd+'/'+self.title)

    def status_callback(self):
        transaction = self.items[self.title].get('transaction')
        webbrowser.open("https://live.blockcypher.com/btc-testnet/tx/"+transaction)

    def go_home(self):
        webbrowser.open("https://www.waitingforsatoshi.com")
