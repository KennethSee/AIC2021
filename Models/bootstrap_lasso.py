import numpy as np
import pandas as pd
import random
from sklearn.model_selection import KFold
from sklearn.linear_model import Lasso, LassoCV


class BootstrapLasso:
    def __init__(self, df, x_name: str):
        # remove date column if exists
        if 'date' in df.columns:
            df = df.drop(['date'], axis=1)

        self.df = df
        self.x_name = x_name
        self.boots = []
        self._bootstrap()
        self.trained = []
        self.predicts = []
        self.final_prediction = 0

    def train(self):
        alphas = np.linspace(pow(10, 2), pow(10, 3))
        cv = KFold(n_splits=5, shuffle=True, random_state=2)
        for boot in self.boots:
            clf_lasso = LassoCV(alphas=alphas, cv=cv, normalize=True).fit(self.df.drop([self.x_name], axis=1),
                                                                          self.df[self.x_name])
            self.trained.append(clf_lasso)

    def predict(self, next_driver_values: pd.DataFrame):
        for train_model in self.trained:
            prediction = train_model.predict(next_driver_values)
            self.predicts.append(prediction)
        self.final_prediction = np.mean(self.predicts)
        return self.final_prediction

    def _bootstrap(self):
        for i in range(100):
            self.boots.append(BootstrapLasso.bootstrap_sample(self.df.shape[0], self.df))
        return self.boots

    @staticmethod
    def bootstrap_sample(n: int, df):
        df_bootstrap = pd.DataFrame()
        for i in range(n):
            rand_num = random.randint(0, n - 1)
            row = df.iloc[rand_num]
            df_bootstrap = df_bootstrap.append(row)
        return df_bootstrap