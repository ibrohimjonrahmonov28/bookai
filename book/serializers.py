from rest_framework import serializers
from account.models import User
from .models import Category, Book, Rating, SlideBar, Comment, Favorite, BookViews, Participant
from django.db.models import Avg
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    category_info = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        average_rating = Rating.objects.filter(book=obj).aggregate(Avg('score'))['score__avg']
        if average_rating is not None:
            rounded_average_rating = round(average_rating, 1)
            return rounded_average_rating
        else:
            return 0.0  
    class Meta:
        model = Book
        fields = "__all__"

    def get_category_info(self, obj):
        return {
            'category_name': obj.category.name,
            'category_description': obj.category.id
            
        }


class UploadBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()


class BookViewSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = BookViews
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = Favorite
        fields = '__all__'  

class RatingSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = Rating
        fields = "__all__"

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class SlideBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideBar
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class CommentPutSerializer(serializers.Serializer):
    body = serializers.CharField()
    book_id = serializers.IntegerField()

class RatingCustomSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    description =serializers.CharField()
    score =serializers.IntegerField()

class FavoriteBodySerializer(serializers.Serializer):
    book_id = serializers.IntegerField()