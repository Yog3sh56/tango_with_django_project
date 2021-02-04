from django.contrib import admin
from rango.models import Category, Page

# Register your models here.
#admin.site.register(Category)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


admin.site.register(Page, PageAdmin)


# Add in the class to customize the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slugs': ('name',)}


# Update the registration to include this customised interface
admin.site.register(Category, CategoryAdmin)
