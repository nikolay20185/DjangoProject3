from django import forms
from .models import Discussion, Reply


class DiscussionForm(forms.ModelForm):
    """
    Form for creating and editing discussions.
    """
    class Meta:
        model = Discussion
        fields = ['title', 'topic', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок обсуждения'}),
            'content': forms.Textarea(attrs={
                'rows': 8, 
                'placeholder': 'Поделитесь своим вопросом или мыслями...'
            })
        }


class ReplyForm(forms.ModelForm):
    """
    Form for creating replies to discussions.
    """
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 5, 
                'placeholder': 'Ваш ответ...'
            })
        }


class DiscussionSearchForm(forms.Form):
    """
    Form for searching discussions.
    """
    query = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск обсуждений...'})
    )
    topic = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Все темы"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Topic
        self.fields['topic'].queryset = Topic.objects.all() 