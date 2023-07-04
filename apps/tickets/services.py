from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied
from .models import Ticket, Conversation
from apps.tickets.models.integrations import Integration, FreshdeskIntegration
from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant
from django.core.paginator import Paginator
from django.db.models import Q
import assemblyai as aai
from django.conf import settings


def process_ticket_data(external_id, subject, agent, status, ticket_data, html_ticket, text_ticket, integration):
    # ticket, created = Ticket.objects.update_or_create(
    #     external_id=external_id,
    #     defaults={
    #         'subject': subject,
    #         'agent': agent,
    #         'status': status,
    #         'ticket_data': ticket_data,
    #         'html_ticket': html_ticket,
    #         'text_ticket': text_ticket,
    #         'integration': integration,
    #         'created_at': datetime.strptime(ticket_data['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
    #         'updated_at': datetime.now()  # assuming updated_at is now
    #     }
    # )
    # return ticket, created
    return 0


def setup_crm_integration(admin_user, workspace, integration_data):
    """
    Sets up a new CRM integration.

    Args:
        admin_user (User): The admin user setting up the integration.
        workspace (Workspace): The account to associate the integration with.
        integration_data (dict): The data for the integration.

    Returns:
        Integration: The created integration.
    """
    # Check if the admin_user is an admin in the workspace
    # workspace_user = admin_user.workspaceuser
    # if not workspace_user.is_admin:
    #     raise PermissionDenied("Only admin users can set up integrations.")
    # TODO undo two lines below once tenancy is done
    if get_current_tenant() is None:
         raise PermissionDenied("Only one CRM integration can be active at a time.")
    integration_type = integration_data.get('type')
    integration_class = Integration
    if integration_type == 'freshdesk':
        integration_class = FreshdeskIntegration

    integration = integration_class.objects.create(
        name=integration_data['name'],
        type=integration_type,
        integration_key=integration_data['integration_key'],
        workspace=workspace,
        created_by=admin_user,
        active=integration_data.get('active', True),
        details=integration_data.get('details', {})
    )
    
    return integration




def get_agents(integration):
    """
    Fetch all agents from the CRM API.

    Args:
        integration (Integration): The integration object containing API details.

    Returns:
        list: A list of agents fetched from the API.
    """
    # Initialize an empty list to hold agents
    agents = []

    # Use the integration details to connect to the CRM API
    # Example: Make an API call to fetch agents
    response = api_call_to_fetch_agents(integration.details['api_key'], integration.details['url'])

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the response and extract agent data
        agents = response.json().get('agents', [])
    
    return agents

def get_tickets(integration, last_updated_at=None):
    """
    Fetch all tickets from the CRM API updated since the last_updated_at.

    Args:
        integration (Integration): The integration object containing API details.
        last_updated_at (datetime): The timestamp to fetch tickets updated since then.

    Returns:
        list: A list of tickets fetched from the API.
    """
    # Initialize an empty list to hold tickets
    tickets = []

    # Set the default last_updated_at to 24 hours ago if not provided
    if last_updated_at is None:
        last_updated_at = datetime.now() - timedelta(days=1)

    # Use the integration details to connect to the CRM API
    # Example: Make an API call to fetch tickets
    response = api_call_to_fetch_tickets(integration.details['api_key'], integration.details['url'], last_updated_at)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the response and extract ticket data
        tickets = response.json().get('tickets', [])
    
    return tickets

# Example function to simulate an API call to fetch agents
def api_call_to_fetch_agents(api_key, url):
    # Implement the actual API call logic here
    pass

# Example function to simulate an API call to fetch tickets
def api_call_to_fetch_tickets(api_key, url, last_updated_at):
    # Implement the actual API call logic here
    pass


def transcribe_call(call,redact=False,speaker_labels=True):
    """ takes in a ConversationCall and transcribes it using AssemblyAI's API.
    Later, we want to do tests with azure and whispr to compare results. We can also give the user the choice of AI model.
    """
    aai.settings.api_key = settings.ASSEMBLY_AI_API_KEY
    # we need to get the file from a restricted URL. S3 has presigned urls. This should be the same thing we do for file downloads
    # see https://dev.to/idrisrampurawala/share-your-aws-s3-private-content-with-others-without-making-it-public-4k59
    # or see https://www.assemblyai.com/blog/transcribing-audio-files-in-an-s3-bucket-with-assemblyai/
    audio_url = "https://github.com/AssemblyAI-Community/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
    # 
    config = aai.TranscriptionConfig(
    speaker_labels=speaker_labels,
    speakers_expected=2 ### hmmmmmmm
    )
    if redact:
        config.set_redact_pii(
        policies=[
            aai.PIIRedactionPolicy.person_name,
            aai.PIIRedactionPolicy.organization,
            aai.PIIRedactionPolicy.occupation,
            # TODO allow configurability of this later on
        ],
        substitution=aai.PIISubstitutionPolicy.hash,
        )
    try:
        transcript = aai.Transcriber().transcribe(audio_url, config)
    except Exception as e:
        # sentry?
        print(f"Error during transcription: {e}")
    # for testing
    transcript_string = ""
    for utterance in transcript.utterances:
        transcript_string.join(f"Speaker {utterance.speaker}: {utterance.text}\n")
    # update the conversation with the transcription
    call.call_transcription_data = transcript.utterances
    call.call_transcription = transcript_string
    # TODO write some code to determine speaker. We can probably use a simple prompt to say "given this text" 
    # is speaker 1 or 2 the agent?
    call.save()
    return transcript.utterances
    


def filter_tickets(filter_data, integration, page=1, page_size=10):
    """
    Filters tickets based on provided filter data and returns paginated results.

    Args:
        filter_data: A dictionary containing filter criteria.
        integration: The integration instance to filter tickets for.
        page: The page number for pagination.
        page_size: The number of items per page.

    Returns:
        A paginated list of filtered tickets.
    """
    filters = Q()
    for field, value in filter_data.items():
        if value:
            filters &= Q(**{field: value})
    
    tickets = Ticket.objects.filter(filters, integration=integration)
    paginator = Paginator(tickets, page_size)
    paginated_tickets = paginator.get_page(page)
    
    return paginated_tickets