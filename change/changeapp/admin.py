from django.contrib import admin
from django import forms
from .models import Post, Like, University, Interest, Profile, Comment, SubmittedInterest
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ('post_id', 'post_text','date_posted','author','interest','university')
	list_display_links = ('post_text', 'author')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'birth_date', 'interest', 'university']

class UniversityAdmin(admin.ModelAdmin):
	list_display = ('university_id', 'university_name')
	list_display_links = ('university_name',)

class InterestAdmin(admin.ModelAdmin):
    list_display = ['interest_id', 'interest_name', 'date_created']	

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_id', 'post_id', 'comment','author','date_posted']	

class submittedInterestAdmin(admin.ModelAdmin):
	list_display = ['interest_name','interest_description']

admin.site.register(SubmittedInterest, submittedInterestAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(University, UniversityAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Comment, CommentAdmin)
