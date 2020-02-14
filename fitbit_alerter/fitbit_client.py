import matplotlib.pyplot as plt
import fitbit

import pandas as pd
import datetime

from fitbit_alerter.config import Config
from fitbit_alerter.gather_keys_oath2 import OAuth2Server

config = Config()
CLIENT_ID = config.client_id
CLIENT_SECRET = config.client_secret


class FitbitClient(object):
    def __init__(self):
        self.server = OAuth2Server(CLIENT_ID, CLIENT_SECRET)
        self.server.browser_authorize()
        ACCESS_TOKEN = str(self.server.fitbit.client.session.token['access_token'])
        REFRESH_TOKEN = str(self.server.fitbit.client.session.token['refresh_token'])
        self.auth2_client = fitbit.Fitbit(CLIENT_ID,
                                          CLIENT_SECRET,
                                          oauth2=True,
                                          access_token=ACCESS_TOKEN,
                                          refresh_token=REFRESH_TOKEN)

    def get_one_day_data(self, year: int, month: int, day: int):
        date = pd.datetime(year=year, month=month, day=day)
        data = self.auth2_client.intraday_time_series('activities/heart',
                                                 base_date=date,
                                                 detail_level='1sec')
        return data
    
    def get_body_fat(self, ):
        pass
    
    def get_body_weight(self, ):
        pass

    def get_sleep(self, ):
        pass
    
    def get_resting_heart_rates(self, s_year, s_month, s_day, e_year, e_month, e_day, period='1d'):
        start_date = pd.datetime(year=s_year, month=s_month, day=s_day)
        end_date = pd.datetime(year=e_year, month=e_month, day=e_day)

        heart_rates = self.auth2_client.time_series('activities/heart',
                                                    base_date=start_date,
                                                    end_date=end_date)#,
                                                    #period=period)
        resting_heart_rates = []
        for hr in heart_rates['activities-heart']:
            try:
                # TODO add datetimes
                resting_heart_rates.append(hr['value']['restingHeartRate'])
            except KeyError:
                continue
        return resting_heart_rates
