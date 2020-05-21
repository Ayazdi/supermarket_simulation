""" probability Matrix and array
This module reads the csv data and apply feature engineering in order to obtain
probablilty matrix and arrays to define customers pattern in the supermarket
and the time they spend at each aisle.
"""
import pandas as pd
import os


class PorbabilityClass():

    def __init__(self, aisle, weekday):
        """
        Parameters
        ----------
        aisle : str
            name of the aisle in the supermarket
        weekday : str
                either a day of the week from Monday to Friday or all_days
        """
        self.weekday = weekday
        self.aisle = aisle

    def read_data(self):
        """Read and concatenation of the csv files"""
        PATH = "..\\data\\"
        df = pd.DataFrame()
        for csv in os.listdir(PATH):
            if csv[-3:] == "csv":
                df_day = pd.read_csv(f'{PATH}{csv}', delimiter=";")
                df = pd.concat([df, df_day], sort=True)
        return df

    def add_datetime_columns(self):
        """Add hour and weekday columns to the dataset"""
        df = self.read_data()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df['hour'] = df['timestamp'].dt.hour
        df['weekday'] = df['timestamp'].dt.weekday
        df['weekday'].replace({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}, inplace=True)

        return df

    def porb_matrix_by_day(self):
        """
        Probability matrix of the aisles and probability array
        of the first aisle of each day of the week or all days toghether

        returns probability array of the first aisle and the probability matrix
        """
        df = self.add_datetime_columns()
        if self.weekday == 'all_days':
            df_1 = pd.DataFrame(df.sort_values(['customer_no', 'timestamp']).groupby(['weekday', 'customer_no', 'location'])['timestamp'].min())
            df_1 = df_1.sort_values(["customer_no", 'timestamp'])
            df_1 = pd.DataFrame(df_1.index.get_level_values(2), df_1['timestamp']).reset_index()

        else:
            df_1 = df[df['weekday'] == self.weekday]
            df_1 = pd.DataFrame(df_1.sort_values(['customer_no', 'timestamp']).groupby(['customer_no', 'location'])['timestamp'].min())
            df_1 = df_1.sort_values(["customer_no", 'timestamp'])
            df_1 = pd.DataFrame(df_1.index.get_level_values(1), df_1['timestamp']).reset_index()
        df_1['next_location'] = df_1['location'].shift(-1)
        df_1['next_location'][df_1['location'] == 'checkout'] = 'checkout'
        df_1['initial'] = df_1['location'].shift(-1)

        first_loc = df_1['initial'][df_1['location'] == 'checkout']
        first_loc = first_loc.value_counts()/first_loc.value_counts().sum()

        prob_mat = pd.crosstab(df_1['location'], df_1['next_location'], normalize=0)

        return first_loc, prob_mat

    def sector_time_prob(self):
        """
        Probability array of the time spent at each aisle on each day of the
        week or all days of the week
        """

        df = self.add_datetime_columns()
        if self.weekday == 'all_days':
            df_1 = pd.DataFrame(df.sort_values(['customer_no', 'timestamp']).groupby(['weekday','customer_no','location'])['timestamp'].min())
            df_1 = df_1.sort_values(["customer_no",'timestamp'])
            df_1 = pd.DataFrame(df_1.index.get_level_values(2), df_1['timestamp']).reset_index()
        else:
            df_1 = df[df['weekday'] == self.weekday]
            df_1 = pd.DataFrame(df_1.sort_values(['customer_no', 'timestamp']).groupby(['customer_no','location'])['timestamp'].min())
            df_1 = df_1.sort_values(["customer_no", 'timestamp'])
            df_1 = pd.DataFrame(df_1.index.get_level_values(1), df_1['timestamp']).reset_index()

        df_1['timestamp-2'] = df_1['timestamp'].shift(-1)
        df_1 = df_1[df_1['location'] == self.aisle]
        df_1['timespent'] = df_1['timestamp-2'] - df_1['timestamp']
        df_1 = df_1[(df_1['timespent'] < pd.to_timedelta('40m')) & (df_1['timespent'] >= pd.to_timedelta('1m'))]

        time_prob = df_1['timespent'].value_counts()/df_1['timespent'].value_counts().sum()
        time_prob.index = time_prob.index/pd.Timedelta('1 min')

        return time_prob
