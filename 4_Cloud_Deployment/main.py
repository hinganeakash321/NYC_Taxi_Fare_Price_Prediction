import streamlit as st
import gmplot
import datetime 
from latitude_longitude import *
from location import *
from address_list import *
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components 
from PIL import Image


path="xgb_model.pkl"
model = pickle.load(open(path, 'rb'))

def function(clock_time,book_date,pickup_point,dropoff_point,passenger_count):
    input_data=clock_time,book_date,pickup_point,dropoff_point,passenger_count
    df = input_processing(input_data)
    output=model.predict(df)
    global dollors
    dollors=f"${output[0]:.2f}"
    print(dollors)
    return dollors

with st.sidebar:
        select=option_menu( menu_title=None,
            options=['Fare_Amount_Prediction'])
# def Home_Page():
#     st.sidebar.markdown("Home")
    # original_title = '<p style="font-family:Courier; color:White; font-size: 60px;">NYC Cab Booking</p>'
    # st.markdown(original_title, unsafe_allow_html=True)
    # c1,c2=st.columns(2)
    # with c1:

    #     image = Image.open("cab.png")
    #     st.image(image)   
    
    # info1,info2=st.columns(2)
    # with info2:
    #     pass
    # info3,info4,info5=st.columns(2) 
    # with info4:
    #     st.button("Get Started -->")
        
    

def Objective():
    st.title("Predict Fare Amount")     
    pickup_point = st.multiselect(
    'Enter Pickup Point',Location_list,key="pickpoint")

    dropoff_point = st.multiselect(
    'Enter Drop-off Point',Location_list,key="droppoint") 



    col1,col2,col3,col4,col5=st.columns(5)

    passenger_count=st.number_input("Enter total Passenger",min_value=1,max_value=4)

    with col1:
        book_date  = st.date_input("Select Booking Date ",datetime.datetime.now().date())

    with col2:
        pass

    with col3:
        clock_time = st.time_input('Enter time')

    if(len(pickup_point)==0):
        pass
    elif(len(dropoff_point)==0):
        pass
    elif(len(pickup_point)>=2 or len(dropoff_point)>=2):
        st.error("PLease Select Only One Pickup and Drop-off Location !!")
    elif dropoff_point==pickup_point:
        st.error("PLease Enter Correct Pickup and Dropoff Location !!")
    else:
        col4,col5,col6=st.columns(3)

        with col4:
            pass

        input_data=clock_time,book_date,pickup_point,dropoff_point,passenger_count
        with col5:
            is_click = st.button("Predict", key="loading",on_click=function,args=input_data)
            st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(246, 51, 102);te } </style>""", unsafe_allow_html=True)
            if is_click:
                st.metric(label="Fare Amount", value=function(clock_time,book_date,pickup_point,dropoff_point,passenger_count))               
                


 #Page 1
if select=='Home':
    Home_Page()
    
        
#Page 2
if select=='Fare_Amount_Prediction':
    Objective()

    


# gmapOne = gmplot.GoogleMapPlotter(40.7237, -73.9825,14)
# x1 = getdata(pickup_point,zip_p)[0]
# y1 = getdata(pickup_point,zip_p)[1]

# x2 = getdata(dropoff_point,zip_d)[0]
# y2 = getdata(dropoff_point,zip_d)[1]

# lat = [x1,x2]
# lng = [y1,y2]

# # print(lat)
# # print(lng)

# gmapOne.scatter(lat,lng,'#ff000',size=50,marker=False)
# gmapOne.plot(lat,lng,'blue',edge_width=3.5)
# gmapOne.draw('path2.html')

# st.title("Map api") 
# components.iframe("file:///C:/Users/Harshita/Desktop/Project-Review-1-NYC/path2.html",width=900,height=1200)









