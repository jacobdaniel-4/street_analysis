import streamlit as st
import requests

# Function to get activity
def get_activity(activity_type=None, accessibility=None, participants=None):
    url = "http://bored.api.lewagon.com/api/activity/"
    
    # Prepare parameters for the request
    params = {}
    if activity_type:
        params['type'] = activity_type.lower()
    if accessibility is not None:
        params['accessibility'] = accessibility
    if participants is not None:
        params['participants'] = participants
    
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
            
            participants = st.number_input(
                "Number of participants:", min_value=1, max_value=10, value=1, step=1
            )
        
        with col2:
            accessibility = st.slider(
                "Accessibility level:",
                0.0, 1.0, step=0.1, help="0 for highly accessible (easy), 1 for least accessible (challenging)"
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
    activity = get_activity(activity_type, accessibility, participants)
    
    # Display the result in a styled box
    st.success(f"🎉 **{activity}**")

# Footer
st.write("---")
st.markdown("#### Created by [Your Name](https://www.yourportfolio.com) | Powered by the Bored API")
