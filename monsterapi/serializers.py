from rest_framework import serializers
from .models import Monster


class MonsterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Monster
        fields = ("picture_id", "file_format", "picture_filename", "description",
        "bible_passage", "bible_text", "book_id", "melody", "motives",)
