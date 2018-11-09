import json
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Monster, Printer, Owner, Book
from .serializers import MonsterSerializer, PrinterSerializer, OwnerSerializer, BookSerializer

from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet


class PrinterViewSet(ModelViewSet):
    serializer_class = PrinterSerializer
    queryset = Printer.objects.all()

class OwnerViewSet(ModelViewSet):
    serializer_class = OwnerSerializer
    queryset = Owner.objects.all()

class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(BASE, 'monsterapi')
DATA_DIR = os.path.join(APP_DIR, 'data')


# Create your views here.
def import_json(request, version):
    with open(os.path.join(DATA_DIR, 'MetadatenMartinusBibliothek20181101.Json'), "r") as f:
        data = json.loads(f.read())

    buch = BookSerializer(data=data['Buch'][0])
    buch.is_valid()

    return HttpResponse(str(buch.validated_data) + str(buch.errors))


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
