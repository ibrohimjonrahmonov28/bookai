from django.db import models
from  account.models import User

class Category(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 150, unique=True )
	icon = models.FileField(upload_to = "media/icons/",null=True,blank=True)
	create_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.name

class Book(models.Model):
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length=100, db_index=True,null=True)
	price = models.IntegerField()
	isbn_number = models.CharField(max_length = 100)
	description = models.TextField()
	views_count= models.IntegerField(default=0)
	bookfile = models.FileField(upload_to = "media/books/",null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.name
 
class AudioFile(models.Model):
	book=models.ForeignKey(Book,on_delete=models.CASCADE)
	file=models.FileField(upload_to= "media/audio/", blank=True)

class Participant(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	author=models.ForeignKey(User,on_delete=models.CASCADE)


class Rating(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	book=models.ForeignKey(Book,on_delete=models.CASCADE)
	description=models.TextField()
	score=models.IntegerField()
	created_data=models.DateTimeField(auto_now_add=True)
	updated_data=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f" user {self.user} score {self.score} "

class SlideBar(models.Model):
	title = models.CharField(max_length=150)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	slideimg = models.ImageField(upload_to = "media/slide/",null= True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	book=models.ForeignKey(Book, on_delete=models.CASCADE)
	user=models.ForeignKey(User, on_delete= models.CASCADE)
	body=models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)



class Favorite(models.Model):
	user=models.ForeignKey(User,on_delete= models.CASCADE)
	book=models.ForeignKey(Book,on_delete=models.CASCADE)
	

class BookViews(models.Model):
	book=models.ForeignKey(Book,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)


# top_views = BookViews.objects.filter(created_at__gte="xxx-xx-xx", ceated_at__lte="xxx-xx-xx")
# books = Book.objects.filder(id__in=top_views.values_list("book_id", flat=True)).order_by("-views_count")[::10]