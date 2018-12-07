from .models import (Monster, Printer, Owner, Book, Melody, Game, Check,
    Recipe, Name)
from .serializers import (MonsterSerializer, PrinterSerializer, OwnerSerializer,
    BookSerializer, MelodySerializer, GameSerializer, CheckSerializer,
    RecipeSerializer, NameSerializer, StatCheckSerializer)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.dateparse import parse_datetime
#from rest_framework_extensions.mixins import NestedViewSetMixin

from django.shortcuts import render

from random import choice, sample, shuffle
import json
from collections import OrderedDict
import datetime

#####
# Views for /details/
#####

class PrinterViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = PrinterSerializer
    queryset = Printer.objects.all()


#NestedViewSetMixin,
class OwnerViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = OwnerSerializer
    queryset = Owner.objects.all()


class BookViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = BookSerializer
    queryset = Book.objects.all()


class MonsterViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = MonsterSerializer

    # exclude that special someone
    queryset = Monster.objects.all().exclude(id=666)


class MelodyViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = MelodySerializer

    # just the first 30 entries
    queryset = Melody.objects.all()[0:29]


class GameViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = GameSerializer
    queryset = Game.objects.all().order_by('-id')[0:19]


class CheckViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = CheckSerializer
    queryset = Check.objects.all().order_by('-id')[0:19]


class RecipeViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class NameViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = NameSerializer
    queryset = Name.objects.all()


#####
# THE /game/ function
#####

class GameView(APIView):

    def get(self, request, format=None):
        """ Gets a dataset containing a random monster and three random
        melodies. Saves this data as a new 'Game' entry and returns its ID
        so that it can be checked by the CheckGame function. """

        ANIMAL = 666

        # dataset for the response - everything should be well ordered
        # to be readable by humans, too
        data = OrderedDict()

        # STEP A: THE MONSTER

        # Oh my God, it's time for a special someone!
        now = datetime.datetime.now()
        if now.second in [6, 6*6]:
            rand_monster_pk = ANIMAL
        else:
            # Get a random monster data set
            # 1. get all monster ids as a list
            monster_pks = list(Monster.objects.values_list('pk', flat=True))
            # 2. remove the ANIMAL from the list
            monster_pks.remove(ANIMAL)
            # 3. Choose a random monster id
            rand_monster_pk = choice(monster_pks)

        # get the monster by the random id
        rand_monster = Monster.objects.get(pk=rand_monster_pk)

        # get a list of all melody primary keys
        melody_pks = list(Melody.objects.values_list('pk', flat=True))

        # Remove the pk of the selected monster's melody from melody list to avoid duplicity
        melody_pks.remove(rand_monster.melody.pk)

        # STEP B: THE MELODIES

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
        data['name'] = {
            'forename': rand_monster.name.forename,
            'gender': rand_monster.name.gender,
            'attribute': rand_monster.name.attribute,
            'complete': str(rand_monster.name) }

        melodies = [MelodySerializer(rand_monster.melody).data,
            MelodySerializer(other_melodies[0]).data,
            MelodySerializer(other_melodies[1]).data]

        # the list of three melodies is shuffled, so we do not know
        # which is the right one
        shuffle(melodies)

        data['melodies'] = melodies

        # STEP C: THE GAME

        # save this game to database
        game = Game(monster=rand_monster,
            melody1=rand_monster.melody,
            melody2=other_melodies[0],
            melody3=other_melodies[1])
        game.save()

        data['game_id'] = game.id

        return Response(data)

#####
# DEPRECATED!
# /checkmonster/
#####

class CheckMonster(APIView):
    """ Simple check function
        Parameters: int:monster_id/int:game_id """

    def get(self, request, monster_id, melody_id):
        monster = Monster.objects.filter(pk=monster_id).first()

        return Response({ 'result': monster.melody.pk == melody_id })

#####
# /checkgame/
#####

class CheckGame(APIView):
    """ Check if a certain melody fits a certain monster.<br />
        Parameters: int:game_id/int:melody_id<br />
        Results: <strong>result</strong> : true|false<br/>
        <strong>message</strong> Information if there was an error<br/>
        <strong>recipe</strong> A random recipe from the cuisine of westphalia if <result>
        was false and its wikipedia link."""

    def get(self, request, game_id, melody_id):

        # STEP A: Get the Game and the Melody

        game = Game.objects.filter(id=game_id).first()
        tested_melody = Melody.objects.filter(id=melody_id).first()

        message = ''

        # maybe this check is done manually, or there is another error
        # regarding the ids, so we'll report it.
        if game.monster == None:
            result = False
            message = 'No game.monster found! '

        if tested_melody == None:
            result = false
            message += 'No melody found!'

        # STEP B: Test if the Melody matches this Game (that is: if it's the
        # same Melody that is connected to the Monster within this Game)

        else:
            result = (game.monster.melody == tested_melody)
            # doesn't mean that the melody matches, but the Check is successful
            message = '{}/{} OK'.format(game.monster.id, tested_melody.id)

            # save this Check in the db
            check = Check(game=game, monster=game.monster,
                tested_melody=tested_melody, result=result, message=message)
            check.save()

        response = { 'result': result, 'message': message }

        # STEP C: The recipe

        # result false -> append a random recipe from the db
        if result == False:
            recipe_pks = list(Recipe.objects.values_list('pk', flat=True))
            recipe = Recipe.objects.get(pk=choice(recipe_pks))

            response['recipe'] = {
                'title': recipe.title,
                'href': recipe.href }

        return Response(response)


#####
# Other simple views, just for fun(k) ... ;-)
#####


def AllMonsters(request):
    monsters = Monster.objects.all()
    return render(request, 'monsters.html', {'monsters': monsters})


def Welcome(request):
    return render(request, 'welcome.html')

#####
# /stat/
#####

class Stat(APIView):


    def get(self, request, model, startpoint, endpoint):
        # parse startpoint
        start = parse_datetime(startpoint)
        stop = parse_datetime(endpoint)

        print("start", startpoint, start)
        print("stop", endpoint, stop)
        # filter objects

        if model == "checks":
            data = Check.objects.filter(created_date__range=(start, stop))
            data_serializer = StatCheckSerializer(data, many=True)
        elif model == "games":
            data = Game.objects.filter(created_date__range=(start, stop))
            data_serializer = GameSerializer(data, many=True)
        else:
            data_serializer = None

        # create REST serializer
        return Response(data_serializer.data)
