from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory
from game_form import GameForm
from identity import IdentityStore
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.spinner import SpinnerOption
from kivy.logger import Logger
from kivy.uix.dropdown import DropDown


class SideChooser(BoxLayout):

    def corp_response(self):
        print 'Corporation'

    def runner_response(self):
        print 'Runner'


class RunTrackerRoot(BoxLayout):

    def show_game_form(self, side):
        self.clear_widgets()
        gameform = Factory.GameForm()
        gameform.side_prop = side
        self.setup_ids(gameform, side)
        self.add_widget(gameform)

    def setup_ids(self, form, side):
        Logger.info(side)
        runner_ids = IdentityStore.get_id_list(side_code='runner')
        corp_ids = IdentityStore.get_id_list(side_code='corp')
        runner_ids.sort()
        corp_ids.sort()
        if side == 'Runner':
            form.personal_id_prop.values = tuple(runner_ids)
            form.personal_id_prop.text   = runner_ids[0]
            form.opponent_id_prop.values = tuple(corp_ids)
            form.opponent_id_prop.text   = corp_ids[0]
        else:
            form.personal_id_prop.values = tuple(corp_ids)
            form.personal_id_prop.text   = corp_ids[0]
            form.opponent_id_prop.value = tuple(runner_ids)
            form.opponent_id_prop.text   = runner_ids[0]

        # base_button = form.personal_id_dd_prop
        # dropdown = DropDown()
        # for x in ids:
        #     Logger.info(x)
        #     btn = Button(text=str(x), height=44)
        #     btn.bind(on_release=lambda btn: dropdown.select(btn.text))
        #     dropdown.add_widget(btn)
        # base_button.add_widget(dropdown)
        # base_button.bind(on_release=dropdown.open)
        # dropdown.bind(on_select=lambda instance, x: setattr(base_button, 'text', x))


class RunTrackerApp(App):
    # i = IdentityStore()
    # i.update()
    pass

if __name__ == '__main__':
    RunTrackerApp().run()