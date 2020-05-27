from django.contrib import admin

from djaif.book import models


class Admin(admin.ModelAdmin):
    filter_horizontal = ('items',)


class BookAdmin(admin.ModelAdmin):
    change_form_template = 'admin/book_change_form.html'


admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookPage, Admin)
admin.site.register(models.PageLink, Admin)
admin.site.register(models.BookProgress)
admin.site.register(models.Item)
