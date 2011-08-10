# Copyright Christopher Adams, 2011
# All rights reserved.

from django import forms

from manuscript.models import Paragraph, Title, Page, Chapter

class ParagraphForm(forms.ModelForm):
	class Meta:
		model = Paragraph

class TitleForm(forms.ModelForm):
	class Meta:
		model = Title

class PageForm(forms.ModelForm):
	class Meta:
		model = Page

class ChapterForm(forms.ModelForm):
	class Meta:
		model = Chapter

class BigSearchForm(forms.Form):
	q = forms.CharField(max_length=1000, label="Search for text")
	titles = forms.ModelMultipleChoiceField(queryset=Title.objects.all(), label="In", required=False)
	nearprompt = forms.IntegerField(min_value=1, max_value=100, required=False)
