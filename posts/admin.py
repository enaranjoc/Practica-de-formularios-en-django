from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('autor', 'titulo', 'descripcion')

admin.site.register(Post, PostAdmin)