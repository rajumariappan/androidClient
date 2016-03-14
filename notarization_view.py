from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.label import Label
from kivy.adapters.dictadapter import DictAdapter
import webbrowser

from notarization_details import NotarizationDetailView


class MasterDetailView(GridLayout):
    '''Implementation of an master-detail view with a vertical scrollable list
    on the left (the master, or source list) and a detail view on the right.
    When selection changes in the master list, the content of the detail view
    is updated.
    '''

    def __init__(self, items, **kwargs):
        kwargs['cols'] = 2
        super(MasterDetailView, self).__init__(**kwargs)
        self.notary = kwargs['notary']
        self.items = items
        list_item_args_converter = \
                lambda row_index, rec: {'text': rec['name'],
                                        'size_hint_y': None,
                                        'height': 25}

        dict_adapter = DictAdapter(sorted_keys=sorted(items.keys()),
                                   data=items,
                                   args_converter=list_item_args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   cls=ListItemButton)
        list_header = Label(text='CLAIMS MADE',size_hint=(.3, .1), font_size='20sp', bold=True)
        self.add_widget(list_header)
        detail_header = Label(text='CLAIM DETAILS',size_hint=(.7, .1), font_size='20sp', bold=True)
        self.add_widget(detail_header)
        master_list_view = ListView(adapter=dict_adapter,
                                    background_down=[.2, .2, .2, 1],
                                    size_hint=(.3, 1.0))

        self.add_widget(master_list_view)

        detail_view = NotarizationDetailView(
                title=dict_adapter.selection[0].text,
                items=self.items,
                notary=self.notary,
                size_hint=(.7, 1.0))

        dict_adapter.bind(on_selection_change=detail_view.item_changed)
        self.add_widget(detail_view)

    def go_home(self):
        webbrowser.open("https://www.waitingforsatoshi.com")
