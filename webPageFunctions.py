from datetime import datetime, timedelta
import math
import json

def create_poll(event):
    try:
        with open('poll_links.json', 'r') as file:
            data = json.load(f)

        # Iterate through each poll entry
        given_date = datetime.now() + timedelta(days=1)
        given_duration=round(int(event['duration']))
        for poll in data:
            # Check if the start date and duration match
            if poll["start_date"] == given_date.strftime("%Y-%m-%d") and poll["duration"] == given_duration:
                # Extract links
                public_link = poll["public_link"]
                admin_link = poll["admin_link"]
                
                # Delete the matching entry
                data.remove(poll)
                
                print("Matching poll found and deleted.")
                
                # Save the updated list back to the JSON file
                with open('poll_links.json', 'w') as f:
                    json.dump(data, f, indent=4)
                
                # Return the links
                return public_link, admin_link
        


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
