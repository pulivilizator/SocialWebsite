from . import models

from django import forms


class AddPostForm(forms.ModelForm):
    """Form definition for MODELNAME."""
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}))
    content = forms.CharField(label='Основной текст поста', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Введите тескт', 'rows': 15, 'cols': 50}))
    photo = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = models.Post
        fields = ('title', 'content', 'photo', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['accept'] = 'image/*'


class AddCommentForm(forms.ModelForm):
    content = forms.CharField(label='Напишите комментарий', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Текст', 'rows': 5, 'cols': 50}))

    class Meta:
        model = models.Comment
        fields = ('content', )
