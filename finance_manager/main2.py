import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import os
import plotly.express as px


st.set_page_config("Money Management",page_icon="💰",layout="wide")
st.title("Bank Finance Manager")

# success=True # temp delete when all done

#login

side=st.sidebar
name=side.text_input("Enter your name")
email=side.text_input("Enter your email address",placeholder="exp@gmail.com")
phone=side.text_input("enter your phone number")
np.random.seed(42)
success=False
if (len(phone)==10):
    otp=np.random.randint(low=1000,high=9999,size=1)
    side.write(otp[0])
    entered_pass=side.text_input("this is your password enter this password to continue")
    if (entered_pass and name and email):
        if int(otp[0]) == int(entered_pass):
            success=side.success("you've logged in successfully")
            if success:
                success=True
    else:
        side.write("Please fill all the values")
        
if success:
    st.subheader("Welcome to SBI")
    if "sleep_done" not in st.session_state:
        st.write("please wait for 10 min , it's lunch time")
        time.sleep(10)
        st.session_state.sleep_done = True



categories_json="categories.json"
if "categories" not in st.session_state:
    st.session_state.categories={
        "uncategorized":[]
    }

if os.path.exists(categories_json):
    with open(categories_json,'r') as f:
        st.session_state.categories=json.load(f)

def save_categories():
    with open(categories_json,'w') as f:
        json.dump(st.session_state.categories,f)
        
def categorised_trx(df):
    df["Category"]="uncategorized"
    for category, keywords in st.session_state.categories.items():
        if category=="uncategorized" or not keywords:
            continue
        lowered_keywords=[keyword.lower().strip() for keyword in keywords]
        print(df.loc[0])
        for idx,row in df.iterrows():
            details=row['Description'].lower().strip()
            if any(keyword in details for keyword in lowered_keywords):
                df.at[idx,"Category"]=category

    return df

def add_keyword_in_category(category,keyword):
    keyword=keyword.strip()
    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    return False

def load_file(file):
    try:
        df=pd.read_csv(file)
        df.columns=[col.strip() for col in df.columns]
        df["Date"]=df["Date"].str.replace("-"," ")
        df["Date"]=pd.to_datetime(df["Date"],format=("%d %b %y"))
        return categorised_trx(df)
    except Exception as e:
        st.error(f"Error in Processing {e}")
        return None

if success:
    st.subheader("Welcome to your own Finance App")
    uploaded_file=st.file_uploader("upload your bank statement here")
    if uploaded_file is not None:
        df=load_file(uploaded_file)

        if df is not None:
            # Clean up Debit and Credit columns
            df["Debit"]=df["Debit"].astype(str).str.replace(r"[^\d.]","",regex=True).replace("","0").astype(float)
            df["Credit"] = df["Credit"].astype(str).str.replace(r"[^\d.]", "", regex=True).replace("", "0").astype(float)            

            # Split into debit and credit transactions
            debit_df = df[df["Debit"] > 0].copy()
            credit_df = df[df["Credit"] > 0].copy()
            
            st.session_state.debit_df=debit_df.copy()
            
            tab1,tab2=st.tabs(["Expenses(Debit)","Payments(Credit)"])

            with tab1:
                new_category=st.text_input("New category name")
                submit=st.button("add category")
                if submit and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category]=[]
                        save_categories()
                        st.rerun()
                # st.write(debit_df[["Date","Description","Ref No./Cheque No.","Debit","Balance","Category"]]) 
                
                st.subheader("Your expenses")
                edited_df=st.data_editor(
                    st.session_state.debit_df[["Date","Description","Debit","Category"]],
                
                column_config={
                    "Date" : st.column_config.DateColumn("Date",format="DD/MM/YYYY"),
                    "Description" : st.column_config.TextColumn("Details",width="medium",),
                    "Debit": st .column_config.NumberColumn("Amount",width="small",format="%.2f INR"),
                    "Category": st.column_config.SelectboxColumn("Category",options=list(st.session_state.categories.keys()))
                },
                hide_index=True,
                use_container_width=True,
                key="category_editor"
                )
                save_button=st.button("Apply Changes",type="primary")
                if save_button:
                    for idx, row in edited_df.iterrows():
                        new_category=row["Category"]
                        if new_category==st.session_state.debit_df.at[idx,"Category"]:
                            continue
                        details=row["Description"]
                        st.session_state.debit_df.at[idx,"Category"]=new_category
                        add_keyword_in_category(new_category,details)
                    

                # Expense Summary and Pie Chart (always visible)
                st.session_state.debit_df["Balance"] = pd.to_numeric(st.session_state.debit_df.get("Balance", 0), errors="coerce").fillna(0)
                category_total = st.session_state.debit_df.groupby("Category")["Debit"].sum().reset_index()
                category_total = category_total.sort_values("Debit", ascending=False)

                st.subheader("Expense Summary")
                st.dataframe(
                    category_total,
                    column_config={
                        "Debit": st.column_config.NumberColumn("Amount", format="%.2f INR")
                    },
                    use_container_width=True,
                    hide_index=True
                )

                fig = px.pie(
                    category_total,
                    values="Debit",
                    names="Category",
                    title="Expenses by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
            with tab2:
                st.subheader("Payment summary")
                total_payemet=credit_df["Credit"].sum()
                st.write(f"Total Payment {total_payemet:.2f} INR")
                
                st.dataframe(
                    credit_df,
                    column_config={
                        "Date": st.column_config.DateColumn("Date",format=("DD/MM/YYYY")),
                        "Description": st.column_config.TextColumn("Details",width="medium"),
                        "Credit": st.column_config.NumberColumn("Amount",width="small",format="%.2f INR"),
                        "Balance": st.column_config.NumberColumn("Balance"),
                        "Category": st.column_config.TextColumn("Category")
                    },
                    use_container_width=True,
                    hide_index=True
                )
