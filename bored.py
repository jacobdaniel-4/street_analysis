import streamlit as st
import requests

def get_activity(activity_type=None, price=None):
    url = "https://www.boredapi.com/api/activity/"
    
    # Prepare parameters for the request
    params = {}
    if activity_type:
        params['type'] = activity_type.lower()
    if price is not None:
        params['price'] = price
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('activity', 'No activity found')
    else:
        return "Failed to fetch activity"

# Streamlit app layout
st.title("Bored? Let's Find You an Activity!")

# Create a form for user input
with st.form(key='activity_form'):
    activity_type = st.selectbox(
        "Choose activity type:",
        options=["Any", "Recreational", "Education", "Social", "DIY", "Charity", "Cooking", "Relaxation", "Music", "Busywork"]
    )
    
    price = st.slider(
        "Select maximum price (0 for free, 1 for most expensive):",
        0.0, 1.0, step=0.1
    )
    
    # Submit button
    submit_button = st.form_submit_button(label="Get Activity")

# Once the form is submitted, fetch the activity
if submit_button:
    # Adjust activity_type for the API
    activity_type = None if activity_type == "Any" else activity_type
    
    # Get activity from the API
    activity = get_activity(activity_type, price)
    
    # Display the result
    st.write(f"Suggested activity: {activity}")
