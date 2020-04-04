from django.db import models


# Create your models here.
class Book(models.Model):
    """Interactive function."""
    title = models.TextField(name='title', unique=True)
    first_page = models.ForeignKey(
        'BookPage', null=True, on_delete=models.SET_NULL,
        related_name='first_name',
    )
    cover_art = models.ImageField(null=True)

    def __str__(self):
        return '{self.title} ({self.id})'.format(self=self)


class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.TextField(name='title')
    body = models.TextField(name='body')

    def __str__(self):
        return '{self.title} ({self.id})'.format(self=self)


class PageLink(models.Model):
    from_page = models.ForeignKey(BookPage, on_delete=models.CASCADE)
    to_page = models.ForeignKey(
        BookPage, on_delete=models.CASCADE, related_name='to_page',
    )
    name = models.TextField()

    def __str__(self):
        return (
            '{self.from_page.title} ➝ {self.to_page.title} '
            '({self.id})'.format(
                self=self,
            )
        )

    class Meta:
        unique_together = ['from_page', 'to_page']
