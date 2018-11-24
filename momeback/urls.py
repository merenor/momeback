"""momeback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
#from monsterapi import views as apiviews
from .api import router
from monsterapi.views import (GameView, CheckMonster, CheckGame, AllMonsters,
    Welcome)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('detail/', include(router.urls)),
    path('game/', GameView.as_view()),
    path('checkmonster/<int:monster_id>/<int:melody_id>/',
        CheckMonster.as_view()),
    path('checkgame/<int:game_id>/<int:melody_id>/',
        CheckGame.as_view()),
    path('view/allmonsters', AllMonsters),
    path('', Welcome)
]
