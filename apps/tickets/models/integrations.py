from django.db import models
from django.contrib.auth import get_user_model
from apps.customer_accounts.models import Workspace, TenantClass, TenantForeignKey  # Import the Workspace model
from django.conf import settings
from django.db import models
import os
import yaml

User = get_user_model()

class Integration(TenantClass):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    integration_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    workspace = TenantForeignKey(Workspace, on_delete=models.CASCADE, related_name='integrations')  # Added Workspace relationship
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)
    details = models.JSONField(default=dict) 

    def __str__(self):
        return self.name

    def parse_ticket_data(self, raw_data):
        raise NotImplementedError("Subclasses must implement this method")

    def fetch_tickets(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def load_filterable_fields(self):
        # Construct the file path based on the model's class name
        file_path = os.path.join('apps', 'tickets', 'filters', f'{self.__class__.__name__}.yaml')
        
        # Load the standard fields from the YAML file
        with open(file_path, 'r') as file:
            standard_fields = yaml.safe_load(file)
        
        # Get custom fields from the integration details
        custom_fields = self.details.get('custom_fields', [])

        # Merge standard and custom fields
        fields = standard_fields.get(f'{self.__class__.__name__}').get('fields')
        fields.extend(custom_fields)
        
        return fields
    
    @classmethod
    def create_from_json(cls, json_data, user=None):
        integration = cls(
            name=json_data.get('name'),
            type=json_data.get('type'),
            integration_key=json_data.get('integration_key'),
            workspace=user.workspace if user else None,
            created_by=user,
            active=json_data.get('active', True),
            details=json_data.get('details', {})
        )
        integration.save()
        return integration

class FreshdeskIntegration(Integration):
    def parse_ticket_data(self, raw_data):
        parsed_data = {
            "subject": raw_data.get("subject"),
            "status": raw_data.get("status"),
            "created_at": raw_data.get("created_at"),
            "updated_at": raw_data.get("updated_at"),
            "html_ticket": raw_data.get("description"),
            "text_ticket": raw_data.get("description_text"),
            "ticket_data": raw_data
        }
        return parsed_data

# Similarly, define other CRM-specific integration classes here
#TODO need methods to fetch regularly. Note that we should always aim to use the updated_at field as an indicator from the CRMs side of what to pull
#TODO create a fake integration for testing
class SavedFilter(TenantClass):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    integration = TenantForeignKey(Integration, on_delete=models.CASCADE)
    filter_data = models.JSONField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

