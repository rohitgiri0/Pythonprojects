# required packages
import streamlit as st
import time
from datetime import date, timedelta

# title and subtitle for this web app
st.title("Age Calculator")
st.subheader("A web app made for calculating age")

# taking user input and storing todays date in a variable
dob=st.date_input("enter your birthdate: ",min_value=date(1800,1,1),max_value=date(2030,1,1))
today=date.today()

# calculating age
age=today.year-dob.year

# adjusting age if birthday hasn't happend this year
if (today.month,today.day)<(dob.month,dob.day):
    age-=1

# sleeping for 2 seconds and showing success message with calculated age, when done 
if st.button("calculate age"):
    if age:
        time.sleep(2)
        st.success("age calculated successfully")
        st.write(f"You are {age} year old")
        
        
        
# to calculate precise date using a method
# import streamlit as st
# import datetime as dt
# from  dateutil.relativedelta import relativedelta

# st.title("Age Calculate APP")
# st.subheader("Automate Calculate Age")

# date = st.date_input(
#     "Please select your birthdate:",
#     min_value=dt.date(1900, 1, 1),
#     max_value=dt.date.today()
# )
# current_date = dt.date.today()

# diff = relativedelta(current_date, date)
# st.write(f"Your age is: {diff.years} years, {diff.months} months, and {diff.days} days.")