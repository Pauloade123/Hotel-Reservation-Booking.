import pandas as pd
import streamlit as st
import joblib

model = joblib.load('model.pkl')

st.markdown("""
    <style>
        .stApp {
            background-color: #5f4d30;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center; color: #fc3804;'>HOTEL RESERVATION PREDICTOR</h1>",
    unsafe_allow_html=True
)
st.markdown("""
    <p style='text-align: center; color: white; font-size: 18px; margin: auto; display: block;'>
        Enter customer details below to predict if bookings will be cancelled or not.
    </p>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #fc3804;'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    no_of_adults = st.number_input("Number of adults booked", min_value=1, max_value=4)
    no_of_children = st.number_input('Number of children booked', min_value=0, max_value=10)
    no_of_weekend_nights = st.number_input('Number of weeked Nights booked', min_value=0,  max_value=7)
    no_of_week_nights = st.number_input('Number of weeek nights', min_value=0, max_value=17)
    type_of_meal_plan = st.number_input('Type of meal plan booked', min_value=0, max_value=3)
    required_car_parking_space = st.selectbox('Required Parking Space', ['No', 'Yes'])
    room_type_reserved = st.number_input('Room Type Booked', min_value=0, max_value=6)

with col2:
    lead_time = st.number_input('Lead Time', min_value=0)
    market_segment_type = st.number_input('Market Segment Type Booked', min_value=0, max_value=4)
    repeated_guest = st.selectbox('Repeated Guest', ['No', 'Yes'])
    no_of_previous_cancellations = st.number_input('Number of Previous Cancellations', min_value=0, max_value=13)
    no_of_previous_bookings_not_canceled = st.number_input('Number Of Previous Bookings Not Canceled', min_value=0, max_value=58)
    avg_price_per_room = st.number_input('Average price Per Room($)', min_value=23.0, max_value=180.0)
    no_of_special_requests = st.number_input('Number Of Special Request', min_value=0, max_value=5)

if required_car_parking_space == 'Yes':
    required_car_parking_space = 1
else:
    required_car_parking_space = 0

if repeated_guest == 'Yes':
    repeated_guest = 1
else:
    repeated_guest = 0

if st.button('predict'):
    input_data = pd.DataFrame([[no_of_adults, no_of_children, no_of_weekend_nights,
       no_of_week_nights, type_of_meal_plan, required_car_parking_space,
       room_type_reserved, lead_time, market_segment_type,
       repeated_guest, no_of_previous_cancellations,
       no_of_previous_bookings_not_canceled, avg_price_per_room,
       no_of_special_requests]])
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    booking_probability = round(probability[0][1] * 100, 2)

    if prediction[0] == 1:
        st.error(f"⚠️ This customer is likely to cancel bookings ({booking_probability}% probabilty)")
    else:
        st.success(f'✅ This customer is not likely to cancel bookings. ({booking_probability}% probability)')
