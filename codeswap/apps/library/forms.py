from django import forms
from .models import CodeSnippet, Comment, Tag


class CodeSnippetForm(forms.ModelForm):
    """
    Form for creating and editing code snippets.
    """
    tags = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Теги через запятую (например: react, animation, ui)'})
    )
    
    class Meta:
        model = CodeSnippet
        fields = ['title', 'language', 'code', 'description', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание сниппета и инструкции по использованию'}),
            'code': forms.Textarea(attrs={'rows': 10, 'class': 'code-editor', 'placeholder': 'Вставьте ваш код сюда'})
        }
    
    def clean_tags(self):
        tags_data = self.cleaned_data.get('tags')
        if not tags_data:
            return []
        
        # Split tags by comma and strip whitespace
        tag_names = [tag.strip() for tag in tags_data.split(',') if tag.strip()]
        
        # Create or get tag objects
        tag_objects = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)
        
        return tag_objects
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            # Clear existing tags and add new ones
            instance.tags.clear()
            for tag in self.cleaned_data.get('tags', []):
                instance.tags.add(tag)
                
        return instance


class CommentForm(forms.ModelForm):
    """
    Form for adding comments to snippets.
    """
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш комментарий...'})
        }


class SnippetSearchForm(forms.Form):
    """
    Form for searching snippets.
    """
    query = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск сниппетов...'})
    )
    language = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Все языки"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import ProgrammingLanguage
        self.fields['language'].queryset = ProgrammingLanguage.objects.all() 