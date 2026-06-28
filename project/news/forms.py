from django import forms
from .models import Post
from django.utils import timezone
from datetime import timedelta



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text']

    
    def clean(self):
        cleaned_data = super().clean()

        author = cleaned_data.get('author')

        yesterday = timezone.now() - timedelta(hours=24)
        count = Post.objects.filter(
            author=author,
            created__gte=yesterday
        ).count()
                
        if count >= 3:
            raise forms.ValidationError("Вы не можете публиковать более 3 новостей в сутки.")
        return cleaned_data