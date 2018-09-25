"""WechatVote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from Vote.views import Index, VoteEventRetrive, Voting, VoteIndex, WXCallback, WXTokenAccess

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', obtain_jwt_token),
    path('api-auth-verify', verify_jwt_token),
    path('api-auth-refresh', refresh_jwt_token),
    path('wx-callback', WXCallback.as_view()),
    path('wx-api', WXTokenAccess.as_view()),
    path('retrive/<int:id>', VoteEventRetrive.as_view()),
    path('voting', Voting.as_view()),
    path('voteindex', VoteIndex.as_view()),
    # path('', Index.as_view()),  不添加关注微信号认证
    path('', VoteIndex.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
