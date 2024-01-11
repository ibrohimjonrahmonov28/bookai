from rest_framework import serializers
from MyUser.models import Users
from .models import Category, Book, Rating, SlideBar, Comment, Favorite, BookViews

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    category_info=serializers.SerializerMethodField()
    def get_category_info(self,obj):
        return obj.category.name

    class Meta:
        model = Book
        fields="__all__"



class BookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookViews
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Favorite
        fields = '__all__'  


# class SlideBarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SlideBar
#         fields = '__all__'

# class CommentSerializer(serializers.ModelSerializer):
#     user = UsersSerializer()
#     book = BookSerializer()

#     class Meta:
#         model = Comment
#         fields = '__all__'

# class FavoriteSerializer(serializers.ModelSerializer):
#     user = UsersSerializer()
#     book = BookSerializer()

#     class Meta:
#         model = Favorite
#         fields = '__all__'
