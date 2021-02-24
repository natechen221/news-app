from django.contrib import admin
from myNews.models import *

class UserAdmin(admin.ModelAdmin):
        list_display = ('id','user')

class ArticleAdmin(admin.ModelAdmin):
        list_display = ('id','title','author','date','article_pictures','category')

class CategoryAdmin(admin.ModelAdmin):
        list_display = ('name','size')

class CommentAdmin(admin.ModelAdmin):
        list_display = ('id','user','content','parent','object_id')

admin.site.register(UserProfile,UserAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(ArticleCategory,CategoryAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Like)
