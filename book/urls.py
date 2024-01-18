from django.urls import path
from . import views 
from rest_framework.routers import DefaultRouter

# router=DefaultRouter()
# router.register("books", views.BookView,basename="books")


urlpatterns=[
    path("category", views.CategoryView.as_view(),name="categories"),
    path('categories/<slug:category_slug>/books/', views.BooksByCategory.as_view(), name='books-by-category'),
    path('top-books/', views.TopBookView.as_view(), name='top-books'),
    path('favorite/', views.FavoriteView.as_view(), name='favorite'),
    path('search/', views.SearchView.as_view(), name='search'),

]

    # path("", views.category_list,name="category_list"),
    # path("category/<int:category_id>", views.book_by_category,name="book_by_category"),