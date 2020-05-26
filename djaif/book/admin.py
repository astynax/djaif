from django.contrib import admin

from djaif.book import models

class Admin(admin.ModelAdmin):
    filter_horizontal = ('items',)

admin.site.register(models.Book)
admin.site.register(models.BookPage, Admin)
admin.site.register(models.PageLink, Admin)
admin.site.register(models.BookProgress)
admin.site.register(models.Item)
