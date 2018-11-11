from .models import Monster, Printer, Owner, Book, Melody
from .serializers import MonsterSerializer, PrinterSerializer, OwnerSerializer, BookSerializer, MelodySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.shortcuts import render

from random import choice, sample
import json
from collections import OrderedDict

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
        data = OrderedDict()

        # Get a random monster data set
        monster_pks = Monster.objects.values_list('pk', flat=True)
        rand_monster_pk = choice(list(monster_pks))
        rand_monster = Monster.objects.get(pk=rand_monster_pk)

        # Get a list of all melody primary keys
        melody_pks = list(Melody.objects.values_list('pk', flat=True))

        # Remove the pk of the selected monster from  to avoid duplicity
        melody_pks.remove(rand_monster_pk)

        # Get two random melodies
        rand_melody_pks = sample(melody_pks, 2)
        other_melodies = [Melody.objects.get(pk=pk) for pk in rand_melody_pks]

        # For the output of melody1, melody2 and melody3,
        # choose the place for the right answer
        monster_pos = choice([1, 2, 3])

        data['id'] = rand_monster.pk
        data['picture_id'] = rand_monster.picture_id
        data['file_format'] = rand_monster.file_format
        data['picture_filename'] = "http://monsterapi.pythonanywhere.com/media/monster_pics/" + rand_monster.picture_filename
        data['description'] = rand_monster.description
        data['bible_passage'] = rand_monster.bible_passage
        data['bible_text'] = rand_monster.bible_text
        data['book_title'] = rand_monster.book.title
        data['name'] = str(rand_monster.name)

        data['melodies'] = []

        if monster_pos == 1:
            data['melodies'].append({
                'id': rand_monster.melody.pk,
                'name': rand_monster.melody.name,
                'mei_data': rand_monster.melody.mei_data })
            data['melodies'].append({
                'id': other_melodies[0].pk,
                'name': other_melodies[0].name,
                'mei_data': other_melodies[0].mei_data })
            data['melodies'].append({
                'id': other_melodies[1].pk,
                'name': other_melodies[1].name,
                'mei_data': other_melodies[1].mei_data })

        if monster_pos == 2:
            data['melodies'].append({
                'id': other_melodies[0].pk,
                'name': other_melodies[0].name,
                'mei_data': other_melodies[0].mei_data })
            data['melodies'].append({
                'id': rand_monster.melody.pk,
                'name': rand_monster.melody.name,
                'mei_data': rand_monster.melody.mei_data })
            data['melodies'].append({
                'id': other_melodies[1].pk,
                'name': other_melodies[1].name,
                'mei_data': other_melodies[1].mei_data })

        if monster_pos == 3:
            data['melodies'].append({
                'id': other_melodies[0].pk,
                'name': other_melodies[0].name,
                'mei_data': other_melodies[0].mei_data })
            data['melodies'].append({
                'id': other_melodies[1].pk,
                'name': other_melodies[1].name,
                'mei_data': other_melodies[1].mei_data })
            data['melodies'].append({
                'id': rand_monster.melody.pk,
                'name': rand_monster.melody.name,
                'mei_data': rand_monster.melody.mei_data })

        return Response(data)


class CheckMelody(APIView):

    def get(self, request, monster_id, melody_id):
        monster = Monster.objects.get(pk=monster_id)
        if monster.melody == None:
            return Response({ 'result': 'Monster ist unmusikalisch. :-(' })

        return Response({ 'result': monster.melody.pk == melody_id })

def AllMonsters(request):
    monsters = Monster.objects.all()
    return render(request, 'monsters.html', {'monsters': monsters})
