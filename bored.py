import requests

def get_activity():
    url = "https://bored.api.lewagon.com/api/activity/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Suggested activity: {data['activity']}")
    else:
        print("Failed to fetch activity")

if __name__ == "__main__":
    get_activity()
