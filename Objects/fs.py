class FS:
    def __init__(self, df):
        self.df = df
        # get fs items, direction and fixed status
        items = df.iloc[:, 0].tolist()
        direction = df.iloc[:, 1].tolist()
        is_fixed = df.iloc[:, 2].tolist()
        self.items = {}
        for i in range(len(items)):
            self.items[items[i]] = (direction[i], is_fixed[i])
        # transform data
        self.df_processed = self.process()

    def process(self):
        df_t = self.df.drop(['Direction', 'IsFixed'], axis=1).T
        new_header = df_t.iloc[0]
        df_t = df_t.iloc[1::, :]
        df_t.columns = new_header
        df_t.reset_index(inplace=True)
        df_t = df_t.rename(columns={'index': 'date'})
        return df_t

    def get_fs_items(self):
        return [key for key, value in self.items.items()]

    def get_fs_variable_items(self):
        '''Only retrieve items that are not fixed'''
        items = self.get_fs_items()
        return [item for item in items if self.items[item][1] != 1]

    def get_dates(self):
        return self.df_processed['date'].tolist()