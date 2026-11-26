import pandas as pd
from pathlib import Path


class Data:
    def __init__(self):
        self.processed_dir = Path(__file__).resolve().parents[1] / "data" / "processed"
        self.dataset_path = self.processed_dir / "NASA_dataset.csv"
        self.descriptions_path = self.processed_dir / "NASA_descriptions.csv"

        self.data: pd.DataFrame
        self.data_engine: pd.DataFrame
        self.row_index = 0

        self.sensors_description = pd.read_csv(self.descriptions_path)
        self.data = pd.read_csv(self.dataset_path)
        

    async def fetch_sensor_data(self, fields: str | None = None):
        if fields is None:
            return self.sensors_description

        if fields == 'settings':
            _filter = [f'setting_{i}' for i in range(1,4)]
        elif fields == 'sensors':
            _filter = [f'sensor_{i}' for i in range(1,22)]
        else:
            raise ValueError(f"Unknown fields value: {fields!r}")

        filtered = self.sensors_description[self.sensors_description['field'].isin(_filter)]
        return filtered

    async def fetch_engine_data(self, subset_type: str = "train", subset: str = "FD001", engine_id: int = 1):
        filter = (
            (self.data["subset_type"] == subset_type) &
            (self.data["subset"] == subset) &
            (self.data["engine_id"] == engine_id))

        self.data_engine = self.data[filter]

    def next_row(self):
        row = self.data_engine.iloc[self.row_index]
        self.row_index += 1
        return row
