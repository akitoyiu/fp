from django import forms
from .models import Post, Category, PostComment, PostMedia
from ckeditor.widgets import CKEditorWidget
from django.forms.widgets import ClearableFileInput
from .validators import validate_file_type


#Dynamic method
cats_list = Category.objects.all().values_list('name', 'name')
cats = []
for item in cats_list:
    cats.append(item)
#Static method
#cats = {('Coding', 'Coding'), ('UK', 'UK'), ('Entertainment', 'Entertainment')}

#Demised
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'tags', 'author', 'category', 'body', 'postmedias')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Post Title here'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Separate tags by comma'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': 'author', 'id':'author_id', 'type':'hidden'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=cats, attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),

        }

class MyClearableFileInput(ClearableFileInput):
    initial_text = 'Current Image'
    input_text = 'Change Image'
    clear_checkbox_label = 'Remove'
    

class NewPostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Post Title'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Separate tags by comma'}))
    category = forms.CharField(widget=forms.Select(choices=cats, attrs={'class':'form-control'}))
    postmedias = forms.FileField(validators=[validate_file_type], label='Choose Files', required=False, widget=MyClearableFileInput(attrs={'Multiple':True}))
    #body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    body = forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control', 'placeholder':'Comments'}))  

    class Meta:
        model = Post
        fields = {'title', 'tags', 'category', 'postmedias', 'body'}
        

class EditPostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Post Title'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Separate tags by comma'}))
    category = forms.CharField(widget=forms.Select(choices=cats, attrs={'class':'form-control'}))    
    body = forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control', 'placeholder':'Comments'}))  

    postmedias = forms.FileField(label='Choose Files', required=False, widget=MyClearableFileInput(attrs={'Multiple':True}))
    

    class Meta:
        model = Post
        fields = {'title', 'tags', 'category', 'postmedias', 'body'}


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('comment',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }