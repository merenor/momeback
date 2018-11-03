import json
import os

from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics

from .models import Monster
from .serializers import MonsterSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(BASE, 'monsterapi')
DATA_DIR = os.path.join(APP_DIR, 'data')

# Create your views here.
def newgame(request):
    pass

def showmonster(request, pic_id):
    monster = Monster.objects.filter(picture_id=pic_id)

    return HttpResponse("ok")


class ListMonstersView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer


class SingleMonstersView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, picture_id):
        try:
            return Monster.objects.get(picture_id=picture_id)
        except Monster.DoesNotExist:
            raise Http404

    def get(self, request, version, picture_id, format=None):
        monster = self.get_object(picture_id)
        serializer = MonsterSerializer(monster)
        return Response(serializer.data)
