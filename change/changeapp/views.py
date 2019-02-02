from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from .models import Post, Like, Profile, Interest, Comment, SubmittedInterest
from django.contrib.auth.models import User
from .forms import signUpForm, PostForm, UserEditForm, ProfileEditForm,CommentForm,SubmitInterestForm,changePasswordForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpRequest
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
import random
import logging
from django.core import serializers
import json
from django.http import Http404
from django.utils.text import slugify

# Create your views here.

logger = logging.getLogger(__name__)


@login_required(login_url='login')
@csrf_protect
def index(request):
	recent_interest = Interest.objects.order_by('-date_created').all()[:10]
	interests = Profile.objects.get(user=request.user)
	# Check if the user has interests 
	if not interests.interest:
		print("edit int")
		return redirect('edit_interests')
	# create a post list object 
	post_list = {}
	# Loop through the user interests
	for i in interests.interest:
		current_interest = i
		try:
			# Get the first post by order of date on the current_interest in the for loop
			post = Post.objects.order_by('-date_posted').filter(interest=current_interest)[:1].get()
			# add it to the post_list{} object
			post_list[current_interest] = post
		except Post.DoesNotExist:
			print("No post with interest " + current_interest)

	data = {
		"post_list" : post_list,
		'recent_interest' : recent_interest,
		
	}
	# return JsonResponse(post_list, safe=False)
	return render(request, "index.html", data)



# interest page view
@login_required(login_url='login')
@csrf_protect
def interest(request, interest):
	# add post form
	form = PostForm()
	all_interests = Interest.objects.all().values_list('interest_name', flat=True);

	# loop through all the intrests
	for i in all_interests:
		# check if the current interest in the loop matches the interest in the request
		if interest == i:
			post_list = Post.objects.order_by('-date_posted').filter(interest=interest)
			# number of user and posts in the interest (i)
			posts_count = Post.objects.filter(interest = interest).count()
			users_count = Profile.objects.filter(interest__contains=[interest]).count()
			# paginations stuff
	
			paginator = Paginator(post_list, 4)
			page = request.GET.get('page')
			posts = paginator.get_page(page)
			context = {
				'posts':posts,
				'interest': interest, 
				'form': form,
				'posts_count': posts_count,
				'users_count': users_count,
				'user_has_interest': Profile.objects.filter(interest__contains=[interest], user=request.user).exists()
			}	
			return render(request, 'interest_page.html', context)	
	raise Http404("Page does not exist")


# view to handle signUp of new users
def signUp(request):
	if request.method == "POST":
		# signup (Form) data
		form = signUpForm(request.POST)
		# chec if the form is valid
		if form.is_valid():
			username = request.POST.get('username')
			email = request.POST.get('email')
			password = request.POST.get('password')
			university = request.POST.get('university')
			check_username = User.objects.filter(username=username).exists()
			if check_username:
				response = {
					'username_exists':True
				}
				return JsonResponse(response)	
			else:				
				user = User.objects.create_user(username, email, password)
				user.save()
				# create a profile instance and Add the university
				profile = Profile.objects.create(user=user, university=university)
				profile.save()
				response = {
					'created':True
				}
				return JsonResponse(response)	
	else:
		form = signUpForm()
	context = {
		'form': form,
	}
	return render(request, 'registration/signup.html', context)


# remove account
@login_required(login_url='login')
@csrf_protect
def remove_account(request):
	acc_to_delete = User.objects.filter(username=request.user)
	acc_to_delete.delete()
	return redirect('login')


# change password
@login_required(login_url='login')
@csrf_protect
def change_password(request):
	form  = changePasswordForm()
	if request.method == "POST":
		user_pass = User.objects.get(username=request.user)
		password = request.POST.get('password')
		user_pass.set_password(password)
		user_pass.save()
		response = {
			'changed':True
		}
		return JsonResponse(response)	
	context = {
		'form': form,
	}
	return render(request, 'registration/change_password.html', context)
	
# edit interests 
@login_required(login_url='login')
@csrf_protect
def edit_interests(request):
	all_interests = Interest.objects.all().order_by('-date_created')
	
	# receive interest changes from client
	if request.method == "POST":
		# get the json from the ajax
		changes = request.POST.getlist('data[]')
		interests = Profile.objects.get(user=request.user)
		interests.interest = changes
		interests.save()
		changes_saved = True
		print(changes)
		data = {
			"changes_saved": changes_saved
		}
		return JsonResponse(data)

	context = {
		'all_interests' : all_interests,
	}
	return render(request, 'edit_interests.html', context)



@login_required(login_url='login')
@csrf_protect
def add_interest(request):	
	if request.method == "GET":
		interest = request.GET.get('interest')
		action = request.GET.get('action')
		# profile intance
		profile_instance = Profile.objects.get(user=request.user)

		if action == "Add":
			profile_instance.interest.insert(0,interest)
			profile_instance.save()
			data = {
				"interest": "added",
				"users_count": Profile.objects.filter(interest__contains=[interest]).count()
			}
			return JsonResponse(data)
		else:
			profile_instance.interest.remove(interest)
			profile_instance.save()
			data = {
				"interest": "removed",
				"users_count": Profile.objects.filter(interest__contains=[interest]).count()
			}
			return JsonResponse(data)

# get all interests and also user saved interets
@login_required(login_url='login')
@csrf_protect
def get_interests(request):
	user_interests = Profile.objects.values_list('interest', flat=True).filter(user= request.user)
	for i in user_interests:
		data = list(i)
	# data = serializers.serialize('json',user_interests)
	return JsonResponse(data, safe=False)


# edit profile
@login_required(login_url='login')
@csrf_protect
def edit_profile(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance= request.user, data=request.POST)
		profile_form = ProfileEditForm(instance= request.user.profile, data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			# form save data
			user_form.save()
			profile_form.save()
			return redirect('index')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)

	context = {
		'user_form':user_form,
		'profile_form': profile_form		
	}
	return render(request, 'edit_profile.html', context)


@login_required(login_url='login')
@csrf_protect
def add_post(request):
	form = PostForm(data=request.POST)
	time_now = timezone.now();	
	author = request.user
	university = request.user.profile.university
	if request.method == "POST":
		if form.is_valid():
			post_text = request.POST.get('post_text')
			interest = request.POST.get('interest')
			post = Post(post_text=post_text, 
				date_posted=time_now, 
				author=author, 
				university=university, 
				interest=interest)
			post.save() 
			response = {
				'saved':True
			}
			return JsonResponse(response)
	else:
		raise Http404("Page does not exist")



@login_required(login_url='login')
@csrf_protect
def submit_interest(request):
	form = SubmitInterestForm(data=request.POST)
	if request.method == "POST":
		if form.is_valid():
			interest_name = request.POST.get("interest_name");
			interest_description = request.POST.get("interest_description");
			date_submitted = timezone.now()
			submitted_by = request.user
			submittedInterest = SubmittedInterest(interest_name=interest_name,
				interest_description=interest_description,
				date_submitted=date_submitted,
				submitted_by=submitted_by)
			submittedInterest.save()
			response = {
			'saved':True
			}

			return JsonResponse(response)
	else:
		context = {
			'form': SubmitInterestForm
		}
		return render(request, 'submit_interest.html', context)



@login_required(login_url='login')
@csrf_protect
def my_posts(request):
	my_posts_list = Post.objects.order_by('-date_posted').filter(author=request.user)
	paginator = Paginator(my_posts_list, 10)
	page = request.GET.get('page')
	posts = paginator.get_page(page)
	context = {
		'posts':posts	
	}
	return render(request, 'my_posts.html', context)


@login_required(login_url='login')
@csrf_protect
def delete_post(request, post_id):
	post_to_delete = Post.objects.filter(post_id=post_id, author=request.user)
	post_to_delete.delete()
	is_deleted = Post.objects.filter(post_id=post_id, author=request.user).exists()
	response = {
		'is_deleted':is_deleted
	}
	return JsonResponse(response)



@login_required(login_url='login')
@csrf_protect
def add_comment(request):
	time_now = timezone.now()
	author = request.user
	if request.method == "POST":
		# get the comment and post in json from the ajax
		comment_text = request.POST.get('comment_text')
		post_id = request.POST.get('post_id')
		comment = Comment(post_id=post_id,comment=comment_text,author=author,date_posted=time_now)
		comment.save()
		response ={
			'saved':True
		}
		return JsonResponse(response)
	else:
		raise Http404("page does not exist")




def post_detail(request, post_id):
	post = Post.objects.get(post_id = post_id)
	return render(request, 'post_detail.html', {'post':post})


# Handles the like request
@login_required(login_url='login')
@csrf_protect
def like(request, post_id):
	user = request.user
	query_uv = Like.objects.filter(like_post_id = post_id,like_user = request.user)
	if query_uv.exists():
		remove_like(post_id,user)	
	else:
		add_like(post_id, user)
	data = {
		'like_count' : Like.objects.filter(like_post_id = post_id).count(),
		'is_like' : Like.objects.filter(like_post_id = post_id,like_user = request.user).exists(),

	}		
	return JsonResponse(data)



# checks for an like for the logged user and also the like count for that particular post
@login_required(login_url='login')
@csrf_protect
def check_like(request, post_id):
	user = request.user
	data = {
		'is_like' : Like.objects.filter(like_post_id = post_id,like_user = request.user).exists(),
		'like_count' : Like.objects.filter(like_post_id = post_id).count()
	}
	return JsonResponse(data)


def flag_post(request, post_id):
	return request


# utils for adding and removing like
def add_like(post_id, user):
	like_add = Like(like_user=user, like_post_id=post_id)
	like_add.save()
	
def remove_like(post_id, user):
	like_remove = Like.objects.filter(like_post_id = post_id,like_user = user)
	like_remove.delete()



