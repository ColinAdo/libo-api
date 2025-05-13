import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from books.models import Book, Category
from likes.models import Like
from bookmark.models import Bookmark

# Account consumer
class BookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            self.close()
            return

        self.username = user.username
        await self.channel_layer.group_add(
            self.username, 
            self.channel_name
        )
        await self.accept()
        logging.info(f'User connected to room: {self.username}')
        print(f"{self.username} connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.username, 
            self.channel_name
        )
        logging.info(f"User disconnected from room: {self.username}")
        print(f"{self.username} disconnected")

    # Parse the received JSON data
    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Received", json.dumps(data, indent=2))

        operation = data['event']
        

        # Send the message to the group if create_account oppereation
        if operation == 'create_book':
            category = data['data']['category']
            author = data['data']['author']
            title = data['data']['title']
            cover_image = data['data']['cover_image']
            pdf_file = data['data']['pdf_file']
            description = data['data']['description']
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'create_book',
                    'category': category,
                    'author': author,
                    'title': title,
                    'cover_image': cover_image,
                    'pdf_file': pdf_file,
                    'description': description,
                }
            )
            await self.save_book(category, author, title, cover_image, pdf_file, description)
        
        elif operation == 'like_book':
            id = data['data']['id']
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'like_book',
                    'id': id,
                }
            )
            await self.save_like(id)

        elif operation == 'bookmark_book':
            id = data['data']['id']
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'bookmark_book',
                    'id': id,
                }
            )
            await self.save_bookmark(id)
       
    # Send the created book to WebSocket
    async def create_book(self, event):
        category = event['category']
        author = event['author']
        title = event['title']
        cover_image = event['cover_image']
        cover_image = event['cover_image']
        pdf_file = event['pdf_file']
        description = event['description']

        await self.send(text_data=json.dumps({
            'category': category,
            'author': author,
            'author': author,
            'title': title,
            'title': title,
            'cover_image': cover_image,
            'pdf_file': pdf_file,
            'description': description,
        }))

    # Send back the liked book to frontend
    async def like_book(self, event):
        id = event['id']

        await self.send(text_data=json.dumps({
            'id': id,
        }))

    # Send back the bookmarked book to frontend
    async def bookmark_book(self, event):
        id = event['id']

        await self.send(text_data=json.dumps({
            'id': id,
        }))

    async def chatpdf_message(self, event):
        message = event['message']
        source_id = event['sourceId']

        await self.send(text_data=json.dumps({
            'type': 'chatpdf_response',
            'message': message,
            'sourceId': source_id,
        }))


    @sync_to_async
    def save_book(self, category, author, title, cover_image, pdf_file, description):
        # user = self.scope.get('user')

        cat = Category.objects.get(title=category)
        Book.objects.create(category=cat, author=author, title=title, cover_image=cover_image, pdf_file=pdf_file, description=description)

    @sync_to_async
    def save_like(self, id):
        user = self.scope.get('user')

        isLiked = Like.objects.filter(user=user, book=id).exists()
        book = Book.objects.get(id=id)

        if isLiked:
            Like.objects.get(user=user, book=id).delete()
        else:
            Like.objects.create(user=user, book=book)

    @sync_to_async
    def save_bookmark(self, id):
        user = self.scope.get('user')

        isBookmarked = Bookmark.objects.filter(user=user, book=id).exists()
        book = Book.objects.get(id=id)

        print("Is liked", isBookmarked)
        if isBookmarked:
            Bookmark.objects.get(user=user, book=id).delete()
        else:
            Bookmark.objects.create(user=user, book=book)
