from django.urls import path
from . import views 
from rest_framework.routers import DefaultRouter

router =DefaultRouter()


router.register("books", views.BookView,basename="books")


urlpatterns=[
    path("category", views.CategoryView.as_view(),name="categories"),
    path('categories/<int:category_id>/', views.BooksByCategory.as_view(), name='books-by-category'),
    path('top-books/', views.TopBookView.as_view(), name='top-books'),
    path('favorite/', views.FavoriteView.as_view(), name='favorite'),
    path('search/', views.SearchView.as_view(), name='search'),
    path("audinize/",views.UploadBookView.as_view(),name="audinize"),
    path("ratingcreate/", views.RatingCreateAPIView.as_view(), name= "ratingcreate"),
    path("ratingdetail/<int:pk>/", views.RatingDetailAPIView.as_view(), name ="ratingdetail"),
    path('participants/', views.ParticipantList.as_view(), name='participant-list'),
    path('slidebars/', views.SlideBarsView.as_view(), name='slidebars'),
    path('books/<int:book_id>/comments/', views.BookCommentsAPIView.as_view(), name='book-comments'),
    path("getbook/<int:pk>/", views.OneBookView.as_view()),
    path("recentbook/", views.RecentBooksView.as_view())
    

]+ router.urls

   