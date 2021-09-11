import pandas as pd


class Driver:
    def __init__(self, name: str, values: dict = None):
        self.name = name
        self.df = pd.DataFrame()
        self.load_driver_data(values)

    def load_driver_data(self, values: dict):
        if values is None:
            return None
        else:
            dates = []
            data = []
            for key, val in values.items():
                dates.append(key)
                data.append(val)
            data_dict = {'date': dates, self.name: data}
            self.df = pd.DataFrame.from_dict(data_dict)
            return self.df
