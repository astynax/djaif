from django.contrib.auth.models import User
from django.db import models, transaction


class Book(models.Model):
    title = models.CharField(name='title', max_length=100, unique=True)
    first_page = models.ForeignKey(
        'BookPage', null=True, on_delete=models.SET_NULL,
        related_name='first_name',
    )
    cover_art = models.ImageField(null=True, blank=True)

    def __str__(self):
        return '{self.title} ({self.id})'.format(self=self)


class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(name='title', max_length=100)
    body = models.TextField(name='body')

    items = models.ManyToManyField('book.Item', blank=True)  # noqa: WPS110

    def __str__(self):
        return '{self.title} ({self.id})'.format(self=self)


class PageLink(models.Model):
    from_page = models.ForeignKey(BookPage, on_delete=models.CASCADE)
    to_page = models.ForeignKey(
        BookPage, on_delete=models.CASCADE, related_name='to_page',
    )
    name = models.TextField()

    items = models.ManyToManyField('book.Item', blank=True)  # noqa: WPS110

    class Meta:
        unique_together = ['from_page', 'to_page']

    def __str__(self):
        return (
            '{self.from_page.title} ➝ {self.to_page.title} '
            '({self.id})'.format(
                self=self,
            )
        )

    def has_all_needed(self, items):
        return all(i in items for i in self.items.all())


class BookProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_page = models.ForeignKey(BookPage, on_delete=models.CASCADE)

    items = models.ManyToManyField('book.Item', blank=True)  # noqa: WPS110

    class Meta:
        unique_together = ['user', 'book']

    @classmethod
    def start_reading(cls, user, book):
        progress = BookProgress(
            user=user, book=book, book_page=book.first_page,
        )
        progress.save()
        return progress

    @transaction.atomic
    def save_to(self, save_id):
        if save_id is None:
            state = ProgressSave.objects.create(
                progress=self,
                book_page=self.book_page,
            )
            state.items.set(self.items.all())
        else:
            state = ProgressSave.objects.get(id=save_id)
            state.book_page = self.book_page
            state.save()
            state.items.set(self.items.all())
            state.droppeditemsave_set.all().delete()
        for di in self.droppeditem_set.all():
            DroppedItemSave(
                item=di.item,
                book_page=di.book_page,
                progress_save=state,
            ).save()

    @transaction.atomic
    def load_from(self, save_id):
        state = ProgressSave.objects.get(id=save_id)
        self.book_page = state.book_page  # noqa: WPS601
        self.save()
        self.items.set(state.items.all())
        self.droppeditem_set.all().delete()
        for dis in state.droppeditemsave_set.all():
            DroppedItem(
                item=dis.item,
                book_page=dis.book_page,
                book_progress=self,
            ).save()

    def notes(self):
        """Return a prepared set of notes.

        These notes will be annotated with relation to the
        current page and will appear in order:

        1. pinned notes (key=0, pinned=True)
        2. current page notes (key=1)
        3. other notes (key=0, pinned=False)

        Within each group the notes will be ordered
        by decreasing of 'updated_at'.
        """
        return Note.objects.filter(
            progress=self,
        ).annotate(
            key=models.Count(
                'page',
                filter=models.Q(page=self.book_page),
            ),
        ).order_by(
            '-pinned',
            '-key',
            '-updated_at',
        )


class ProgressSave(models.Model):
    progress = models.ForeignKey(BookProgress, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)

    book_page = models.ForeignKey(BookPage, on_delete=models.CASCADE)

    items = models.ManyToManyField('book.Item', blank=True)  # noqa: WPS110


class Item(models.Model):
    name = models.TextField()

    def __str__(self):
        return '{self.name}'.format(self=self)


class DroppedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    book_page = models.ForeignKey(BookPage, on_delete=models.CASCADE)
    book_progress = models.ForeignKey(BookProgress, on_delete=models.CASCADE)

    def __str__(self):
        return '{self.item.name} ({self.book_page.title})'.format(self=self)


class DroppedItemSave(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    book_page = models.ForeignKey(BookPage, on_delete=models.CASCADE)
    progress_save = models.ForeignKey(ProgressSave, on_delete=models.CASCADE)


class Note(models.Model):
    text = models.TextField()
    progress = models.ForeignKey(BookProgress, on_delete=models.CASCADE)
    page = models.ForeignKey(
        BookPage,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
