from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
# Register your models here.
@admin.register(Post)
@admin.register(Category)
@admin.register(Resume)
class ProductAdmin(TranslationAdmin):
    group_fieldsets = True    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            '/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(Connection)
admin.site.register(Portfolio)
admin.site.register(Comment)
admin.site.register(Image_for_detail)
