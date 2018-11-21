from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Book, Owner, Printer, Monster, Melody


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

    class Meta:
        model = Book
        fields = ('id', 'book_slug', 'language', 'title', 'work',
            'place_of_publication', 'year', 'dnb_id', 'printer', 'owner',
            'monsters')


class MelodySerializer(ModelSerializer):

    class Meta:
        model = Melody
        fields = ('id', 'work_title', 'movement', 'clef', 'keysig',
            'timesig', 'pae_data', 'rism_id', 'rism_opac_link', 'tu_da_link')


class MonsterSerializer(ModelSerializer):

    class Meta:
        model = Monster
        fields = ("id", "picture_slug", "file_format", "picture_filename",
            "description", "bible_passage", "bible_text", "book", "melody",
            "motives",)
