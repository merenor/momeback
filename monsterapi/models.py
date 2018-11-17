from django.db import models
from random import choice

# Create your models here.
class Melody(models.Model):
    """ Melodies by Graupner """
    """ TODO: What is actually given by RISM dataset? """
    class Meta:
        verbose_name_plural = "melodies"

    title = models.CharField(max_length=255, blank=True, null=True)
    gwv = models.CharField(max_length=7, blank=True, null=True)
    instrument = models.CharField(max_length=255, blank=True, null=True)
    clef = models.CharField(max_length=3, blank=True, null=True)
    keysig = models.CharField(max_length=3, blank=True, null=True)
    timesig = models.CharField(max_length=1, blank=True, null=True)
    pae_data = models.TextField(blank=True, null=True)
    mei_data = models.TextField(blank=True, null=True)
    #rism_link = models.URL
    #sound_file =

    def __str__(self):
        return str(self.title)


class Printer(models.Model):
    """ Person """

    name = models.CharField(max_length=255, blank=True, null=True)
    gnd_id = models.URLField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Owner(models.Model):
    """ Library that owns a certain bible """

    library = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    signature = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Motive(models.Model):
    """ Monster Types """

    name = models.CharField(max_length=255, blank=True, null=True)


class Book(models.Model):
    """ Bibles """

    book_id = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    work = models.CharField(max_length=255, blank=True, null=True)
    place_of_publication = models.CharField(max_length=255, blank=True, null=True)
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    dnb_id = models.URLField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Name(models.Model):
    """ Names for little monsters """
    class Meta:
        ordering = ['gender', 'name', 'attribute']

    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=3)
    attribute = models.CharField(max_length=50)

    def __str__(self):
        # creates german noun from an adjective
        # i.e. "grausam" -> "Grausame", but also "feige" -> "Feige"
        the_attribute = self.attribute[:1].upper() + self.attribute[1:]
        if not self.attribute.endswith('e'):
            the_attribute += 'e'

        return "{name}, {gender} {attribute}".format(
            name=self.name,
            gender=self.gender,
            attribute=the_attribute)


class Monster(models.Model):
    """ Our litte monsters """

    picture_id = models.CharField(max_length=255, blank=True, null=True)
    file_format = models.CharField(max_length=4, blank=True, null=True)
    image = models.ImageField(upload_to='media/monster_pics/', default='media/monster_pics/leo.png', blank=True, null=True)
    picture_filename = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bible_passage = models.CharField(max_length=20, blank=True, null=True)
    bible_text = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    melody = models.ForeignKey(Melody, on_delete=models.CASCADE, blank=True, null=True)
    motives = models.ManyToManyField(Motive, blank=True)
    name = models.ForeignKey(Name, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):

        # Generate a name for this monster
        if not self.name:
            name_pks = Name.objects.values_list('pk', flat=True)
            rand_name_pk = choice(list(name_pks))
            self.name = Name.objects.get(pk=rand_name_pk)
            print("CREATE MONSTER NAME!")

        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.description)
