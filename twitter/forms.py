from django import forms
from .models import Tweet, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Profile Extras Form
class ProfilePicForm(forms.ModelForm):
	profile_image = forms.ImageField(label="Profile Picture", required=False)

	profile_bio = forms.CharField(label="Profile Bio", required=False, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}))
	homepage_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website Link'}))
	facebook_link =  forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook Link'}))
	instagram_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}))
	linkedin_link =  forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Linkedin Link'}))

	class Meta:
		model = Profile
		fields = ('profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link',)

class TweetForm(forms.ModelForm):
	body = forms.CharField(required=True, 
		widget=forms.widgets.Textarea(
			attrs={
			"placeholder": "Write what's in your mind today!",
			"class":"form-control",
			}
			),
			label="",
		)

	class Meta:
		model = Tweet
		exclude = ("user", "likes",)


class CommentForm(forms.ModelForm):
	body = forms.CharField(required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"placeholder": "Escreva um comentario...",
				"class": "form-control",
			}
		),
		label="",
	)

	class Meta:
		model = Comment
		fields = ("body",)


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''

		# Ao editar um usuario ja existente (instance com pk), a senha
		# deixa de ser obrigatoria - so troca se o campo for preenchido.
		if self.instance and self.instance.pk:
			self.fields['password1'].required = False
			self.fields['password2'].required = False
			self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Deixe em branco para manter a senha atual.</small></span>'
			self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
		else:
			self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
			self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 or password2:
			if password1 != password2:
				raise forms.ValidationError("As senhas nao coincidem.")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		password = self.cleaned_data.get("password1")
		if password:
			user.set_password(password)
		if commit:
			user.save()
		return user