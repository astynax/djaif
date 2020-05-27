from django.urls import path

from djaif.book import views

urlpatterns = [
    path('', views.view_books),
    path('book/<int:book_id>', views.view_book, name='book'),
    path('book/<int:book_id>/page/<int:page_id>', views.view_page, name='page'),
    path(
        'book/<int:book_id>/page/<int:page_id>/take/<int:item_id>',
        views.take_item,
        name='take',
    ),
    path('book/<int:book_id>/map.svg', views.view_book_map),
]
