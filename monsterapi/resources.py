from import_export import resources
from import_export.fields import Field
from .models import Book, Printer, Owner, Monster
from import_export.widgets import ForeignKeyWidget


class BookResource(resources.ModelResource):

    book_id = Field(attribute='book_id', column_name='BuchID')
    language = Field(attribute='language', column_name='Sprache')
    title = Field(attribute='title', column_name='Titel')
    work = Field(attribute='work', column_name='Werk')
    place_of_publication = Field(attribute='place_of_publication', column_name='Erscheinungsort')
    #printer = Field(attribute='printer', column_name='Drucker', widget=ForeignKeyWidget(Printer, 'name'))
    year = Field(attribute='year', column_name='Erscheinungsjahr')
    dnb_id = Field(attribute='dnb_id', column_name='DnbID')
    #owner = Field(attribute='owner', column_name='Besitzer', widget=ForeignKeyWidget(Owner, 'library'))

    class Meta:
        model = Book


class PrinterResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Name')
    gnd_id = Field(attribute='gnd_id', column_name='GndID')

    class Meta:
        model = Printer


class OwnerResource(resources.ModelResource):
    library = Field(attribute='library', column_name='Bibliothek')
    location = Field(attribute='location', column_name='Ort')
    signature = Field(attribute='signature', column_name='Signatur')

    class Meta:
        model = Owner


class MonsterResource(resources.ModelResource):
    picture_id = Field(attribute='picture_id', column_name='BildID')
    description = Field(attribute='description', column_name='Bildtitel')
    file_format = Field(attribute='file_format', column_name='Format')
    picture_filename = Field(attribute='picture_filename', column_name='Dateiname')
    bible_passage = Field(attribute='bible_passage', column_name='Bibelstelle')
    bible_text = Field(attribute='bible_text', column_name='TextBibelstelle')
    book_id = Field(attribute='book_id', column_name='BuchID', widget=ForeignKeyWidget(Book, "book_id"))

    class Meta:
        model = Monster
