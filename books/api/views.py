from django.conf import settings

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Book
from books.api.serializers import BookSerializer

import openai
from openai.error import RateLimitError

class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def chat(self, request, pk=None):
        book = self.get_object()
        question = request.data.get('question', '')
        try:
            response = self.generate_response(book.text_content, question)
            return Response({'question': question, 'response': response})
        except RateLimitError:
            return Response({'error': 'Rate limit exceeded. Please try again later.'}, status=429)

    @action(detail=True, methods=['get'])
    def summarize(self, request, pk=None):
        book = self.get_object()
        try:
            summary = self.generate_summary(book.text_content)
            return Response({'summary': summary})
        except RateLimitError:
            return Response({'error': 'Rate limit exceeded. Please try again later.'}, status=429)

    def generate_response(self, text, question):
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Text: {text}\n\nQuestion: {question}\nAnswer:"}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()

    def generate_summary(self, text):
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
