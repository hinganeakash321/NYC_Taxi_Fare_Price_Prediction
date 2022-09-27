import numpy as np 
import pandas as pd 
import pickle
from latitude_longitude import getdata
from address_list import zip_code

zip_p = ''
zip_d = ''

df_cols = ['pickup_datetime','pickup_longitude', 'pickup_latitude',
       'dropoff_longitude', 'dropoff_latitude', 'passenger_count']
#input_cols = ['passenger_count',
#       'trip_distance', 'year', 'month', 'day', 'weekday',
#       'pickup_datetime_hour' ]
       
input_cols = ['pickup_longitude', 'pickup_latitude', 'dropoff_longitude',
       'dropoff_latitude', 'passenger_count', 'year', 'month', 'day',
       'weekday', 'pickup_datetime_hour', 'trip_distance']

path="xgb_model.pkl"
model = pickle.load(open(path, 'rb'))

def input_processing(input):

    clock_time,book_date,pickup_point,dropoff_point,passenger_count=input
    # print(f"{type(zip_code)}, {type(pickup_point)}  --pick up")
    # print(f"{type(zip_code)}, {type(dropoff_point)} -drop")
    # print(f"pickup================================================ {pickup_point}")
    global zip_p
    global zip_d
    zip_p = zip_code.get(pickup_point[0])
    zip_d = zip_code.get(dropoff_point[0])
    

    pickup_point_lat , pickup_point_lon = getdata(pickup_point,zip_p)

    dropoff_point_lat , dropoff_point_lon = getdata(dropoff_point,zip_d)

    date_format=f"{str(book_date)} {str(clock_time)}"

    inp_user=[[date_format,pickup_point_lon,pickup_point_lat,dropoff_point_lon,dropoff_point_lat,passenger_count]]

    df = pd.DataFrame(inp_user,columns=df_cols)

    df=add_trip_distance(df)

    df=add_dateparts(df,'pickup_datetime')

    df = df.drop('pickup_datetime', axis=1)

    return df[input_cols]

#1
def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

#2
def add_trip_distance(df):
    df['trip_distance'] = haversine_np(df['pickup_longitude'], df['pickup_latitude'], df['dropoff_longitude'], df['dropoff_latitude'])
    return df

#3
def add_dateparts(df, col):
    df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S.%f')
    df['year'] = df[col].dt.year
    df['month'] = df[col].dt.month
    df['day'] = df[col].dt.day
    df['weekday'] = df[col].dt.weekday
    df[col + '_hour'] = df[col].dt.hour
    df.drop(col,axis=1)
    return df



