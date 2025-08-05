from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from datetime import datetime

class MainScreen(Screen):
    spinner_machine = ObjectProperty(None)
    input_date = ObjectProperty(None)
    btn_add_machine = ObjectProperty(None)

    def on_pre_enter(self):
        self.update_machines()

    def update_machines(self):
        machines = self.manager.app.data_manager.get_machines()
        self.spinner_machine.values = machines
        if machines:
            self.spinner_machine.text = machines[0]
        else:
            self.spinner_machine.text = 'Sin máquinas'

    def add_machine_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_machine = TextInput(hint_text='Nombre máquina', multiline=False)
        btn_add = Button(text='Agregar', size_hint_y=None, height=40)
        btn_cancel = Button(text='Cancelar', size_hint_y=None, height=40)

        content.add_widget(input_machine)
        content.add_widget(btn_add)
        content.add_widget(btn_cancel)

        popup = Popup(title='Agregar máquina', content=content, size_hint=(.8, .4))

        def add_machine(instance):
            name = input_machine.text.strip()
            if name:
                self.manager.app.data_manager.add_machine(name)
                self.manager.app.data_manager.save()
                self.update_machines()
                popup.dismiss()

        btn_add.bind(on_press=add_machine)
        btn_cancel.bind(on_press=popup.dismiss)
        popup.open()

    def add_record(self):
        machine = self.spinner_machine.text
        date = self.input_date.text.strip()
        if machine == 'Sin máquinas' or not date:
            self.show_message('Selecciona máquina y fecha válida (AAAA-MM-DD)')
            return
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except:
            self.show_message('Formato de fecha incorrecto. Usa AAAA-MM-DD')
            return

        record = {
            'hora_reporte': datetime.now().strftime('%H:%M'),
            'nota': 'Falla registrada'
        }
        self.manager.app.data_manager.add_record(machine, date, record)
        self.show_message(f'Registro guardado para {machine} en {date}')

    def show_message(self, msg):
        popup = Popup(title='Mensaje',
                      content=Label(text=msg),
                      size_hint=(.7, .3))
        popup.open()


class HistoryScreen(Screen):
    spinner_machine = ObjectProperty(None)
    spinner_date = ObjectProperty(None)
    layout_records = ObjectProperty(None)
    label_summary = ObjectProperty(None)

    def on_pre_enter(self):
        self.update_machines()

    def update_machines(self):
        machines = self.manager.app.data_manager.get_machines()
        self.spinner_machine.values = machines
        if machines:
            self.spinner_machine.text = machines[0]
            self.update_dates()
        else:
            self.spinner_machine.text = 'Sin máquinas'
            self.spinner_date.values = []
            self.spinner_date.text = 'Sin fechas'
            self.clear_records()

    def update_dates(self, *args):
        machine = self.spinner_machine.text
        dates = self.manager.app.data_manager.get_dates(machine)
        self.spinner_date.values = dates
        if dates:
            self.spinner_date.text = dates[0]
            self.show_records()
        else:
            self.spinner_date.text = 'Sin fechas'
            self.clear_records()

    def show_records(self, *args):
        self.layout_records.clear_widgets()
        machine = self.spinner_machine.text
        date = self.spinner_date.text
        records = self.manager.app.data_manager.get_records(machine, date)
        if not records:
            self.layout_records.add_widget(Label(text='No hay registros para esta fecha'))
            self.label_summary.text = 'Total registros: 0'
            return
        total = 0
        for rec in records:
            text = f"Hora reporte: {rec.get('hora_reporte', 'N/A')} - Nota: {rec.get('nota', '')}"
            self.layout_records.add_widget(Label(text=text))
            total += 1
        self.label_summary.text = f'Total registros: {total}'

    def clear_records(self):
        self.layout_records.clear_widgets()
        self.layout_records.add_widget(Label(text='No hay registros para mostrar'))
        self.label_summary.text = ''