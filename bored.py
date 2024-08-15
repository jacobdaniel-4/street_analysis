import streamlit as st
import requests

def get_activity():
    url = "http://bored.api.lewagon.com/api/activity/"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('activity', 'No activity found')
    else:
        return "Failed to fetch activity"

# Streamlit app layout
st.title("Bored? Let's Find You an Activity!")

# Create a simple button to trigger the activity fetch
if st.button("Get Activity"):
    activity = get_activity()
    st.write(f"Suggested activity: {activity}")
