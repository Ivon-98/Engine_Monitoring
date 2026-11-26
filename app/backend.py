from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frontend import Frontend
    from database import Data

class Backend:
    def __init__(self, frontend:'Frontend', data:'Data'):
        self.frontend=frontend
        self.data=data

    async def fetch_engine_data(self, subset_type:str='train', subset:str='FD001', engine_id:int=1):
        await self.data.fetch_engine_data(subset_type, subset, engine_id)

    async def next_row(self):
        return self.data.next_row()

    async def update(self) -> None:
        self.row = await self.next_row()
        await self.set_graphs()
        await self.set_settings()
        await self.set_status()

    async def set_graphs(self):
        for field, data in self.frontend.graph_data.items():
            data['cycles'].append(self.row['cycle'])
            data['values'].append(self.row[field])
            data['chart'].data = [data['cycles'], data['values']]

    async def set_settings(self):
        self.frontend.setting_1.value = self.row['setting_1']
        self.frontend.setting_2.value = self.row['setting_2']
        self.frontend.setting_3.value = self.row['setting_3']

    async def set_status(self):
        self.frontend.rul.value = self.row['rul_limited']
