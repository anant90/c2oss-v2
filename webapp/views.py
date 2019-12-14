import json
import random
import string

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout
from rauth import OAuth2Service, OAuth2Session

from api.models import *

github_service = OAuth2Service(
	client_id = settings.GITHUB_CLIENT_ID,
	client_secret = settings.GITHUB_CLIENT_SECRET,
	name = 'github',
	authorize_url = settings.GITHUB_AUTHORIZE_URL,
	access_token_url = settings.GITHUB_ACCESS_TOKEN_URL,
	base_url = settings.GITHUB_BASE_URL)

# Create your views here.
def index(request):
	is_logged_in = "false"
	if request.user.is_authenticated:
		is_logged_in = "true"

	return render(request, 'index.html', {"isLoggedIn": is_logged_in})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def oauth_github_authorize_url_redirect(request):
	params = {
		'scope': 'public_repo'
	}
	authorize_url = github_service.get_authorize_url(**params)
	return HttpResponseRedirect(authorize_url)

def oauth_github_callback(request):
	if 'error' in request.GET:
		return HttpResponseRedirect('/')

	code = request.GET['code']
	session = github_service.get_auth_session(data={'code': code})
	user_data = session.get('user', params={'format': 'json'}).json()

	try:
		user = CustomUser.objects.get(github_login=user_data['login'])
	except:
		#Create the user
		password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
		user = CustomUser.objects.create_user(user_data['email'], password)
		user.github_login = user_data['login']
		user.name = user_data['name']

	#Update the avatar url:
	user.avatar_url = user_data['avatar_url']
	user.github_access_token = session.access_token
	user.save()

	#TODO: Refresh issues data

	#Login as the user
	user.backend = 'django.contrib.auth.backends.ModelBackend'
	login(request, user)
	return HttpResponseRedirect('/')
