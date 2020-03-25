from django.contrib import admin
from article.models import Post,Category,Tags
# Register your models here.
class Display(admin.ModelAdmin):
    list_display = ['title','author','create_time','category']

admin.site.register(Post,Display)
admin.site.register(Category)
admin.site.register(Tags)
