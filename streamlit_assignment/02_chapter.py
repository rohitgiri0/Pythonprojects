#importing required modules
import streamlit as st
import time
from datetime import date

#title
st.title("Nothing Before Coffee")   
 
#checkbox
choco=st.checkbox("Add Chocolate")

# condition on checkbox
if choco:
    st.success("chocolate added") 
    
#radio buttons
coffee_types=st.radio("select your coffee base: ",["milk","water"])

#selection box
flavour=st.selectbox("choose flavour: ",["Hazelnut","Vanila","Butterstoch","Classic"])

#slider
sugar=st.slider("select sugar quantity: ",0,5,2)

#number input
cups=st.number_input("select how many cups you want: ",min_value=1,max_value=10)

#text input
name=st.text_input("enter your name: ")
name=name.capitalize()

#date input
birthdate=st.date_input(value=date(2000,1,1),label="enter your birthday to availing special discounts",min_value=date(1900,1,1),max_value="today")

#todays date
today=date.today()

#condition on dates
if (birthdate.month,birthdate.day)==(today.month,today.day):
    st.success(f"Happy birthday {name} 🎂 you won a free coffee🥳")

#feedback taking and showing success message
feedback=st.text_input("we'd be soo grateful if you leave a review for us")
if feedback:
    st.success("feedback posted successfully")

#all info what user selected
st.subheader("Your Coffee") 
choco_status=(lambda: 'Added' if choco else 'Not added')()
st.write(f"chocolate : {choco_status}")
st.write(f"selected base : {coffee_types}")
st.write(f"flavour: {flavour}")
st.write(f"sugar added : {sugar} spoons")
st.write(f"we are prepairing {cups} for you😊")

#button for making coffee
if st.button("make coffee"):
# using condition for slow down the process of making coffee
    if choco:
        time.sleep(5)
        st.success("your coofee is ready with chocolate!")
    
    else:
        time.sleep(5)
        st.success("your coofee is ready!")
        
#the end 