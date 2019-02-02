from django import forms
from django.forms import ModelForm, Textarea,Select, CheckboxSelectMultiple,CheckboxInput
from .models import Post, Profile, University,Interest, Comment, SubmittedInterest
from django.contrib.auth.models import User




#form to handle submitted interests

class SubmitInterestForm(forms.ModelForm):
	class Meta:
		model = SubmittedInterest
		fields = ('interest_name','interest_description')
		widgets = {
			'interest_description': forms.Textarea(attrs ={
				'id': "interest_description",
				'required': True,
				'placeholder': 'What is the interest about...',
				'rows': '4'
			}),
			'interest_name': forms.TextInput(attrs ={
				'id': "interest_name",
				'required': True,
			}),
		}

# Form to handle (User) model Edit 
class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email','first_name','last_name')


# Form to handle the (Profile) model Edit
class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('university',)
		# get the list of universities for the select widget
		universities=University.objects.all()
		widgets = {
			'university': Select(choices=((x.university_name,x.university_name) for x in universities)),
		}

# Form to handle the sign up 
class signUpForm(forms.Form):
	username = forms.CharField(label='username')
	email=  forms.EmailField(label='email')
	password = forms.CharField(widget=forms.PasswordInput())
	# confirm_password = forms.CharField(widget=forms.PasswordInput())
	# birth_date = forms.DateField(label='Date of Birth', widget=forms.DateInput())
	# get the list of universities for the signup university widget
	universities=University.objects.all()
	university = forms.CharField(widget=Select(choices=((x.university_name,x.university_name) for x in universities)))
	

# change_password
class changePasswordForm(forms.Form):
	new_password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())

class PostForm(ModelForm):
	class Meta:
		model = Post
		exclude = ['author', 'date_posted', 'university', 'interest']
		# remove the default label on the form 
		labels = {
			'post_text': ('')
		}
		widgets = {
			'post_text': forms.Textarea(attrs ={
				'id': "post_text",
				'required': True,
				'placeholder': 'Spark a conversation...',
				'rows': '4'
			}),
		}
		# widgets = {
		# 	'post_text': Textarea(attrs={'cols':50,'rows':10}),
		# }
 

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ['author', 'date_posted', 'post_id']
		# remove the default label on the widget
		labels = {
			'comment':('')
		}
		widgets = {
			'comment' : forms.TextInput(attrs ={
				'id': 'comment',
				'required':True,
				'placeholder':'Add comment',
				'class':'',
				}),
		}