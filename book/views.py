from django.shortcuts import render
from .serializers import CategorySerializer, BookSerializer, BookViewSerializer, FavoriteSerializer,UploadBookSerializer
from rest_framework.viewsets import ModelViewSet
from . models import Category,Book,BookViews,Favorite,Participant,Rating,SlideBar,Comment
from rest_framework.viewsets import mixins
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
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import filters
from django.core.cache import cache
from .helper import read_book

class CategoryView(ListAPIView):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()


class BooksByCategory(APIView):
    def get(self, request, category_slug):
        category = Category.objects.filter(slug=category_slug)
        if not category:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        books = Book.objects.filter(categories=category)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# def category_list(request): 
#     categories = Category.objects.all() 
#     return render(request, 'index.html', {'categories': categories})

# def book_by_category(request, category_id): 
#     books = Book.objects.filter(category_id=category_id) 
#     return render(request, 'book_by_category.html', {'books': books})


class BookView(ModelViewSet):
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



class TopBookView(APIView):
    def get(self, request):
        one_month_ago = timezone.now() - timedelta(days=30)
        top_books = BookViews.objects.filter(created_at__gte=one_month_ago).values('book').annotate(book_count=Count('book')).order_by('-book_count')[:10]
        book_ids = [book['book'] for book in top_books]
        queryset = Book.objects.filter(id__in=book_ids)
        serializer = BookSerializer(queryset, many=True) 
        return Response(serializer.data)

class FavoriteView(APIView):    
    def get(self, request):
        cache_key = f"favorite_book_{request.user.id}"
        favorite_books = cache.get(cache_key)

        if favorite_books is None:
            
            favorite_books = Favorite.objects.filter(user=request.user)
            
            cache.set(cache_key, favorite_books)

        serializer = FavoriteSerializer(favorite_books, many=True)
        return Response(serializer.data)

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

class TopBookView(APIView):
    @swagger_auto_schema(request_body=BookSerializer)
    def post(self, request):
        data=request.data
        start_data=data["start_data"]
        end_data=data["end_data"]
        top_views = BookViews.objects.filter(created_at__gte=start_data, created_at__lte=end_data)
        books = Book.objects.filter(id__in=top_views.values_list("book_id", flat=True)).order_by("-views_count")[::10]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class SearchView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$name']
    
class UploadBookView(APIView):
    @swagger_auto_schema(request_body=UploadBookSerializer)
    def post(self, request):
        data=request.data
        book_id=data["book_id"]
        try:

            book=Book.objects.filter(id=book_id)

            book_path = book['file'].path
            
            # Faylni o'qish va uni matnga aylantirish
            text_content = read_book(book_path)

            # Boshqa logika (masalan, ma'lumotlarni saqlash, kitob obyektini yaratish)...
            
            return Response({'text_content': text_content}, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response({'error': 'Kitob topilmadi'}, status=status.HTTP_404_NOT_FOUND)