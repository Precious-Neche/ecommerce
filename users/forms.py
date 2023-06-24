from django import forms
from . models import Profile

class ProfileForm(forms.ModelForm):
    password1 = forms.CharField(label = ('Password'), required = True, widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label = ('Confirm Password'), required = True, widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    fullname = forms.CharField(label = ('Full Name'), widget = forms.TextInput(attrs = {'class': 'form-control'}))
    username = forms.CharField( widget = forms.TextInput(attrs = {'class': 'form-control'}))
    email = forms.EmailField( widget = forms.TextInput(attrs = {'class': 'form-control'}))
   

    profile_picture = forms.ImageField(label= ('Profile picture'), required= False, widget= forms.FileInput(attrs = {'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ("fullname",'username','email','Gender','Phone', 'Address','password1', 'password2', 'profile_picture',)

        widgets = {
            'Address': forms.Textarea(attrs = {'class': 'form-control', 'rows':3}),
            'Phone': forms.TextInput(attrs= {'class': 'form-control'}),
            'Gender': forms.Select(attrs={'class': 'form-control'})

            
        }
class UpdateProfileForm(forms.ModelForm):
    
    fullname = forms.CharField(label = ('Full Name'), widget = forms.TextInput(attrs = {'class': 'form-control'}))
    username = forms.CharField( widget = forms.TextInput(attrs = {'class': 'form-control'}))
    email = forms.EmailField( widget = forms.TextInput(attrs = {'class': 'form-control'}))
   

    profile_picture = forms.ImageField(label= ('Profile picture'), required= False, widget= forms.FileInput(attrs = {'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ("fullname",'username','email','Gender','Phone', 'Address', 'profile_picture',)

        widgets = {
            'Address': forms.Textarea(attrs = {'class': 'form-control', 'rows':3}),
            'Phone': forms.TextInput(attrs= {'class': 'form-control'}),
            'Gender': forms.Select(attrs={'class': 'form-control'})

            
        }
