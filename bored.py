import streamlit as st
import requests

# Function to get activity
def get_activity(activity_type=None, price=None):
    url = "http://bored.api.lewagon.com/api/activity/"
    
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
st.set_page_config(page_title="Boredom Buster", page_icon=":sunglasses:", layout="centered")

# App title
st.title("Bored? Let’s Find You an Activity!")
st.markdown("### Get personalized suggestions based on your preferences.")

# Styling container
with st.container():
    st.write("---")
    
    # Create a form for user input
    st.subheader("Choose your preferences:")
    
    with st.form(key='activity_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            activity_type = st.selectbox(
                "Activity type:",
                options=["Any", "Recreational", "Education", "Social", "DIY", "Charity", "Cooking", "Relaxation", "Music", "Busywork"]
            )
        
        with col2:
            price = st.slider(
                "Maximum price:",
                0.0, 1.0, step=0.1, help="0 for free activities, 1 for most expensive"
            )
        
        # Submit button
        submit_button = st.form_submit_button(label="Find Activity", help="Click to get your activity suggestion")
    
    st.write("---")

# Fetch and display the activity
if submit_button:
    st.subheader("Your Activity Suggestion:")
    
    # Adjust activity_type for the API
    activity_type = None if activity_type == "Any" else activity_type
    
    # Get activity from the API
    activity = get_activity(activity_type, price)
    
    # Display the result in a styled box
    st.success(f"🎉 **{activity}**")

# Footer
st.write("---")
st.markdown("#### Created by [Resources For Parents LLC](https://www.yourportfolio.com) |")

