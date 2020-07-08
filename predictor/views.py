from django.shortcuts import render
from sklearn.tree import DecisionTreeRegressor
from predictor.choices import warming_type
import googlemaps
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Create your views here.
def predict(request):
    if request.method == 'POST':
        propertytype=request.POST['propertytype']
        address=request.POST['address']
        bahtroom=request.POST['bahtroom']
        livingroom=request.POST['livingroom']
        bedroom=request.POST['bedroom']
        netarea=request.POST['netarea']
        age=request.POST['age']
        #heating
        state=request.POST['state']
        floornum=request.POST['floornum']
        totalfloor=request.POST['totalfloor']
        #latitute longtitude
        latlong=latitudelongtitude(address)
    else:
        propertytype=0
        address=0
        bahtroom=0
        livingroom=0
        bedroom=0
        netarea=0
        age=0
        #heating
        state=0
        floornum=0
        totalfloor=0
        #latitute longtitude
        latlong=[0,0]

    df1 = pd.read_csv("C:/Users/pampamamericano/PycharmProjects/bitiriyor/predictor/121.csv")
    df1['pricepersqft'] = df1["RealtyPrice"] / df1["NetArea"]
    df2 = df1[~(df1.NetArea / df1.TotalRooms > 38)]
    df3 = removepricepersqftoutliers(df2)
    df4 = removebahtroomoutlier(df3)
    A = pd.DataFrame()
    A["PropertyType"] = df4['PropertyType']
    A["Bahtroom"] = df4["Bahtroom"]
    A["LivingRoom"] = df4["LivingRoom"]
    A["Room"] = df4["Room"]
    A["NetArea"] = df4["NetArea"]
    A["Age"] = df4["Age"]
    A["Heating"] = df4["Heating"]
    A["FloorNumber"] = df4["FloorNumber"]
    A["FloorCount"] = df4["FloorCount"]
    A["Latitude"] = df4["Latitude"]
    A["Longtitude"] = df4["Longtitude"]
    A["RealtyPrice"] = df4["RealtyPrice"]
    X = A.drop("RealtyPrice", axis="columns")
    y = A.RealtyPrice
    x = np.zeros(len(X.columns))
    x[0] = propertytype
    x[1] = bahtroom
    x[2] = livingroom
    x[3] = bedroom
    x[4] = netarea
    x[5] = age
    x[6] = state
    x[7] = floornum
    x[8] = totalfloor
    x[9] = latlong[0]
    x[10] = latlong[1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    lr_clf = DecisionTreeRegressor(criterion="friedman_mse", splitter="best",max_depth=10)
    lr_clf.fit(X_train, y_train)
    predicted=lr_clf.predict([x])[0]
    context = {
        'warming_type' : warming_type,
        'predicted' : predicted
    }


    return render(request, 'predictor/predictor.html',context)

def latitudelongtitude(request):
    gmaps_key = googlemaps.Client(key="AIzaSyB5UNh4NCFM0pLc3R5OEUK6kNZJHHGJIHI")
    geocode_result = gmaps_key.geocode(request)
    latlong=[]
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        latlong.append(lat)
        latlong.append(lon)
    except:
        latlong.append(33)
        latlong.append(33)
    return latlong

def removepricepersqftoutliers(df):
    #we create empty data frame
    df_out=pd.DataFrame()
    #first we group propertytype then we assigning them into subdf
    for key,subdf in df.groupby("PropertyType"):
        m=np.mean(subdf.pricepersqft)
        sd=np.std(subdf.pricepersqft)
        reduced_df=subdf[(subdf.pricepersqft>(m-sd))&(subdf.pricepersqft<(m+sd))]
        df_out=pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out

def removebahtroomoutlier(df):
    exclude_indices=np.array([])
    for propertytype, propertytype_df in  df.groupby("PropertyType"):
        bahtstats={}
        for bathroom, bathroom_df in propertytype_df.groupby("Bahtroom"):
            bahtstats[bathroom]={
                "mean":np.mean(bathroom_df.pricepersqft),
                "std":np.std(bathroom_df.pricepersqft),
                "count":bathroom_df.shape[0]
            }
        for bathroom, bathroom_df in propertytype_df.groupby("Bahtroom"):
            stats=bahtstats.get(bathroom-1)
            if stats and stats["count"]>5:
                exclude_indices=np.append(exclude_indices,bathroom_df[bathroom_df.pricepersqft<(stats["mean"])].index.values)
    return df.drop(exclude_indices,axis="index")

