from rest_framework.serializers import (ModelSerializer,
    PrimaryKeyRelatedField, CharField, SerializerMethodField)
from .models import (Book, Owner, Printer, Monster, Melody, Name, Game, Check,
    Recipe)


class PrinterSerializer(ModelSerializer):
    class Meta:
        model = Printer
        fields = ('id', 'name', 'gnd_id')


class OwnerSerializer(ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'library', 'location', 'signature')


class BookSerializer(ModelSerializer):
    monsters = PrimaryKeyRelatedField(many=True, read_only=True)
    printer = PrinterSerializer()
    owner = OwnerSerializer()

    class Meta:
        model = Book
        fields = ('id', 'book_slug', 'language', 'title', 'work', 'volume',
            'place_of_publication', 'year', 'dnb_id', 'printer', 'owner',
            'monsters')


class SimpleBookSerializer(ModelSerializer):
    printer = PrinterSerializer()
    owner = OwnerSerializer()

    class Meta:
        model = Book
        fields = ('id', 'book_slug', 'language', 'title', 'work', 'volume',
            'place_of_publication', 'year', 'dnb_id', 'printer', 'owner')

class NameSerializer(ModelSerializer):
    complete = CharField(source='__str__')

    class Meta:
        model = Name
        fields = ('forename', 'gender', 'attribute', 'complete')


class MelodySerializer(ModelSerializer):
    class Meta:
        model = Melody
        fields = ('id', 'work_title', 'movement', 'clef', 'keysig',
            'timesig', 'pae_data', 'rism_id', 'rism_opac_link', 'tu_da_link')


class MonsterSerializer(ModelSerializer):
    name = NameSerializer()
    melody = MelodySerializer()
    book = SimpleBookSerializer()

    class Meta:
        model = Monster
        fields = ("id", "picture_slug", "file_format", "picture_filename",
            "description", "bible_passage", "bible_text", "book", "name",
            "melody",)


class GameSerializer(ModelSerializer):
    monster = MonsterSerializer()
    melody1 = MelodySerializer()
    melody2 = MelodySerializer()
    melody3 = MelodySerializer()

    class Meta:
        model = Game
        fields = ("id", "created_date", "monster", "melody1",
            "melody2", "melody3")


class CheckSerializer(ModelSerializer):
    game = GameSerializer()
    tested_melody = MelodySerializer()

    class Meta:
        model = Check
        fields = ("id", "created_date", "game", "tested_melody", "result")


class StatCheckSerializer(ModelSerializer):
    """This Serializer is implemented for statistical reasons. It provides
    kind of summarized information about a Check, in contrary of
    CheckSerializer that renders all the nested data, too."""

    monster_name = SerializerMethodField()
    monster_picture_filename = SerializerMethodField()
    melody1_work_title = SerializerMethodField()
    melody2_work_title = SerializerMethodField()
    melody3_work_title = SerializerMethodField()
    tested_melody_work_title = SerializerMethodField()

    class Meta:
        model = Check
        fields = ('id', 'created_date', 'monster_name',
        'monster_picture_filename', 'melody1_work_title', 'melody2_work_title',
        'melody3_work_title', 'tested_melody_work_title', 'result')

    # ''id'' comes from the Check data
    # ''created_date'' comes from the Check data

    def get_monster_name(self, obj):
        return str(obj.monster.name)

    def get_monster_picture_filename(self, obj):
        return obj.monster.picture_filename

    def get_melody1_work_title(self, obj):
        return obj.game.melody1.work_title

    def get_melody2_work_title(self, obj):
        return obj.game.melody2.work_title

    def get_melody3_work_title(self, obj):
        return obj.game.melody3.work_title

    def get_tested_melody_work_title(self, obj):
        return obj.tested_melody.work_title

    # ''result'' is in the Check data itself



class RecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ("id", "title", "href")
