from .models import Monster, Printer, Owner, Book, Melody
from .serializers import MonsterSerializer, PrinterSerializer, OwnerSerializer, BookSerializer, MelodySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.mixins import NestedViewSetMixin

from random import choice, sample
import json

class PrinterViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = PrinterSerializer
    queryset = Printer.objects.all()

class OwnerViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = OwnerSerializer
    queryset = Owner.objects.all()

class BookViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class MonsterViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = MonsterSerializer
    queryset = Monster.objects.all()

class MelodyViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = MelodySerializer
    queryset = Melody.objects.all()

class GameView(APIView):

    def get(self, request, format=None):
        # dataset for the response
        data = {}

        # Get a random monster
        monster_pks = Monster.objects.values_list('pk', flat=True)
        rand_monster_pk = choice(list(monster_pks))
        rand_monster = Monster.objects.get(pk=rand_monster_pk)

        # Get three different melodies
        melody_pks = list(Melody.objects.values_list('pk', flat=True))
        # remove right monster id to avoid duplicity
        melody_pks.remove(rand_monster_pk)
        rand_melody_pks = sample(melody_pks, 2)
        other_melodies = [Melody.objects.get(pk=pk) for pk in rand_melody_pks]

        monster_pos = choice([1, 2, 3])

        if monster_pos == 1:
            data['melody1_id'] = rand_monster.melody.pk
            data['melody1_name'] = rand_monster.melody.name
            data['melody1_mei_data'] = rand_monster.melody.mei_data

            data['melody2_id'] = other_melodies[0].pk
            data['melody2_name'] = other_melodies[0].name
            data['melody2_mei_data'] = other_melodies[0].mei_data

            data['melody3_id'] = other_melodies[1].pk
            data['melody3_name'] = other_melodies[1].name
            data['melody3_mei_data'] = other_melodies[1].mei_data

        if monster_pos == 2:
            data['melody1_id'] = other_melodies[0].pk
            data['melody1_name'] = other_melodies[0].name
            data['melody1_mei_data'] = other_melodies[0].mei_data

            data['melody2_id'] = rand_monster.melody.pk
            data['melody2_name'] = rand_monster.melody.name
            data['melody2_mei_data'] = rand_monster.melody.mei_data

            data['melody3_id'] = other_melodies[1].pk
            data['melody3_name'] = other_melodies[1].name
            data['melody3_mei_data'] = other_melodies[1].mei_data

        if monster_pos == 3:
            data['melody1_id'] = other_melodies[0].pk
            data['melody1_name'] = other_melodies[0].name
            data['melody1_mei_data'] = other_melodies[0].mei_data

            data['melody2_id'] = other_melodies[1].pk
            data['melody2_name'] = other_melodies[1].name
            data['melody2_mei_data'] = other_melodies[1].mei_data

            data['melody3_id'] = rand_monster.melody.pk
            data['melody3_name'] = rand_monster.melody.name
            data['melody3_mei_data'] = rand_monster.melody.mei_data

        data['id'] = rand_monster.pk
        data['picture_id'] = rand_monster.picture_id
        data['file_format'] = rand_monster.file_format
        data['picture_filename'] = "http://monsterapi.pythonanywhere.com/media/monster_pics/" + rand_monster.picture_filename
        data['description'] = rand_monster.description
        data['bible_passage'] = rand_monster.bible_passage
        data['bible_text'] = rand_monster.bible_text
        data['book_title'] = rand_monster.book.title
        data['name'] = rand_monster.str()

        return Response(data)


class CheckMelody(APIView):

    def get(self, request, monster_id, melody_id):
        monster = Monster.objects.get(pk=monster_id)
        if monster.melody == None:
            return Response({ 'result': 'Monster ist unmusikalisch. :-(' })

        return Response({ 'result': monster.melody.pk == melody_id })
