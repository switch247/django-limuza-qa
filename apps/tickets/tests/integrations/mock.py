import json
from datetime import datetime, timedelta

# Mock response class
class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

# Load mock data from JSON files
def load_mock_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Mock API call to fetch tickets including conversations
def mock_api_call_to_fetch_tickets(api_key, url, last_updated_at):
    tickets = load_mock_data('mock_tickets.json')['tickets']
    conversations = load_mock_data('mock_conversations.json')['conversations']

    # Filter tickets based on last_updated_at
    filtered_tickets = [
        ticket for ticket in tickets
        if datetime.strptime(ticket['updated_at'], '%Y-%m-%dT%H:%M:%SZ') > last_updated_at
    ]

    # Attach conversations to the tickets
    for ticket in filtered_tickets:
        ticket['conversations'] = [
            conversation for conversation in conversations
            if conversation['ticket_id'] == ticket['id']
        ]

    return MockResponse({"tickets": filtered_tickets})

# Mock API call to fetch agents
def mock_api_call_to_fetch_agents(api_key, url):
    agents = load_mock_data('mock_agents.json')['agents']
    return MockResponse({"agents": agents})

# Updated service methods to use the mock methods
def get_agents(integration):
    response = mock_api_call_to_fetch_agents(integration.details['api_key'], integration.details['url'])
    if response.status_code == 200:
        agents = response.json().get('agents', [])
        return agents
    return []

def get_tickets(integration, last_updated_at=None):
    if last_updated_at is None:
        last_updated_at = datetime.now() - timedelta(days=1)
    response = mock_api_call_to_fetch_tickets(integration.details['api_key'], integration.details['url'], last_updated_at)
    if response.status_code == 200:
        tickets = response.json().get('tickets', [])
        return tickets
    return []
