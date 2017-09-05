from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from round import RoundRecord
from identity import IdentityStore
from kivy.uix.modalview import ModalView
from identity import IdentityStore
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

class GameForm(BoxLayout):
    opponent_name_prop     = ObjectProperty()
    opponent_id_prop       = ObjectProperty()
    personal_id_prop       = ObjectProperty()
    deck_name_prop         = ObjectProperty()
    agenda_points_prop     = ObjectProperty()
    outcome_win_prop       = ObjectProperty()
    outcome_loss_prop      = ObjectProperty()
    outcome_tie_prop       = ObjectProperty()
    flatline_checkbox_prop = ObjectProperty()
    agenda_checkbox_prop   = ObjectProperty()

    def personal_id(self):
        # Logger.info('entering Modal function')
        # view = ModalView(size_hint=(None, None))
        # ids = IdentityStore.get_id_list(side_code='runner')
        # layout = GridLayout(orientation='vertical')
        # layout.bind(minimum_height=layout.setter('height'))
        # for id in ids:
        #     layout.rows += 1
        #     minilayout = GridLayout(cols=2)
        #     minilayout.add_widget(Label(text=str(id).replace(':','\n')))
        #     minilayout.add_widget(CheckBox(group='pids', value=str(id)))
        #     layout.add_widget(minilayout)
        # select_button = Button(text='Select')
        # select_button.bind(on_press=self.personal_id_select)
        # layout.add_widget(select_button)
        # root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        # root.add_widget(layout)
        # view.add_widget(root)
        # ScrollEffect(target_widget=view, max=100)
        # view.open()
        pass

    def personal_id_select(self):
        pass

    def submit_form(self):
        if not self.check_wining_conditions(): return
        r = RoundRecord(personal_id=self.personal_id_prop.text,
                        opp_name=self.opponent_name_prop.text,
                        opp_id=self.opponent_id_prop.text,
                        deck_name=self.deck_name_prop.text,
                        agenda_points=int(self.agenda_points_prop.value),
                        outcome=self.outcome_verify(),
                        victory_type=self.victory_verify()
                        )
        r.save()
        popup = self.create_popup(r.outcome)
        popup.open()

    def create_popup(self, outcome):
        layout = GridLayout(rows=2)
        layout.add_widget(Label(text='Your {v} \nhas been recorded.'.format(v=outcome), halign='center', size_hint_y=4))
        box = BoxLayout(size_hint_y=1)
        another_button = Button(text='Add Another Round', font_size=24)
        box.add_widget(another_button)
        cls_button = Button(text='Close Window', font_size=24)
        box.add_widget(cls_button)
        layout.add_widget(box)
        popup = Popup(title='Round Entry Saved', content=layout,
                      size_hint=(None, None), size=(500, 500))
        cls_button.bind(on_press=popup.dismiss)
        #another_button.bind()
        return popup

    def check_wining_conditions(self):
        winning_agenda_points = self.points_to_win(self.personal_id_prop.text, self.opponent_id_prop.text)
        if self.flatline_checkbox_prop.active:
            return True
        elif int(self.agenda_points_prop.value) >= winning_agenda_points:
            if not self.agenda_checkbox_prop.active:
                self.agenda_checkbox_prop.active = True
            return True
        else:
            return False

    def points_to_win(self, personal_id, opp_id):
        '''
        Stub until we get a method in identities to return
        the proper adjust winning value
        '''
        return IdentityStore.winning_agenda_points(personal_id, opp_id)

    def victory_verify(self):
        return 'flatline' if self.flatline_checkbox_prop.active else 'agenda'

    def outcome_verify(self):
        if self.outcome_win_prop:
            return 'win'
        elif self.outcome_loss_prop:
            return 'loss'
        elif self.outcome_tie_prop:
            return 'tie'