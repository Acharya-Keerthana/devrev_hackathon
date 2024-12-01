from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

# API Endpoints
WORKS_API_URL = "https://api.devrev.ai/works.list"
CONVERSATIONS_API_URL = "https://api.devrev.ai/conversations.list"

# Authentication
API_KEY = os.getenv("PERSONAL_ACCESS_TOKEN")  # Replace with your actual API key

# Headers for Authentication
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def fetch_all_data(api_url):
    all_data = []
    params = {}
    
    while True:
        response = requests.get(api_url, headers=HEADERS, params=params)
        
        if response.status_code != 200:
            print(f"Failed to fetch data from {api_url}. Status Code: {response.status_code}")
            print("Response:", response.text)
            break
        
        data = response.json()
        all_data.extend(data.get('works', []) if 'works' in data else data.get('conversations', []))
        
        # Check for pagination (assuming 'next_cursor' is used)
        next_cursor = data.get('next_cursor')
        if next_cursor:
            params['cursor'] = next_cursor
        else:
            break
    
    return all_data

def main():
    # Fetch all works (tickets and possibly other types)
    works = fetch_all_data(WORKS_API_URL)
    
    # Filter only tickets
    tickets = [work for work in works if work.get('type') == 'ticket']
    print(f"Total Tickets Retrieved: {len(tickets)}")
    
    # Fetch all conversations
    conversations = fetch_all_data(CONVERSATIONS_API_URL)
    print(f"Total Conversations Retrieved: {len(conversations)}")
    
    # Link tickets to conversations
    linked_data = []
    
    for ticket in tickets:
        ticket_id = ticket.get('id', '')
        ticket_title = ticket.get('title', '')
        
        for conversation in conversations:
            conversation_id = conversation.get('id', '')
            conversation_stage = conversation.get('stage', {}).get('name', '')
            
            for message in conversation.get('messages', []):
                message_body = message.get('body', '')
                if ticket_id in message_body:
                    linked_data.append({
                        "ticket_id": ticket_id,
                        "ticket_title": ticket_title,
                        "conversation_id": conversation_id,
                        "conversation_stage": conversation_stage
                    })
    
    print(f"Total Linked Entries: {len(linked_data)}")
    
    # Save linked data to a JSON file
    with open('linked_data.json', 'w') as outfile:
        json.dump(linked_data, outfile, indent=4)
    
    print("Linked data has been saved to 'linked_data.json'")

if __name__ == "__main__":
    main()
