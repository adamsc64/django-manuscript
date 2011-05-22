from django import forms

from Wyclif.models import Paragraph, Title, Page, Chapter

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
