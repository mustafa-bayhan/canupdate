from .models import *
from modeltranslation.translator import TranslationOptions,register,translator
    
    
    
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
    
class ResumeTranslationOptions(TranslationOptions):
    fields = ('body',)
    
translator.register(Post, PostTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Resume, ResumeTranslationOptions)