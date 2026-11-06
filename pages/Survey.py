# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.
import csv

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    brand_input = st.selectbox("Select your main computer's GPU brand:", ["NVIDIA", "AMD", "APPLE", "INTEL", "NOT LISTED"])
    budget_input = st.text_input("Enter your budget in USD:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:

        budget_clean = budget_input.strip()
        if not budget_clean.isdecimal():
            st.error("Please enter a valid budget")
        else:
            budget_value = int(budget_clean)
            if budget_value < 1 or budget_value > 10000:
                st.error("Please enter a value between 1 and 10000")
            else:
                with open("data.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([brand_input, budget_value])

                st.success("Your data has been submitted!")
                st.write(f"You entered: **Brand:** {brand_input}, **Budget:** {budget_value}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")