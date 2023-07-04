from django import forms
from .models import Ticket, Conversation, ConversationEmail, ConversationCall, ConversationChat
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'external_id',
            'subject',
            'integration',
            'external_agent_id',
            'agent',
            'created_at',
            'status',
            'ticket_data',
            'html_ticket',
            'text_ticket'
        ]
        widgets = {
            'external_id': forms.NumberInput(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300',
                'placeholder': 'Externail ID'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300',
                'placeholder': 'Externail ID'
            }),
            'integration':  forms.Select(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300'
            }),
            'external_agent_id':  forms.NumberInput(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300',
                'placeholder': 'Externail Agent ID'
            }),
            'agent':  forms.Select(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300'
            }),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300'}),
            'status': forms.Select(choices=[
                ('open', 'Open'),
                ('pending', 'Pending'),
                ('resolved', 'Resolved'),
                ('closed', 'Closed')
            ], attrs={'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300'}),
            'ticket_data':  forms.Textarea(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300 min-h-40'
            }),
            'html_ticket':  forms.Textarea(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300 min-h-40'
            }),
            'text_ticket':  forms.Textarea(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-full text-sm bg-base-300 min-h-40'
            }),
        }

class ConversationEmailForm(forms.ModelForm):
    class Meta:
        model = ConversationEmail
        fields = [
            'external_id',
            'external_agent_id',
            'ticket',
            'incoming',
            'private',
            'source',
            'agent',
            'body',
            'body_text',
            'from_email', # If you have any additional fields in the base model
        ]

class ConversationCallForm(forms.ModelForm):
    class Meta:
        model = ConversationCall
        fields = [
            'external_id',
            'external_agent_id',
            'ticket',
            'incoming',
            'private',
            'source',
            'agent',
            'body',
            'body_text',
            'call_recording',
            'call_transcription'  # If you have any additional fields in the base model
        ]

class ConversationChatForm(forms.ModelForm):
    class Meta:
        model = ConversationChat
        fields = [
            'external_id',
            'external_agent_id',
            'ticket',
            'incoming',
            'private',
            'source',
            'agent',
            'body',
            'body_text',
            'chat_platform' # If you have any additional fields in the base model
        ]

class DynamicTicketFilterForm(forms.Form):
    # this form needs to get all the filterable fields of a ticket integration and allow selection to build the filter
    # the form should allow the user to choose a type of filter for each field. For example, the timestamp field should
    # give the option of on/between/before/after and string field should give the option of contains/starts with/ends with/does not contain
    # and integer field should give the option of equals/less than/greater than/less than or equal to/greater than or equal to
    STRING_FILTER_CHOICES = [
        ('contains', 'Contains'),
        ('starts_with', 'Starts with'),
        ('ends_with', 'Ends with'),
        ('does_not_contain', 'Does not contain'),
        ('is', 'Is'),
    ]

    TIMESTAMP_FILTER_CHOICES = [
        ('on', 'On'),
        ('between', 'Between'),
        ('before', 'Before'),
        ('after', 'After'),
        ('is', 'Is'),
    ]

    INTEGER_FILTER_CHOICES = [
        ('equals', 'Equals'),
        ('less_than', 'Less than'),
        ('greater_than', 'Greater than'),
        ('less_than_or_equal', 'Less than or equal to'),
        ('greater_than_or_equal', 'Greater than or equal to'),
        ('is', 'Is'),
    ]

    ARRAY_FILTER_CHOICES = [
        ('contains_any', 'Contains any of'),
        ('contains_all', 'Contains all of'),
        ('is', 'Is'),
    ]

    LOOKUP_MAPPING = {
        'contains': 'icontains',
        'starts_with': 'istartswith',
        'ends_with': 'iendswith',
        'does_not_contain': 'icontains',  # This will be negated in the logic
        'is': 'exact',
        'equals': 'exact',
        'less_than': 'lt',
        'greater_than': 'gt',
        'less_than_or_equal': 'lte',
        'greater_than_or_equal': 'gte',
        'on': 'exact',
        'before': 'lt',
        'after': 'gt',
        'between': 'range',
        'contains_any': 'contains_any',  # Custom lookup for arrays
        'contains_all': 'contains_all',  # Custom lookup for arrays
    }

    def __init__(self, *args, **kwargs):
        integration = kwargs.pop('integration')
        super().__init__(*args, **kwargs)
        
        filterable_fields = integration.load_filterable_fields()
        if not filterable_fields:
            raise Exception('must have filterable fields!')

        for field in filterable_fields:
            field_name = field['name']
            field_type = field['type']
            
            if field_type == 'string':
                self.fields[field_name] = forms.CharField(required=False)
                self.fields[f'{field_name}_filter_type'] = forms.ChoiceField(
                    choices=self.STRING_FILTER_CHOICES, required=False)
            elif field_type == 'timestamp':
                self.fields[field_name] = forms.DateTimeField(required=False)
                self.fields[f'{field_name}_filter_type'] = forms.ChoiceField(
                    choices=self.TIMESTAMP_FILTER_CHOICES, required=False)
                self.fields[f'{field_name}_end'] = forms.DateTimeField(
                    required=False)  # For 'between' filter type
            elif field_type == 'integer':
                self.fields[field_name] = forms.IntegerField(required=False)
                self.fields[f'{field_name}_filter_type'] = forms.ChoiceField(
                    choices=self.INTEGER_FILTER_CHOICES, required=False)
            elif field_type == 'array':
                self.fields[field_name] = forms.CharField(required=False)  # Assuming a comma-separated list input
                self.fields[f'{field_name}_filter_type'] = forms.ChoiceField(
                    choices=self.ARRAY_FILTER_CHOICES, required=False)
            else:
                raise Exception(f'Unsupported field type: {field_type}')
            # Add more types as needed

    def get_filters(self):
        filters = Q()
        for name, value in self.cleaned_data.items():
            if name.endswith('_filter_type') or name.endswith('_end'):
                continue
            if value:
                filter_type = self.cleaned_data.get(f'{name}_filter_type')
                if filter_type:
                    lookup = self.LOOKUP_MAPPING.get(filter_type)
                    if filter_type == 'does_not_contain':
                        filters &= ~Q(**{f'{name}__{lookup}': value})
                    elif filter_type == 'between':
                        end_value = self.cleaned_data.get(f'{name}_end')
                        if end_value:
                            filters &= Q(**{f'{name}__{lookup}': (value, end_value)})
                    elif filter_type in ['contains_any', 'contains_all']:
                        values = value.split(',')  # Assuming comma-separated input for arrays
                        if filter_type == 'contains_any':
                            filters &= Q(**{f'{name}__overlap': values})
                        elif filter_type == 'contains_all':
                            filters &= Q(**{f'{name}__contains': values})
                    else:
                        filters &= Q(**{f'{name}__{lookup}': value})
                else:
                    filters &= Q(**{name: value})
        return filters