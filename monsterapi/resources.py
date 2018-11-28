from import_export import resources
from import_export.fields import Field
from .models import Book, Printer, Owner, Monster, Name, Melody
from import_export.widgets import ForeignKeyWidget

import json

class BookResource(resources.ModelResource):
    book_slug = Field(attribute='book_slug', column_name='BuchID')
    language = Field(attribute='language', column_name='Sprache')
    title = Field(attribute='title', column_name='Titel')
    work = Field(attribute='work', column_name='Werk')
    volume = Field(attribute='volume', column_name='Band')
    place_of_publication = Field(attribute='place_of_publication', column_name='Erscheinungsort')
    year = Field(attribute='year', column_name='Erscheinungsjahr')
    dnb_id = Field(attribute='dnb_id', column_name='DnbID')

    # nested stuff: printer (Drucker) and owner (Besitzer)
    printer = Field(attribute='printer', column_name='Drucker', widget=ForeignKeyWidget(Printer))
    owner = Field(attribute='owner', column_name='Besitzer', widget=ForeignKeyWidget(Owner))

    class Meta:
        model = Book

    def before_import_row(self, row, **kwargs):

        # check the data for printer:
        # get the infos from the current data set
        # check if this printer is already in the database,
        # if not, create data. Finally, add printer.pk to book.
        printer_data = row.get('Drucker')
        (printer, _created) = Printer.objects.get_or_create(
            name=printer_data['Name'],
            gnd_id=printer_data['GndID'])
        row['Drucker'] = printer.pk

        # check the data for owner
        # Same as above
        owner_data = row.get('Besitzer')
        (owner, _created) = Owner.objects.get_or_create(
            library=owner_data['Bibliothek'],
            location=owner_data['Ort'],
            signature=owner_data['Signatur'])
        row['Besitzer'] = owner.pk


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
    picture_slug = Field(attribute='picture_slug', column_name='BildID')
    picture_filename = Field(attribute='picture_filename', column_name='Dateiname')
    file_format = Field(attribute='file_format', column_name='Format')
    description = Field(attribute='description', column_name='Bildtitel')
    bible_passage = Field(attribute='bible_passage', column_name='Bibelstelle')
    bible_text = Field(attribute='bible_text', column_name='TextBibelstelle')
    book_slug = Field(attribute='book', column_name='BuchID',
        widget=ForeignKeyWidget(Book, 'book_slug'))

    class Meta:
        model = Monster

    #def before_import_row(self, row, **kwargs):
    #    book_data = row.get('BuchID')
    #    (book, _created) = Book.objects.get_or_create(book_slug=book_data)
    #    row['BuchID'] = book.pk


class NameResource(resources.ModelResource):
    name = Field(attribute='name', column_name='name')
    gender = Field(attribute='gender', column_name='gender')
    attribute = Field(attribute='attribute', column_name='attribute')

    class Meta:
        model = Name


class MelodyResource(resources.ModelResource):
    work_title = Field(attribute='work_title', column_name='work_title')
    movement = Field(attribute='movement', column_name='movement')
    clef = Field(attribute='clef', column_name='clef')
    keysig = Field(attribute='keysig', column_name='keysig')
    timesig = Field(attribute='timesig', column_name='timesig')
    pae_data = Field(attribute='pae_data', column_name='pae_data')
    rism_id = Field(attribute='rism_id', column_name='rism_id')
    rism_opac_link = Field(attribute='rism_opac_link', column_name='rism_opac_link')
    tu_da_link = Field(attribute='tu_da_link', column_name='tu_da_link')

    class Meta:
        model = Melody
