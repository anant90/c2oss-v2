from django.urls import path, re_path, include

import webapp.views

import api.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    # Examples:
    # path(r'^$', 'c2oss.views.home', name='home'),
    # path(r'^blog/', include('blog.urls')),

    re_path(r'^login/github/?$', webapp.views.oauth_github_authorize_url_redirect, name='oauth_github_authorize_url_redirect'),
    re_path(r'^login/github/callback/?$', webapp.views.oauth_github_callback, name='oauth_github_callback'),
    re_path(r'^api/user/?$', api.views.get_user, name='get_user'),
    re_path(r'^api/issues/?$', api.views.get_issues, name='get_issues'),
    re_path(r'^api/refresh/?$', api.views.non_blocking_refresh_data, name='non_blocking_refresh_data'),
    re_path(r'^logout/?$', webapp.views.logout_view, name='logout_view'),
    re_path(r'^.*$', webapp.views.index, name='index')
]
