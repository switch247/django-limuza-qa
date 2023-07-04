from apps.tickets.models import Ticket, Conversation
from apps.reviews.models import Scorecard, Category, ScorecardCategory, Review, TicketReview, ConversationReview, ReviewCategory

from apps.tickets.models.integrations import Integration
from apps.test_utils import *

def seeder():
    user, workspace, integration = get_dummy_integration()
    agents = MockCRM.get_mock_agents(integration)
    for agent_data in agents:
        User.objects.create(
            username=agent_data['contact']['name'],
            email=agent_data['contact']['email'],
            external_id=agent_data['id'],
            password='password'  # or use a more secure way to set passwords
        )
    new_tickets = MockCRM.get_mock_tickets(integration)
    for ticket_data in new_tickets:
        user = User.objects.get(external_id=ticket_data['responder_id'])
        ticket = Ticket.objects.create(
            external_id=ticket_data['id'],
            external_agent_id=ticket_data['responder_id'],
            subject=ticket_data['subject'],
            agent = user,
            created_at=datetime.strptime(ticket_data['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
            status=ticket_data['status'],
            ticket_data=ticket_data,
            html_ticket="<p>Test HTML</p>",
            text_ticket="Test Text",
            integration=integration
        )
        for conversation in ticket_data['conversations']:
            Conversation.objects.create(
                ticket=ticket,
                agent = user,
                incoming=conversation['incoming'],
                private=conversation['private'],
                source=conversation['source'],
                external_agent_id=conversation['user_id'],
                body=conversation['body'],
                body_text=conversation['body_text'],
                from_email=conversation['from_email'],
                additional_data=conversation,
                external_id = conversation['id']
            )
    Scorecard.objects.create(name='Test Scorecard', created_by=user, account_id='account1')
    Category.objects.create( name='Tone', scale='3_point', allow_na=True)
    Category.objects.create( name='Spelling', scale='binary', allow_na=False)

    print('seed complete')