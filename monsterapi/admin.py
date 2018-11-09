from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Book, Printer, Owner, Monster, Name, Melody
from .resources import BookResource, PrinterResource, OwnerResource, MonsterResource, NameResource, MelodyResource

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource

@admin.register(Printer)
class PrinterAdmin(ImportExportModelAdmin):
    resource_class = BookResource

@admin.register(Owner)
class OwnerAdmin(ImportExportModelAdmin):
    resource_class = BookResource

@admin.register(Monster)
class MonsterAdmin(ImportExportModelAdmin):
    resource_class = MonsterResource

@admin.register(Name)
class NameAdmin(ImportExportModelAdmin):
    resource_class = NameResource

@admin.register(Melody)
class MelodyAdmin(ImportExportModelAdmin):
    resource_class = MelodyResource

# Register your models here.
