from django import forms
from django.forms.widgets import PasswordInput
from tasks.models import Project, Task

# create a form
class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter the email",
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter the password",
        })

    def clean(self):
        super(LoginForm, self).clean()
        
        if self.cleaned_data.get('email') is None:
            self._errors['email'] = self.error_class(
                ['Empty value not allow'])
            return self.cleaned_data
        
        if self.cleaned_data.get('password') is None:
            self._errors['password'] = self.error_class(
                ['Empty value not allow'])
            return self.cleaned_data

        return self.cleaned_data
    

class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter the name of project",
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter the description of project",
        })

    # def clean(self):
    #     super(LoginForm, self).clean()
        
    #     if self.cleaned_data.get('email') is None:
    #         self._errors['email'] = self.error_class(
    #             ['Empty value not allow'])
    #         return self.cleaned_data
        
    #     if self.cleaned_data.get('password') is None:
    #         self._errors['password'] = self.error_class(
    #             ['Empty value not allow'])
    #         return self.cleaned_data

    #     return self.cleaned_data

class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'assign_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter the name of task",
        })
        
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter the description of task",
        })
        
        self.fields['assign_to'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter the description of task",
        })