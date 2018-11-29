from django.db import models
from random import choice
from django.utils import timezone

# Create your models here.
class Melody(models.Model):
    """ Melodies by Graupner """

    class Meta:
        verbose_name_plural = "melodies"

    work_title = models.CharField(max_length=100, blank=True, null=True)
    movement = models.CharField(max_length=100, blank=True, null=True)
    clef = models.CharField(max_length=10, blank=True, null=True)
    keysig = models.CharField(max_length=10, blank=True, null=True)
    timesig = models.CharField(max_length=10, blank=True, null=True)
    pae_data = models.TextField(blank=True, null=True)
    rism_id = models.PositiveIntegerField(blank=True, null=True)
    rism_opac_link = models.CharField(max_length=255, blank=True, null=True)
    tu_da_link = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return str('[{i}] {t} - {m}'.format(i=self.id, t=self.work_title,
            m=self.movement))


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
        return "{lib}, {loc} ({sig})".format(
            lib=self.library,
            loc=self.location,
            sig=self.signature)


class Motive(models.Model):
    """ Monster Types """

    name = models.CharField(max_length=255, blank=True, null=True)


class Book(models.Model):
    """ Bibles """

    book_slug = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=400, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    work = models.CharField(max_length=255, blank=True, null=True)
    volume = models.CharField(max_length=3, blank=True, null=True)
    place_of_publication = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
    dnb_id = models.URLField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{t} ({p} {y})".format(
            t=self.title,
            p=self.place_of_publication,
            y=self.year)


class Name(models.Model):
    """ Names for little monsters """
    class Meta:
        ordering = ['gender', 'forename', 'attribute']

    forename = models.CharField(max_length=50)
    gender = models.CharField(max_length=3)
    attribute = models.CharField(max_length=50)

    def __str__(self):
        # creates german noun from an adjective
        # i.e. "grausam" -> "Grausame", but also "feige" -> "Feige"
        the_attribute = self.attribute[:1].upper() + self.attribute[1:]
        if not self.attribute.endswith('e'):
            the_attribute += 'e'

        return "{forename}, {gender} {attribute}".format(
            forename=self.forename,
            gender=self.gender,
            attribute=the_attribute)


class Monster(models.Model):
    """ Our litte monsters """

    class Meta:
        ordering = ['name']

    picture_slug = models.CharField(max_length=255, blank=True, null=True)
    picture_filename = models.CharField(max_length=255, blank=True, null=True)
    file_format = models.CharField(max_length=4, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bible_passage = models.CharField(max_length=20, blank=True, null=True)
    bible_text = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Book, related_name='monsters',
        on_delete=models.CASCADE, blank=True, null=True)
    melody = models.ForeignKey(Melody, on_delete=models.CASCADE, blank=True,
        null=True)
    # not implemented yet
    # motives = models.ManyToManyField(Motive, blank=True)
    # not implemented yet - image has to be added manually in Django admin :(
    # image = models.ImageField(upload_to='media/monster_pics/',
    #    default='media/monster_pics/leo.png', blank=True, null=True)
    name = models.ForeignKey(Name, on_delete=models.CASCADE, blank=True,
    null=True)

    def save(self, *args, **kwargs):

        # Generate a random name for this monster
        if not self.name:
            name_pks = list(Name.objects.values_list('pk', flat=True))

            # delete all name_pks that are already used
            monstername_pks = list(Monster.objects.values_list('name',
                flat=True))
            for monstername_pk in monstername_pks:
                if monstername_pk in name_pks:
                    name_pks.remove(monstername_pk)

            rand_name_pk = choice(name_pks)
            self.name = Name.objects.get(pk=rand_name_pk)

        # generate a custom melody
        if not self.melody:
            melody_pks = list(Melody.objects.values_list('pk', flat=True))

            # delete all melody_pks that are already used
            monstermelody_pks = list(Monster.objects.values_list('melody',
                flat=True))
            for monstermelody_pk in monstermelody_pks:
                if monstermelody_pk in melody_pks:
                    melody_pks.remove(monstermelody_pk)

            rand_melody_pk = choice(list(melody_pks))
            self.melody = Melody.objects.get(pk=rand_melody_pk)

        super().save(*args, **kwargs)


    def __str__(self):
        return "{n} [{d}]".format(n=self.name, d=self.description)


class Game(models.Model):
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE, blank=True,
        null=True)
    melody1 = models.ForeignKey(Melody, related_name='melody1',
        on_delete=models.CASCADE, blank=True, null=True)
    melody2 = models.ForeignKey(Melody, related_name='melody2',
        on_delete=models.CASCADE, blank=True, null=True)
    melody3 = models.ForeignKey(Melody, related_name='melody3',
        on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return "{:%d.%m.%y, %H:%M:%S} | {}".format(
            self.created_date,
            self.monster.name)


class Check(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True,
        null=True)
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE, blank=True,
        null=True)
    tested_melody = models.ForeignKey(Melody, on_delete=models.CASCADE, blank=True,
        null=True)
    result = models.BooleanField(default=None)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{:%d.%m.%y, %H:%M:%S} | {mon} + {mel} = {res}".format(
            self.created_date,
            mon=self.monster.name if self.monster else "?",
            mel=self.tested_melody.work_title if self.tested_melody else "?",
            res="✓" if self.result else "X")
