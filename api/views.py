from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from operator import itemgetter
from rauth import OAuth2Session
import json
from dateutil import parser
from api.models import *

from rq import Queue
from worker import conn

q = Queue(connection=conn)


def get_user(request):
	if request.user.is_authenticated():
		u = request.user
		result = {
			"name": u.name,
			"avatar_url": u.avatar_url,
			"login": u.github_login,
			"starred_repos_count":  u.starred_repos_count,
			"unassigned_issues_count": u.unassigned_issues_count,
			"bugs_count": u.bugs_count,
			"enhancements_count": u.enhancements_count,
			"total_issues_count": u.total_issues_count,
			"last_synced": str(u.last_synced)
		}
		return HttpResponse(json.dumps(result), content_type='application/javascript')
	else:
		raise Http404

def get_issues(request):
	if request.user.is_authenticated():
		u = request.user
		filters = request.GET.get("filters", "").split(",")

		if u.last_synced is None or (timezone.now() - u.last_synced > timedelta(days=1)):
			blocking_refresh_data(request)

		issues = []
		starred_repos = u.starred_repos.all()
		for r in starred_repos:
			issues += r.issues.filter(github_created_at__gt=timezone.now().date() - timedelta(days=7))
		result = []
		for i in issues:
			if "bugs" in filters and not i.isBug:
				continue
			if "enhancements" in filters and not i.isEnhancement:
				continue
			if "unassigned" in filters and i.isAssigned:
				continue
			if i.assignee_login is None:
				assignee = {}
			else:
				assignee = {
					"html_url": 'https://www.github.com/' + str(i.assignee_login),
					"login": i.assignee_login
				}
			issue = {
				"title": i.title,
				"html_url": i.html_url,
				"repo_full_name": i.repo.full_name,
				"number": i.number,
				"github_created_at": str(i.github_created_at),
				"owner": {
					"html_url":	'https://www.github.com/' + i.creator_login,
					"login": i.creator_login
				},
				"assignee": assignee,
				"comments_count": i.comments_count
			}
			result += [issue]

		#Sort issues by github_created_at
		sorted_result = sorted(result, key=itemgetter('github_created_at'), reverse=True)

		response = {
			"issues": sorted_result,
			"last_synced": str(u.last_synced)
		}

		return HttpResponse(json.dumps(response), content_type='application/javascript')
	else:
		raise Http404


def refresh_data(user, request=None, isQuick=False):
	u = user if user is not None else request.user

	#Don't allow sync more than once every 3 hours
	if u.last_synced is not None and (timezone.now() - u.last_synced < timedelta(hours=3)):
		return

	if u.is_authenticated():
		session = OAuth2Session(
			client_id=settings.GITHUB_CLIENT_ID,
			client_secret=settings.GITHUB_CLIENT_SECRET,
			access_token=u.github_access_token)

		#Get u's starred repos
		has_more = True
		page_number = 1
		repos = []
		while(has_more):
			results = session.get('https://api.github.com/user/starred', params={'format': 'json', 'per_page': 100, 'page': page_number}).json()
			if(len(results)==0):
				has_more = False
			page_number += 1
			repos += results

		starred_repos_count = len(repos)
		issues_count = 0
		bugs_count = 0
		enhancements_count = 0
		unassigned_issues_count = 0

		for index, repo in enumerate(repos):
			#TODO: Change this - hacky way to just look at last 10 repos first 100 issues
			if(index == 10 and isQuick):
				break
			repo_record, created = Repo.objects.get_or_create(full_name=repo["full_name"])
			repo_record.html_url = repo["html_url"]
			repo_record.stargazers.add(u)
			repo_record.save()

			#For the starred repos, get the issues
			has_more = True
			page_number = 1
			issues = []
			while(has_more):
				results = session.get('https://api.github.com/repos/' + repo["full_name"] + '/issues', params={'format': 'json', 'per_page': 100, 'page': page_number}).json()
				if(len(results)==0 or page_number==1): #TODO: For now, fetching only 1 page of 100 most recent issues (by default) for each repo to speed up syncing.
					has_more = False
				page_number += 1
				issues += results

			issues_count += len(issues)
			for issue in issues:
				issue_record, created = Issue.objects.get_or_create(html_url=issue["html_url"])
				issue_record.repo = repo_record
				issue_record.title = issue["title"]
				issue_record.number = issue["number"]
				issue_record.github_created_at = parser.parse(issue["created_at"])
				issue_record.creator_login = issue["user"]["login"]
				issue_record.comments_count = issue["comments"]
				try:
					issue_record.assignee_login = issue["assignee"]["login"]
					issue_record.isAssigned = True
				except:
					issue_record.assignee_login = None
					issue_record.isAssigned = False
					unassigned_issues_count += 1
				for label in issue["labels"]:
					if label["name"] == "bug":
						issue_record.isBug = True
						bugs_count += 1
					if label["name"] == "enhancement":
						issue_record.isEnhancement = True
						enhancements_count += 1
				issue_record.save()

		u.starred_repos_count = starred_repos_count
		u.bugs_count = bugs_count
		u.enhancements_count = enhancements_count
		u.total_issues_count = issues_count
		u.unassigned_issues_count = unassigned_issues_count
		u.last_synced = timezone.now()
		u.save()

		if request:
			return HttpResponse(content_type='application/javascript')
	else:
		raise Http404

def blocking_refresh_data(request):
	return refresh_data(None, request, True)

def non_blocking_refresh_data(request):
	#result = q.enqueue(refresh_data, request)
	result = q.enqueue_call(func=refresh_data, args=[request.user], timeout=600)
	return HttpResponse(content_type='application/javascript')
