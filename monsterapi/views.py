from .models import Monster, Printer, Owner, Book, Melody, Game, Check
from .serializers import (MonsterSerializer, PrinterSerializer, OwnerSerializer,
    BookSerializer, MelodySerializer)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.shortcuts import render

from random import choice, sample, shuffle
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

        # Remove the pk of the selected monster's melody from melody list to avoid duplicity
        melody_pks.remove(rand_monster.melody.pk)

        # Get two random sample melodies
        rand_melody_pks = sample(melody_pks, 2)
        other_melodies = [Melody.objects.get(pk=pk) for pk in rand_melody_pks]

        data['id'] = rand_monster.pk
        data['picture_slug'] = rand_monster.picture_slug
        data['file_format'] = rand_monster.file_format
        data['picture_filename'] = "http://monsterapi.pythonanywhere.com/media/monster_pics/" + rand_monster.picture_filename
        data['description'] = rand_monster.description
        data['bible_passage'] = rand_monster.bible_passage
        data['bible_text'] = rand_monster.bible_text
        data['book_title'] = rand_monster.book.title
        data['name'] = str(rand_monster.name)

        melodies = [MelodySerializer(rand_monster.melody).data,
            MelodySerializer(other_melodies[0]).data,
            MelodySerializer(other_melodies[1]).data]

        shuffle(melodies)

        data['melodies'] = melodies

        # save this game to database
        game = Game(monster=rand_monster,
            melody1=rand_monster.melody,
            melody2=other_melodies[0],
            melody3=other_melodies[1])
        game.save()

        data['game_id'] = game.id

        return Response(data)


class CheckMonster(APIView):
    """ Simple check function
        Parameters: int:monster_id/int:game_id """

    def get(self, request, monster_id, melody_id):
        monster = Monster.objects.filter(pk=monster_id).first()

        return Response({ 'result': monster.melody.pk == melody_id })


class CheckGame(APIView):
    """ Check if a certain melody fits to a certain monster.<br />
        Parameters: int:game_id/int:game_id<br />
        Results: true or false (this also if there was any error) """

    def get(self, request, game_id, melody_id):
        game = Game.objects.filter(id=game_id).first()
        monster = game.monster if game else None
        melody = Melody.objects.filter(id=melody_id).first()

        if monster and melody:
            result = (monster.melody == melody)
        else:
            result = False

        check = Check(game=game, monster=monster, melody=melody, result=result)
        check.save()
        print("\nGame:", check.game, "\nMonster:", check.monster,
            "\nMelodie:", check.melody, "\nResult:", check.result)

        return Response({'result': result})

def AllMonsters(request):
    monsters = Monster.objects.all()
    return render(request, 'monsters.html', {'monsters': monsters})

def Welcome(request):
    return render(request, 'welcome.html')
