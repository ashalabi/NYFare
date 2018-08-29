import pandas as pd
import seaborn as sns
from geopy.distance import geodesic


#column names provided.
cols = ['fare_amount', 'pickup_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count'] 
types = {'fare_amount': 'float16',
         'pickup_longitude': 'float32',
         'pickup_latitude': 'float32',
         'dropoff_longitude': 'float32',
         'dropoff_latitude': 'float32',
         'passenger_count': 'uint8'}

train_data = pd.read_csv("train.csv", dtype = types, usecols = cols, index_col=False)
df_clean = train_data.copy(deep=True)

#use histograms to narrow in on a range of acceptable values, in order to clean.
#sns.distplot(train_data[(train_data["fare_amount"]<100) & (train_data["fare_amount"]>0)]["fare_amount"],kde=False)
#sns.distplot(df_clean[df_clean["passenger_count"]<20]["passenger_count"], kde=False)

#cleaning, removing unacceptable values.
df_clean =  df_clean[(df_clean["fare_amount"]<100) & (df_clean["fare_amount"]>2)]
df_clean =  df_clean[df_clean["passenger_count"]<20]
df_clean = df_clean[(df_clean["pickup_longitude"]<=180)
                    & (df_clean["pickup_longitude"]>=-180)
                    & (df_clean["pickup_latitude"]>=-90)
                    & (df_clean["pickup_latitude"]<=90)]

df_clean = df_clean[(df_clean["dropoff_longitude"]<=180)
                    & (df_clean["dropoff_longitude"]>=-180)
                    & (df_clean["dropoff_latitude"]>=-90)
                    & (df_clean["dropoff_latitude"]<=90)]


#df_clean_zeros = len(df_clean[(df_clean["dropoff_longitude"]==0)
#                    | (df_clean["dropoff_longitude"]==0)
#                    | (df_clean["pickup_latitude"]==0)
#                    | (df_clean["pickup_latitude"]==0)])
#df_clean_zeros/len(df_clean)*100 

#zeroes are only ~2 % of data. so will drop.
df_clean = df_clean[(df_clean["dropoff_longitude"]!=0)
                    & (df_clean["dropoff_longitude"]!=0)
                    & (df_clean["pickup_latitude"]!=0)
                    & (df_clean["pickup_latitude"]!=0)]

df_clean = df_clean[df_clean["passenger_count"]!=0]

df_clean.to_csv("allclean_traindata_nodist.csv")

#Note that the following was not done locally as it took too long. But it is part of the cleaning process.
#NYCFare_Modeling.py contains the follow code as it is easier to do on the cloud.
df_clean["distance"] = df_clean[["pickup_latitude","pickup_longitude","dropoff_latitude","dropoff_longitude"]].apply(lambda x: geodesic((x[0],x[1]),(x[2],x[3])).miles,axis=1)
df_clean["hour_of_day"] = df_clean["pickup_datetime"].apply(lambda x: abs(x.hour-12))
df_clean["year"] = df_clean["pickup_datetime"].apply(lambda x: x.year)
df_clean["day_of_year"] = df_clean["pickup_datetime"].apply(lambda x: abs(x.dayofyear-182))
df_clean["day_of_week"] = df_clean["pickup_datetime"].apply(lambda x: abs(x.dayofweek-3))
df_clean["month"] = df_clean["pickup_datetime"].apply(lambda x: abs(x.month-6))
df_clean["quarter"] = df_clean["pickup_datetime"].apply(lambda x: abs(x.quarter-2))

#no longer need, wasted mem space.
df_clean = df_clean.drop(["pickup_datetime"],axis=1)

#had to do this since we dropped rows, our indices are not sequential. 
df_clean = df_clean.reset_index(drop=True) 

df_clean.to_csv("cleaned_data.csv")
