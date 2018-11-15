from rest_framework.serializers import ModelSerializer
from .models import Book, Owner, Printer, Monster, Melody


class PrinterSerializer(ModelSerializer):
    class Meta:
        model = Printer
        fields = ('id', 'name', 'gnd_id')

    #def create(self, validated_data):
    #    return Printer.objects.create(**validated_data)

    #def update(self, instance, validated_data):
    #    instance.name = validated_data.get('name', instance.name)
    #    instance.gnd_id = validated_data.get('gnd_id', instance.gnd_id)


class OwnerSerializer(ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'library', 'location', 'signature')

    #def create(self, validated_data):
    #    return Owner.objects.create(**validated_data)

    #def update(self, instance, validated_data):
    #    instance.library = validated_data.get('library', instance.library)
    #    instance.location = validated_data.get('location', instance.location)
    #    instance.signature = validated_data.get('signature', instance.signature)


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'book_id', 'language', 'title', 'work',
            'place_of_publication', 'year', 'dnb_id', 'printer', 'owner')

    def create(self, validated_data):
        printer_data = validated_data.pop('printer')
        printer = PrinterSerializer.create(PrinterSerializer(), validated_data=printer_data)
        book, created = Book.objects.update_or_create(printer=printer,
        **validated_data)

        return book

    #def update(self, instance, validated_data):
    #    instance.book_id = validated_data.get('book_id', instance.book_id)
    #    instance.language = validated_data.get('language', instance.language)
    #    instance.title = validated_data.get('title', instance.title)
    #    instance.work = validated_data.get('work', instance.work)
    #    instance.place_of_publication = validated_data.get('place_of_publication', instance.place_of_publication)
    #    instance.year = validated_data.get('year', instance.year)
    #    instance.dnb_id = validated_data.get('dnb_id', instance.dnb_id)
    #    instance.save()
    #    return instance

class MelodySerializer(ModelSerializer):
    class Meta:
        model = Melody
        fields = ("id", "title", "gwv", "clef", "timesig", "keysig",
            "pae_data", "mei_data")


class MonsterSerializer(ModelSerializer):

    class Meta:
        model = Monster
        fields = ("id", "picture_id", "file_format", "picture_filename",
            "description", "bible_passage", "bible_text", "book_id", "melody",
            "motives",)
