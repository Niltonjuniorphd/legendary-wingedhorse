import os
import pandas as pd

daily_csv = 'database/daily_data.csv'
historical_csv = 'database/historical_data.csv'
if os.path.exists(historical_csv):
    df_daily = pd.read_csv(daily_csv)
    if df_daily['Date'].loc[0] == pd.Timestamp.today().date().strftime('%Y-%m-%d'):
        print('Data already exists in the master CSV.')
    else:
        df_daily.to_csv(historical_csv, mode='a', header=False, index=False)
        print('Data added to the historical CSV.')
    
else:
    df_master = pd.read_csv(daily_csv)
    df_master.to_csv(historical_csv, index=False)
    print('Creating a historical CSV and add the first daily data.')


