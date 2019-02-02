from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from .models import Post, PostForm, Upvote, Downvote
from .forms import signUpForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def index(request):
	post_list = Post.objects.order_by('date_posted')
	paginator = Paginator(post_list, 10)
	page = request.GET.get('page')
	posts = paginator.get_page(page)
	
	context = {
		'posts':posts,
		
	}
	return render(request, 'index.html', context)

def signUp(request):
	if request.method == "POST":
		form = signUpForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = User.objects.create_user(username, email, password)
			user.save()
			return HttpResponseRedirect('accounts/login')
	else:
		form = signUpForm()

	return render(request, 'registration/signup.html', {'form': form})


def add_post(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.date_posted = datetime.now()
			post.save()
			return redirect('post_detail', post_id=post.post_id)

	else:
		form = PostForm()
	return render(request, 'add_post.html', {'form':form})

def post_detail(request, post_id):
	post = Post.objects.get(post_id = post_id)
	return render(request, 'post_detail.html', {'post':post})

def upvote(request, post_id):
	user = request.user
	query_uv = Upvote.objects.filter(upvote_post_id = post_id,upvote_user = request.user)
	query_dv = Downvote.objects.filter(downvote_post_id = post_id,downvote_user = request.user)

	if query_uv.exists():
		remove_upvote(post_id,user)
	else:
		if query_dv.exists():
			remove_downvote(post_id,user)
			add_upvote(post_id, user)
		else:
			add_upvote(post_id, user)

	return redirect('/')

def downvote(request, post_id):
	user = request.user
	query_uv = Upvote.objects.filter(upvote_post_id = post_id,upvote_user = request.user)
	query_dv = Downvote.objects.filter(downvote_post_id = post_id,downvote_user = request.user)

	if query_dv.exists():
		remove_downvote(post_id,user)
	else:
		if query_uv.exists():
			remove_upvote(post_id,user)
			add_downvote(post_id, user)
		else:
			add_downvote(post_id, user)

	return redirect('/')

def flag_post(request, post_id):
	return request


# utils
def add_upvote(post_id, user):
	upvote_add = Upvote(upvote_user=user, upvote_post_id=post_id)
	upvote_add.save()
	post_update = Post.objects.get(post_id=post_id)
	post_update.upvote_count = F('upvote_count') + 1
	post_update.save()

def remove_upvote(post_id, user):
	upvote_remove = Upvote.objects.filter(upvote_post_id = post_id,upvote_user = user)
	upvote_remove.delete()
	post_update = Post.objects.get(post_id=post_id)
	post_update.upvote_count = F('upvote_count') - 1
	post_update.save()

def add_downvote(post_id, user):
	downvote_add = Downvote(downvote_user=user, downvote_post_id=post_id)
	downvote_add.save()
	post_update = Post.objects.get(post_id=post_id)
	post_update.downvote_count = F('downvote_count') + 1
	post_update.save()

def remove_downvote(post_id, user):
	downvote_remove = Downvote.objects.filter(downvote_post_id = post_id, downvote_user = user)
	downvote_remove.delete()
	post_update = Post.objects.get(post_id=post_id)
	post_update.downvote_count = F('downvote_count') - 1
	post_update.save()