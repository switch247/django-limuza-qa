from django import forms
from .models import *

class SelectScorecardForm(forms.Form):
    scorecard = forms.ModelChoiceField(queryset=Scorecard.objects.all(), required=True,initial=0)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}),
        }

    def __init__(self, *args, **kwargs):
        review_data = kwargs.pop('review_data', [])
        super().__init__(*args, **kwargs)

        for item in review_data:
            if isinstance(item, ReviewCategory):
                category = item.scorecard_category.category.to_json()
                score = item.score
                na = item.na
            else:
                category = item.category.to_json()
                score = None
                na = item.category.allow_na

            field_name = f'category_{category["id"]}'
            try:
                scale_limit = int(category['scale'][0])
            except (ValueError, TypeError):
                scale_limit = 7  # Default scale limit if parsing fails

            self.fields[field_name] = forms.IntegerField(
                label=category['name'],
                initial=score,
                required=not category['allow_na'],
                widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'step': 25, 'class': 'range w-full'})
            )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'scale', 'allow_na']
        widgets = {
            'scale': forms.Select(choices=Category.SCALE_CHOICES),
        }

class ScorecardForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Scorecard
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weight_fields = {}
        for category in self.fields['categories'].queryset:
            field_name = f'weight_{category.id}'
            self.fields[field_name] = forms.FloatField(
                initial=1.0,
                required=False,
                label=f'Weight for {category.name}'
            )
            self.weight_fields[category.id] = self[field_name]

class ScorecardCategoryForm(forms.ModelForm):
    class Meta:
        
        model = ScorecardCategory
        fields = ['category', 'weighting']
        widgets = {
            'weighting': forms.NumberInput(attrs={'step': 0.1, 'min': 0, 'max': 10}),
        }

class AssignmentRuleForm(forms.ModelForm):
    class Meta:
        model = AssignmentRule
        fields = ['name', 'reviewers', 'description', 'criteria']
        widgets = {
            'reviewers': forms.CheckboxSelectMultiple,
        }

class TicketAssignmentForm(forms.ModelForm):
    class Meta:
        model = TicketAssignment
        fields = ['assignment_rule', 'reviewer', 'reviews', 'start_date', 'end_date']
        widgets = {
            'assignment_rule': forms.Select(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-80 text-sm bg-base-300',
                'placeholder': 'Assignment Rule'
            }),
            'reviewer': forms.Select(attrs={
                'class': 'rounded-lg p-3 border border-base-100 block w-80 text-sm bg-base-300'
            }),
            'reviews': forms.CheckboxSelectMultiple(attrs={
                'class': 'rounded-lg'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'rounded-lg p-3 bg-base-300 border border-base-100 block w-60 text-sm pl-10',
                'placeholder': 'Select date',
                'datepicker': 'true'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'rounded-lg p-3 bg-base-300 border border-base-100 block w-60 text-sm pl-10',
                'placeholder': 'Select date',
                'datepicker': 'true'
            }),
        }

