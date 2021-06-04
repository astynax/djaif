from django.urls import path

from djaif.book import views

urlpatterns = [
    path('', views.view_books),
    path('book/<int:book_id>', views.view_book, name='book'),
    path('book/<int:book_id>/go/<int:pagelink_id>', views.go_to, name='go_to'),
    path('book/<int:book_id>/saves', views.view_saves, name='saves'),
    path('book/<int:book_id>/take/<int:item_id>', views.take, name='take'),
    path('book/<int:book_id>/drop/<int:item_id>', views.drop, name='drop'),
    path(
        'book/<int:book_id>/take_back/<int:dropped_item_id>',
        views.take_back,
        name='take_back',
    ),
    path(
        'book/<int:book_id>/saves/new',
        views.save_to,
        name='save_new',
    ),
    path(
        'book/<int:book_id>/saves/save_to/<int:save_id>',
        views.save_to,
        name='save_to',
    ),
    path(
        'book/<int:book_id>/saves/load_from/<int:save_id>',
        views.load_from,
        name='load_from',
    ),
    path(
        'book/<int:book_id>/saves/delete/<int:save_id>',
        views.delete_save,
        name='delete_save',
    ),
    path(
        'book/<int:book_id>/notes/add',
        views.add_note,
        name='add_note',
    ),
    path(
        'book/<int:book_id>/notes/delete/<int:note_id>',
        views.delete_note,
        name='delete_note',
    ),
    path(
        'book/<int:book_id>/notes/toggle/<int:note_id>',
        views.toggle_note,
        name='toggle_note',
    ),
    path(
        'book/<int:book_id>/notes/update/<int:note_id>',
        views.update_note,
        name='update_note',
    ),
    path('book/<int:book_id>/map.svg', views.view_book_map),
]
