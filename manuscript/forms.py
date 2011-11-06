from django import forms
from manuscript.models import Paragraph, Title, Page, Chapter

class BigSearchForm(forms.Form):
	q = forms.CharField(max_length=1000, label="What are you looking for?",
	    widget=forms.TextInput(attrs={"class":"search-entry-field"}),
	)
	titles = forms.ModelMultipleChoiceField(queryset=Title.objects_with_data.all(), label="Where are you looking for it?", required=False)
	nearprompt = forms.IntegerField(min_value=1, max_value=100, required=False, label="Near by how many words?")

	def clean_q(self):
		q = self.cleaned_data["q"]
		
		# There are a few search operators that we want to disallow.

		return q