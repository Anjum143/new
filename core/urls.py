from django.urls import path
from core.views import index
# from core.views import user_profile
from core import views
from article.views import submit_article
# from django.contrib import admin
app_name = "core"

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("",index,name="index"),
    # path("user_profile",user_profile,name="user_profile")
    # path('submit_article',submit_article,name='submit_article')

]

