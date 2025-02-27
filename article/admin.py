from django.contrib import admin
from article.models import Article 
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display=['title','author','article_file','status','event']
    search_fields = ['title', 'author__username']
    list_filter = ['status', 'event']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj) + ('title', 'author', 'article_file','event')

        return readonly_fields
    
    def save_and_add_another(self, request, obj, form, change):
        
        return False
    
    def has_add_permission(self, request):
        return False
# Register your models here.
# admin.site.register(Article,ArticleAdmin)