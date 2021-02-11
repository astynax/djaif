from functools import wraps

from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from djaif.book import book_map, models


def _return_to(book_id):
    return redirect(reverse('book', kwargs={'book_id': book_id}))


def on_progress(view):
    @wraps(view)  # noqa: WPS430
    def inner(request, book_id, **kwargs):
        try:
            progress = models.BookProgress.objects.get(
                book=book_id, user=request.user,
            )
        except models.BookProgress.DoesNotExist:
            return redirect(reverse('book', kwargs={'book_id': book_id}))
        return view(
            request=request, progress=progress, book_id=book_id, **kwargs,
        )

    return inner


def view_books(request):
    return render(
        request,
        'book_index.html',
        context={'books': models.Book.objects.all()},
    )


def view_book(request, book_id):
    book = get_object_or_404(models.Book, id=book_id)
    if not book.first_page:
        raise ValueError("Book {0.id} hasn't a first page!")
    try:
        progress = models.BookProgress.objects.get(
            book=book, user=request.user,
        )
    except models.BookProgress.DoesNotExist:
        progress = models.BookProgress.start_reading(
            book=book, user=request.user,
        )

    page = progress.book_page

    links = [
        (link, link.has_all_needed(list(progress.items.all())))
        for link in page.pagelink_set.all()
    ]

    return render(
        request,
        'page.html',
        context={
            'page': page,
            'progress': progress,
            'links': links,
            'page_items': page.items.exclude(id__in=progress.items.only('id')),
        },
    )


@on_progress
def go_to(request, progress, book_id, pagelink_id):
    link = get_object_or_404(models.PageLink, id=pagelink_id)
    if (
        link.from_page.id == progress.book_page.id
        and
        link.has_all_needed(progress.items.all())
    ):
        progress.book_page = link.to_page
        progress.save()
    return _return_to(book_id)


@on_progress
def take(request, progress, book_id, item_id):
    item = get_object_or_404(models.Item, id=item_id)  # noqa: WPS110

    if item in progress.book_page.items.all():
        progress.items.add(item)

    return _return_to(book_id)


@on_progress
def view_saves(request, progress, book_id):
    saves = progress.progresssave_set.order_by('-updated_at').all()
    return render(
        request,
        'saves.html',
        context={
            'book': progress.book,
            'page': progress.book_page,
            'saves': saves,
        },
    )


@on_progress
def save_to(request, progress, book_id, save_id=None):
    progress.save_to(save_id)
    return redirect(reverse('saves', kwargs={'book_id': book_id}))


@on_progress
def load_from(request, progress, book_id, save_id):
    progress.load_from(save_id)
    return _return_to(book_id)


def delete_save(request, book_id, save_id):
    models.ProgressSave.objects.get(id=save_id).delete()
    return redirect(reverse('saves', kwargs={'book_id': book_id}))


def view_book_map(request, book_id):
    book = get_object_or_404(models.Book, id=book_id)
    return FileResponse(book_map.book_map(book), filename='map.svg')
