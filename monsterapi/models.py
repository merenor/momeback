from django.db import models

# Create your models here.
class Melody(models.Model):
    """ Melodies by Graupner """
    """ TODO: What is actually given by RISM dataset? """

    name = models.CharField(max_length=255, blank=True, null=True)
    mei_data = models.TextField(blank=True, null=True)
    #rism_link = models.URL
    #sound_file =

    def __str__(self):
        return str(self.name)


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
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    dnb_id = models.URLField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Name(models.Model):
    """ Names for little monsters """

    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=3)
    attribute = models.CharField(max_length=50)

    def __str__(self):
        return "{n}, {g} {a}e".format(n = self.name, g = self.gender,
            a = self.attribute[:1].upper() + self.attribute[1:])


class Monster(models.Model):
    """ Our litte monsters """

    picture_id = models.CharField(max_length=255, blank=True, null=True)
    file_format = models.CharField(max_length=4, blank=True, null=True)
    #image = models.ImageField(upload_to='media/monster_pics/', default='media/monster_pics/leo.png', blank=True, null=True)
    picture_filename = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bible_passage = models.CharField(max_length=20, blank=True, null=True)
    bible_text = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    melody = models.ForeignKey(Melody, on_delete=models.CASCADE, blank=True, null=True)
    motives = models.ManyToManyField(Motive, blank=True)
    name = models.ForeignKey(Name, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.description)
