from rest_framework import serializers
from account.models import User
from .models import Category, Book, Rating, SlideBar, Comment, Favorite, BookViews, Participant

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    category_info = serializers.SerializerMethodField()

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
