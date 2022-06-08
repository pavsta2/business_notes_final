from django.shortcuts import render
from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from notes_app.models import Note
from .serializers import NoteListSerializer
from . import serializers, filters


class NotesListCreateAPIView(APIView):
    def get(self, request: Request):
        resp = Note.objects.all().order_by("date_and_time", "importance")
        serializer = NoteListSerializer(instance=resp, many=True)
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = serializers.NoteListSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(author=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class NoteDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, pk):
        note = get_object_or_404(Note, pk=pk)
        return Response([
            serializers.NoteListSerializer(note).data
        ])

    def put(self, request: Request, pk):
        user = request.user
        data = request.data
        note = get_object_or_404(Note, pk=pk)
        author = note.author

        if user == author:
            serializer = serializers.NoteListSerializer(instance=note, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

            # note.title = data['title']
            # note.message = data['message']
            # note.public = data['public']
            # note.importance = data['importance']
            # note.condition = data['condition']
            # note.date_and_time = data['date_and_time']
            # note.save()
        #     return Response([
        #     serializers.NoteListSerializer(note).data
        # ])
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        user = request.user
        note = Note.objects.get(pk=pk)
        author = note.author

        if user == author:
            serializer = serializers.NoteListSerializer(instance=note)
            note.delete()
            return Response(f"Удалена запись:{serializer.data}")

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteListSerializer

    def filter_queryset(self, queryset):
        queryset = filters.importance_filter(
            queryset,
            importance=self.request.query_params.get("importance")
        )

        queryset = filters.public_filter(
            queryset,
            public=self.request.query_params.get("public")
        )
        return queryset
