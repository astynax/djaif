from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from djaif.book import models


def index(request):
    return render(request, "book_index.html", context={
        'books': models.Book.objects.all(),
    })


def book(request, book_id):
    b = get_object_or_404(models.Book, id=book_id)
    if not b.first_page:
        return render(request, "book.html", context={
            'book': b,
        })
    return redirect(reverse('page', kwargs={
        'book_id': b.id, 'page_id': b.first_page.id
    }))


def page(request, book_id, page_id):
    return render(request, "page.html", context={
        'page': get_object_or_404(
            models.BookPage, book__id=book_id, id=page_id,
        ),
    })
