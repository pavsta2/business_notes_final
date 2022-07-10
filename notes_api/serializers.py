from rest_framework import serializers

from notes_app.models import Note


class NoteListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",  # указываем новое поле для отображения
        read_only=True  # поле для чтения
        )
    class Meta:
        model = Note
        fields = (
            'id', 'title', 'message', 'importance', 'condition', 'date_and_time',  # из модели
            'author',   # из сериализатоллра
        )
