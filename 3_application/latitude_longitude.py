import pandas as pd
import json 
import requests

def getdata(street,zip):
  data = {'street': [street], 'zip': [zip],'city': ['New York'],'country': ['United State'],'lat':[0.0],'lng':[0.0]}
  df1 = pd.DataFrame(data)  

  pd.set_option('display.max_rows', None)

  for i, row in df1.iterrows():
    apiAddress = str(df1.at[i,'street'])+','+str(df1.at[i,'zip'])+','+str(df1.at[i,'city'])+','+str(df1.at[i,'country'])
    #print(apiAddress)
    
    parameters = {
        "key": "UL68GRBWrEgJq0CADyupLogaqZWfrheT",
        "location": apiAddress
    }

    response = requests.get("http://www.mapquestapi.com/geocoding/v1/address", params=parameters)
    #print(response)
    data = response.text
    dataJ = json.loads(data)['results']
    lat = (dataJ[0]['locations'][0]['latLng']['lat'])
    lng = (dataJ[0]['locations'][0]['latLng']['lng'])
    
    df1.at[i,'lat'] = lat
    df1.at[i,'lng'] = lng

  return float(df1['lat']),float(df1['lng'])