from django.contrib.auth.models import User
from django.db import models


# Create your models here.
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
        progress = BookProgress(user=user, book=book, book_page=book.first_page)
        progress.save()
        return progress

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

    def load_from(self, save_id):
        state = ProgressSave.objects.get(id=save_id)
        self.book_page = state.book_page  # noqa: WPS601
        self.save()
        self.items.set(state.items.all())


class ProgressSave(models.Model):
    progress = models.ForeignKey(BookProgress, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)

    book_page = models.ForeignKey(BookPage, on_delete=models.CASCADE)

    items = models.ManyToManyField('book.Item', blank=True)  # noqa: WPS110


class Item(models.Model):
    name = models.TextField()

    def __str__(self):
        return '{self.name}'.format(self=self)
