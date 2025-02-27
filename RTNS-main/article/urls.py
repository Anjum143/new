from django.urls import path
from .views import *

app_name="article"

urlpatterns=[
    path("articles",AprovedArticles,name="approve_article"),
    path("article/<int:article_id>/",SingleArticle,name="single_article")
    
]