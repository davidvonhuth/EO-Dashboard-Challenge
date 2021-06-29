import pandas as pd
import numpy as np


def count_comment_lines(path):
    i = 0
    with open(path) as file:
        for line in file:
            if line[0] == '#':
                i += 1
            else:
                break
    return i


def filter_df_by_date(df, start_date="1990-01-01", end_date="2050-01-01"):
    after_start_date = df.index >= start_date
    before_end_date = df.index <= end_date
    between_two_dates = after_start_date & before_end_date
    return df.loc[between_two_dates]


def parse_discharge_data(path):
    n_comment_lines = 38
    _df = pd.read_csv(path, sep=';', skiprows=38)
    _df['timestamp'] = pd.to_datetime(_df['YYYY-MM-DD'], infer_datetime_format=True)
    # Remove missing data
    _df = _df[_df[' Original'] > -999.0]
    _df = _df.rename(columns={' Original': "discharge"})
    return _df.drop(columns=['YYYY-MM-DD', 'hh:mm', ' Calculated'])


def get_means_by_month(_df):
    months = range(1, 13)
    averages = []
    for month in months:
        curr_month = _df[_df['timestamp'].map(lambda x: x.month) == month]
        averages.append(curr_month['discharge'].mean())
    return np.array(averages)
