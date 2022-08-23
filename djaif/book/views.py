from functools import wraps
from itertools import groupby

from django.db import transaction
from django.db.models import F, Func  # noqa: WPS347
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
        'books.html',
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

    links = [
        (link, link.has_all_needed(list(progress.items.all())))
        for link in progress.book_page.pagelink_set.all()
    ]

    notesets = [
        (name, [
            (
                note.id,
                note.text,
                note.page.title if note.page else '',
            )
            for note in group
        ])
        for name, group in groupby(
            progress.notes().select_related(
                'page',
            ).all(),
            key=lambda note: (
                'page' if note.key else
                'pinned' if note.pinned else
                'other'
            ),
        )
    ]

    return render(
        request,
        'page.html',
        context={
            'page': progress.book_page,
            'progress': progress,
            'links': links,
            'page_items': progress.book_page.items.exclude(
                id__in=progress.items.only('id'),
            ).exclude(
                id__in=progress.droppeditem_set.values_list(
                    'item__id', flat=True,
                ),
            ).all(),
            'dropped_items': progress.droppeditem_set.filter(
                book_page=progress.book_page,
            ).all(),
            'notesets': notesets,
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
def take(request, progress, item_id, **kwargs):
    item = get_object_or_404(models.Item, id=item_id)  # noqa: WPS110

    if item in progress.book_page.items.all():
        progress.items.add(item)

    return _return_to(progress.book.id)


@on_progress
def drop(request, progress, item_id, **kwargs):
    item = get_object_or_404(models.Item, id=item_id)  # noqa: WPS110

    if item in progress.items.all():
        with transaction.atomic():
            models.DroppedItem(
                item=item,
                book_page=progress.book_page,
                book_progress=progress,
            ).save()
            progress.items.remove(item)

    return _return_to(progress.book.id)


@on_progress
def take_back(request, progress, dropped_item_id, **kwargs):
    dropped_item = get_object_or_404(
        models.DroppedItem, id=dropped_item_id,
    )  # noqa: WPS110

    if (
        dropped_item.book_page.id == progress.book_page.id
        and
        dropped_item.book_progress.id == progress.id
    ):
        with transaction.atomic():
            progress.items.add(dropped_item.item)
            dropped_item.delete()

    return _return_to(progress.book.id)


@on_progress
def view_saves(request, progress, book_id):
    saves = progress.progresssave_set.order_by('-updated_at').all()
    return render(
        request,
        'saves.html',
        context={
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
    return render(
        request,
        'map.html',
        context={'book': book_map.book_map(book)},
    )


@on_progress
def add_note(request, progress, book_id):
    page = progress.book_page if 'pin' in request.POST else None
    models.Note.objects.create(
        progress=progress,
        text=request.POST['text'],
        page=page,
    )
    return _return_to(book_id)


def delete_note(request, book_id, note_id):
    models.Note.objects.get(id=note_id).delete()
    return _return_to(book_id)


def toggle_note(request, book_id, note_id):
    models.Note.objects.filter(
        id=note_id,
    ).update(
        pinned=Func(F('pinned'), function='NOT'),
    )
    return _return_to(book_id)


@on_progress
def update_note(request, progress, book_id, note_id):
    note = get_object_or_404(models.Note, id=note_id)
    if request.method == 'GET':
        return render(
            request,
            'note.html',
            context={
                'page': progress.book_page,
                'note': note,
            },
        )
    note.text = request.POST['text']
    note.pinned = 'pinned' in request.POST
    note.page = {
        'keep': note.page,
        'change': progress.book_page,
        'remove': None,
    }[request.POST['page']]
    note.save()
    return _return_to(book_id)
