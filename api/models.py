from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):

	def _create_user(self, email, password,
		is_staff, is_superuser, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		now = timezone.now()
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email,
			is_staff=is_staff, is_active=True,
			is_superuser=is_superuser, last_login=now,
			date_joined=now, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		return self._create_user(email, password, False, False, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, password, True, True, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField('email_address', max_length=254, unique=True)
	github_login = models.CharField(max_length=100, null=True)
	github_access_token = models.CharField(max_length=255, null=True)
	avatar_url = models.TextField(null=True)
	name = models.CharField(max_length=150, null=True)

	#Computed and cached fields
	starred_repos_count = models.IntegerField(default=0)
	unassigned_issues_count = models.IntegerField(default=0)
	bugs_count = models.IntegerField(default=0)
	enhancements_count = models.IntegerField(default=0)
	total_issues_count = models.IntegerField(default=0)
	last_synced = models.DateTimeField(null=True)

	is_staff = models.BooleanField('staff_status', default=False)
	is_active = models.BooleanField('active', default=True)
	date_joined = models.DateTimeField('date_joined', default=timezone.now)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def get_absolute_url(self):
		return 'https://www.github.com/' + self.github_login

class Repo(models.Model):
	html_url = models.TextField(null=True)
	full_name = models.CharField(max_length=100, null=True)
	stargazers = models.ManyToManyField(CustomUser, related_name="starred_repos")

class Issue(models.Model):
	repo = models.ForeignKey(Repo, related_name="issues", null=True, on_delete=models.PROTECT)
	html_url = models.TextField(null=True)
	title = models.TextField(null=True)
	number = models.IntegerField(null=True)
	github_created_at = models.DateField("Created at", null=True)
	creator_login = models.CharField(max_length=100, null=True)
	comments_count = models.IntegerField(null=True)
	assignee_login = models.CharField(max_length=100, null=True)
	isBug = models.BooleanField(default=False)
	isEnhancement = models.BooleanField(default=False)

	#Computed and cached fields:
	isAssigned = models.BooleanField(default=False)
