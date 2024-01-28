from django.shortcuts import render
from .serializers import CategorySerializer,RatingCustomSerializer,CommentPutSerializer, DateRangeSerializer,CommentSerializer,BookSerializer, SlideBarSerializer, BookViewSerializer, FavoriteSerializer,UploadBookSerializer,RatingSerializer,ParticipantSerializer
from rest_framework.viewsets import ModelViewSet
from . models import Category,Book,BookViews,Favorite,Participant,Rating,SlideBar,Comment,AudioFile
from rest_framework.views import APIView
from itertools import chain
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from django.db.models import Count
# from .permission import OnlyMyUser
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from account.models import User
from django.db.models import F,Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import filters
from django.core.cache import cache
from .helper import read_book
from openai import OpenAI
from . audionizer import audionizer
from rest_framework import status
from . filters import ParticipantFilter
from tempfile import NamedTemporaryFile
import os
from django.conf import settings



class CategoryView(ListAPIView): #DONE
    serializer_class=CategorySerializer
    queryset=Category.objects.all()
    # done

class BooksByCategory(APIView): #DONE
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        books = Book.objects.filter(category=category)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #done


class BookView(ModelViewSet): #DONE
    serializer_class=BookSerializer
    queryset = Book.objects.filter()

    def list(self, request, *args, **kwargs):
        is_zero = Book.objects.filter(views_count__gt=0).exists()

        if is_zero == False:
            result = []
            categories = Category.objects.all()
            for category in categories:
                book_by_category = list(Book.objects.filter(category_id=category.id).order_by("-id")[:3])
                result.append(book_by_category)
            queryset = list(chain(*result))
        else:
            result = []
            categories = Category.objects.all()
            for category in categories:
                book_by_category = list(Book.objects.filter(category_id=category.id).order_by("-views_count")[:3])
                result.append(book_by_category)

            queryset = list(chain(*result))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        book_view = BookViews.objects.create(
            user=request.user, book=instance, created_at=timezone.now()
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        # done 

class OneBookView(APIView): #DONE
    def get(self ,request ,pk):
        book = Book.objects.get(id=pk)
        serializer= BookSerializer(book)
        return Response(serializer.data) #done


class TopBookView(APIView):
    def get(self, request):
        one_month_ago = timezone.now() - timedelta(days=30)
        top_books = BookViews.objects.filter(created_at__gte=one_month_ago).values('book').annotate(book_count=Count('book')).order_by('-book_count')[:10]
        book_ids = [book['book'] for book in top_books]
        queryset = Book.objects.filter(id__in=book_ids)
        serializer = BookSerializer(queryset, many=True) 
        return Response(serializer.data)
        #TODO top book larni chiqarish 

class FavoriteView(APIView):   #DONE  
    def get(self, request):
        cache_key = f"favorite_book_{request.user.id}"
        favorite_books = cache.get(cache_key)
        if favorite_books is None:
            favorite_books = Favorite.objects.filter(user=request.user)
            cache.set(cache_key, favorite_books)
        serializer = FavoriteSerializer(favorite_books, many=True)
        return Response(serializer.data) # done


    @swagger_auto_schema(request_body=FavoriteSerializer)
    def post(self, request):
        data = request.data 
        book_id = data["book"]
        book = get_object_or_404(Book, id=book_id)
        favorite = Favorite.objects.create(user=request.user, book=book)
        cache_key = f"favorite_book_{request.user.id}"
        favorite_books = cache.get(cache_key)
        if favorite_books is not None:

            favorite_books.append(favorite)
            cache.set(cache_key, favorite_books)
        else:
            cache.set(cache_key,[favorite])
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)

    def delete(self, request, pk):
        favorite = get_object_or_404(Favorite, pk=pk)
        favorite.delete()
        cache_key = f"favorite_book_{request.user.id}"
        favorite_books = cache.get(cache_key)
        if favorite_books is not None:
            favorite_books = [favorite for favorite in favorite_books if favorite.id != pk]
            cache.set(cache_key, favorite_books)
        else:
            print("Cache is empty. No further actions taken.")
            cache.set(cache_key,[]
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
        # TODO cache ni qayta sozlash 

# class TopBookView(APIView):
#     @swagger_auto_schema(request_body=DateRangeSerializer)
#     def post(self, request):
#         data = request.data
#         start_date = data["start_date"]  
#         end_date = data["end_date"]  
#         top_views = BookViews.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
#         books = Book.objects.filter(id__in=top_views.values_list("book_id", flat=True)).order_by("-views_count")[::10]
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data)


class TopBookView(APIView):
    def get(self, request):
        one_month_ago = timezone.now() - timedelta(days=30)
        top_books = BookViews.objects.filter(created_at__gte=one_month_ago).values('book').annotate(book_count=Count('book')).order_by('-book_count')[:10]
        book_ids = [book['book'] for book in top_books]
        queryset = Book.objects.filter(id__in=book_ids)
        serializer = BookSerializer(queryset, many=True) 
        return Response(serializer.data)

        #TODO top 10 

class SearchView(generics.ListAPIView):  #DONE
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$name', "isbn_number"] # DONE


client = OpenAI(api_key="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")

# class UploadBookView(APIView):
#     @swagger_auto_schema(request_body=UploadBookSerializer)
#     def post(self, request):
#         data = request.data
#         book_id = data.get("book_id")

#         try:
#             book = Book.objects.get(id=book_id)
#             book_path = book.bookfile.path
#             text_content = read_book(book_path)
#             chunk_size = 1000 
#             chunks = [text_content[i:i+chunk_size] for i in range(0, len(text_content), chunk_size)]
#             with NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
#                 for chunk in chunks:
#                     response = client.audio.speech.create(
#                         model="tts-1",
#                         voice="alloy",
#                         input=text_content
#                     )
#                     temp_file.write(response.read())

#                     # desired_filename = f"{book.name}.mp3"  # Customize filename as needed
#                 # try:
#                 #     os.rename(temp_file.name, os.path.join(settings.MEDIA_ROOT, 'audio', desired_filename))
#                 # except OSError as e:
#                 #     return Response({'error': 'Failed to rename audio file: ' + str(e)},
#                 #                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#                 audio_file = AudioFile.objects.create(
#                     book=book,
#                     file=temp_file.name  
#                 )

#             return Response({'audio_file_id': audio_file.id}, status=status.HTTP_201_CREATED)

#         except Book.DoesNotExist:
#             return Response({'error': 'Kitob topilmadi'}, status=status.HTTP_404_NOT_FOUND)
class UploadBookView(APIView):
    @swagger_auto_schema(request_body=UploadBookSerializer)
    def post(self, request):
        data = request.data
        book_id = data.get("book_id")

        try:
            book = Book.objects.get(id=book_id)
            book_path = book.bookfile.path
            text_content = read_book(book_path)

            # Chunk the text content
            chunk_size = 1000 
            chunks = [text_content[i:i+chunk_size] for i in range(0, len(text_content), chunk_size)]

            with NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                for chunk in chunks:
                    response = client.audio.speech.create(
                        model="tts-1",
                        voice="alloy",
                        input=chunk  # Use the current chunk, not the entire text_content
                    )
                    temp_file.write(response.read())

                # Create AudioFile object after processing all chunks
                audio_file = AudioFile.objects.create(
                    book=book,
                    file=temp_file.name  
                )

            return Response({'audio_file_id': text_content}, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({'error': 'Kitob topilmadi'}, status=status.HTTP_404_NOT_FOUND)


class RatingCreateAPIView(APIView): #DONE
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        ratings = Rating.objects.all().order_by("-created_data")
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=RatingCustomSerializer)
    def post(self, request): #DONE
        serializer = RatingCustomSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            book_instance, _ = Book.objects.get_or_create(id=book_id)

            Rating.objects.create(
                user=request.user,
                book=book_instance,
                description=serializer.validated_data['description'],
                score=serializer.validated_data['score']
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #DONE

class RatingDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Rating.objects.get(pk=pk)
        except Rating.DoesNotExist:
            return None

    def get(self, request, pk):
        rating = self.get_object(pk)
        if rating:
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND) # DONE 

    def put(self, request, pk):
        rating = self.get_object(pk)
        if rating:
            serializer = RatingSerializer(rating, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
        # TODO YANADA TAKOMILLASHTIRISH VA TEKSHIRISH

    def delete(self, request, pk):
        rating = self.get_object(pk)
        if rating:
            rating.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
        # DONE

class ParticipantList(generics.ListAPIView): # yanada takomilashtirish 
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filterset_class = ParticipantFilter
    #TODO 

class SlideBarsView(generics.ListAPIView): #done
    serializer_class = SlideBarSerializer
    def get_queryset(self):
        return SlideBar.objects.all().order_by('-created')[:3]
        #DONE 

class BookCommentsAPIView(APIView):
    def get(self, request, book_id):
        comments = Comment.objects.filter(book_id=book_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, book_id):
        request.data['book'] = book_id 
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CommentPutSerializer)
    def put(self, request, book_id):
        comments = Comment.objects.filter(book_id=book_id)
        
        if not comments.exists():
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        request.data["user"] = request.user.id  # Assuming user is related to Comment model
        serializer = CommentSerializer(comments, data=request.data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecentBooksView(generics.ListAPIView): # done 
    serializer_class = BookViewSerializer
    def get_queryset(self):
        return BookViews.objects.filter(user = self.request.user ).order_by("created_at")[:10] #
        # done 