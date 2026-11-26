from nicegui import ui, app
from backend import Backend
from database import Data

class MainProject:
    def __init__(self):
        self.data=Data()
        self.frontend:Frontend=Frontend(self)
        self.frontend.backend=Backend(self.frontend, self.data)

    async def async_init(self):
        await self.frontend.interface()

MAX_ACTIVE_SENSORS = 4

class Frontend:
    def __init__(self, MainProject:MainProject):
        self.MainProject:'MainProject'=MainProject
        self.backend:'Backend'
        self.graph_data = {}

    async def interface(self):
        await self.backend.fetch_engine_data()
        await self.filters()
        await self.title()
        await self.settings()
        await self.Monitor_page()
        await self.evaluation()
        self.sensor_checkboxes['sensor_1'].value = True
        app.timer(1, self.backend.update)


    async def title(self):
        with ui.header().classes("bg-black"):
            ui.icon("engine")
            ui.label("Engine Monitor")

    async def filters(self):
        sensors_desc = await self.MainProject.data.fetch_sensor_data('sensors')

        self.sensor_checkboxes = {}

        with ui.left_drawer():
            ui.label("Sensors").classes("w-full")

            with ui.card() as card:
                for _, row in sensors_desc.iterrows():
                    field, unit, description = row['field'], row['units'], row['description']
                    with ui.row().classes('items-center flex-nowrap'):
                        checkbox = ui.checkbox().props('size=xs')
                        checkbox.on_value_change(
                            lambda e, field=field, unit=unit, description=description: self.on_sensor_toggle(field, unit, description, e.value))
                        self.sensor_checkboxes[field] = checkbox
                        ui.label(row['description'])
                        ui.icon('drag_indicator') \
                            .classes('handle cursor-grab active:cursor-grabbing')
            card.make_sortable(handle='.handle')

    def on_sensor_toggle(self, field, unit, description, checked):
        if checked:
            active = sum(cb.value for cb in self.sensor_checkboxes.values())
            if active > MAX_ACTIVE_SENSORS:
                self.sensor_checkboxes[field].value = False
                ui.notify(f'Just {MAX_ACTIVE_SENSORS} sensors at time', type='warning')
                return
            self.add_graph(field, unit, description)
        else:
            self.remove_graph(field)


    async def Monitor_page(self):
        with ui.card().classes("w-full"):
            self.graphs_container = ui.row().classes('w-full flex flex-wrap gap-4')


    async def settings(self):
        with ui.card(align_items="center").classes("w-full grid grid-col-3"):
            ui.label('setting 1').classes('col-start-1 span-col-1 justify-self-center')
            ui.label('setting 2').classes('col-start-2 span-col-1 justify-self-center')
            ui.label('setting 3').classes('col-start-3 span-col-1 justify-self-center')


            self.setting_1 = ui.input(value='600').props('disabled outlined dense input-class=text-center').classes('col-start-1 span-col-1 justify-self-center')
            self.setting_2 = ui.input(value='600').props('disabled outlined dense input-class=text-center').classes('col-start-2 span-col-1 justify-self-center')
            self.setting_3 = ui.input(value='600').props('disabled outlined dense input-class=text-center').classes('col-start-3 span-col-1 justify-self-center')


    def add_graph(self, field, unit, description):
        with self.graphs_container:
            with ui.card(align_items="center").classes("flex-1 min-w-[45%]") as card:
                ui.label(description).classes('w-full text-center')
                chart = ui.uplot({
                    'scales': {'x': {'time': False}},
                    'axes': [{'incrs': [1,10,20,50, 100,150, 200, 500]}, {'label': unit}],
                    'series': [{}, {'label': field, 'stroke': 'green'}],
                }, [[], []], keep_zoom=False).classes('w-full')

        self.graph_data[field] = {'card': card, 'chart': chart, 'cycles': [], 'values': []}

    def remove_graph(self, field):
        data = self.graph_data.pop(field, None)
        if data:
            data['card'].delete()

    async def evaluation(self, status:str='Normal', RUL:int=0):
        with ui.card(align_items="center").classes("w-full grid grid-col-2"):
            ui.label('Condition').classes('col-start-1 span-col-1 justify-self-center')
            ui.label('RUL').classes('col-start-2 span-col-1 justify-self-center')


            self.condition = ui.input(value='normal').props('disabled outlined dense input-class=text-center').classes('col-start-1 span-col-1 justify-self-center')
            self.rul = ui.input(value='120').props('disabled outlined dense input-class=text-center').classes('col-start-2 span-col-1 justify-self-center')
