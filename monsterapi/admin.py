from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Book, Printer, Owner, Monster
from .resources import BookResource, PrinterResource, OwnerResource, MonsterResource

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

# Register your models here.
