from import_export import resources
from import_export.fields import Field
from .models import Book, Printer, Owner, Monster, Name, Melody
from import_export.widgets import ForeignKeyWidget

import json

class BookResource(resources.ModelResource):
    book_id = Field(attribute='book_id', column_name='BuchID')
    language = Field(attribute='language', column_name='Sprache')
    title = Field(attribute='title', column_name='Titel')
    work = Field(attribute='work', column_name='Werk')
    place_of_publication = Field(attribute='place_of_publication', column_name='Erscheinungsort')
    year = Field(attribute='year', column_name='Erscheinungsjahr')
    dnb_id = Field(attribute='dnb_id', column_name='DnbID')

    # nested stuff
    printer_id = Field(attribute='printer_id', column_name='Drucker', widget=ForeignKeyWidget(Printer))
    owner = Field(attribute='owner', column_name='Besitzer', widget=ForeignKeyWidget(Owner))

    class Meta:
        model = Book

    def before_import_row(self, row, **kwargs):

        # check data for printer
        printer_data = row.get('Drucker')
        (printer, _created) = Printer.objects.get_or_create(
            name=printer_data['Name'],
            gnd_id=printer_data['GndID'])
        row['Drucker'] = printer.id

        # check data for owner
        owner_data = row.get('Besitzer')
        (owner, _created) = Owner.objects.get_or_create(
            library=owner_data['Bibliothek'],
            location=owner_data['Ort'],
            signature=owner_data['Signatur'])
        row['Besitzer'] = owner.id


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


class NameResource(resources.ModelResource):
    name = Field(attribute='name', column_name='name')
    gender = Field(attribute='gender', column_name='gender')
    attribute = Field(attribute='attribute', column_name='attribute')

    class Meta:
        model = Name


class MelodyResource(resources.ModelResource):
    title = Field(attribute='title', column_name='Werktitel')
    gwv = Field(attribute='gwv', column_name='WerkverzeichnisNummer')
    instrument = Field(attribute='instrument', column_name='Partiturstimme')
    clef = Field(attribute='clef', column_name='clef')
    keysig = Field(attribute='keysig', column_name='keysig')
    timesig = Field(attribute='timesig', column_name='timesig')
    pae_data = Field(attribute='pae_data', column_name='pae_data')
    mei_data = Field(attribute='mei_data', column_name='mei_data')

    class Meta:
        model = Melody
