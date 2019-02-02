from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	interest = ArrayField(models.CharField(max_length=200), blank=True, null=True)
	university = models.CharField(max_length=200, blank=True,null=True)

class Post(models.Model):
	post_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
	post_text = models.TextField(max_length=400)
	date_posted = models.DateTimeField('date')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	interest = models.CharField(max_length=200)
	university = models.CharField(max_length=400)

class SubmittedInterest(models.Model):
	interest_name = models.CharField(max_length=400)
	interest_description = models.CharField(max_length=400)
	submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
	date_submitted = models.DateTimeField('date')


class Comment(models.Model):
	comment_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
	post_id = models.UUIDField()
	comment = models.CharField(max_length=400)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date_posted = models.DateTimeField('date')

class Like(models.Model):
	like_user = models.ForeignKey(User, on_delete=models.CASCADE)
	like_post_id = models.UUIDField()

class University(models.Model):
	university_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
	university_name = models.CharField(max_length=400)

class Interest(models.Model):
	interest_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
	interest_name = models.CharField(max_length=400)
	date_created = models.DateTimeField('date')



# class PostForm(ModelForm):
# 	class Meta:
# 		model = Post
# 		exclude = ['author', 'date_posted']
# 		labels = {
# 			'post_text': ('')
# 		}
# 		widgets = {
# 			'post_text': Textarea(attrs={'cols':50,'rows':10}),
# 		}
