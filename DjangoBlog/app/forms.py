from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple


from app.models import Post ,Tag , Category,ForbiddenWord,Comment,Reply

class SignupCustomForm(UserCreationForm):
    email = forms.EmailField(max_length=30)
   
    class Meta:
        model = User
        fields = ("username",'email','password1','password2')


# -------------------------------

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['created_at','updated_at','author','likes','unlikes']
        widgets = {
            'post_content':forms.Textarea(attrs={'cols': 40, 'rows': 1}),
        }
    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)

        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tag.objects.all()
        

    def clean(self):
        super(PostModelForm, self).clean()
        title = self.cleaned_data.get('title')
        if title :
            if len(title) < 5:
                self._errors['title'] = self.error_class( ['A minimum of 5 characters is required'])
        else:
            self._errors['title'] = self.error_class( ['Post title is required'])
        return self.cleaned_data


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("cat_name",)

    def clean(self):
        super(CategoryModelForm, self).clean()
        cat_name = self.cleaned_data.get('cat_name')
        if cat_name :
            if len(cat_name) < 4:
                self._errors['cat_name'] = self.error_class( ['A minimum of 4 characters is required'])
            if Category.objects.filter(cat_name=cat_name).first():
                self._errors['cat_name'] = self.error_class( ['already exists'])
        else:
            self._errors['cat_name'] = self.error_class( ['Category name is required'])
        return self.cleaned_data


class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("tag_name",)

    def clean(self):
        super(TagModelForm, self).clean()
        tag_name = self.cleaned_data.get('tag_name')
        if tag_name :
            if len(tag_name) < 5:
                self._errors['tag_name'] = self.error_class( ['A minimum of 5 characters is required'])

            if Tag.objects.filter(tag_name=tag_name).first():
                self._errors['tag_name'] = self.error_class( ['already exists'])

        else:
            self._errors['tag_name'] = self.error_class( ['tag name is required'])
        return self.cleaned_data


class ForbiddenWordModelForm(forms.ModelForm):
    class Meta:
        model = ForbiddenWord
        fields = ("word",)

    def clean(self):
        super(ForbiddenWordModelForm, self).clean()
        word = self.cleaned_data.get('word')
        if word :
            if ForbiddenWord.objects.filter(word=word).first():
                self._errors['word'] = self.error_class( ['already exists'])
        else:
            self._errors['word'] = self.error_class( ['required'])
        return self.cleaned_data

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

    def clean(self):
        super(CommentModelForm, self).clean()
        content = self.cleaned_data.get('content')
        if content :
            if len(content) < 1:
                self._errors['content'] = self.error_class( ['A minimum of 1 characters is required'])
        else:
            self._errors['content'] = self.error_class( [' required'])
        return self.cleaned_data

class ReplyModelForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ("content",)

    def clean(self):
        super(ReplyModelForm, self).clean()
        content = self.cleaned_data.get('content')
        if content :
            if len(content) < 1:
                self._errors['content'] = self.error_class( ['A minimum of 1 characters is required'])
        else:
            self._errors['content'] = self.error_class( ['required'])
        return self.cleaned_data
        