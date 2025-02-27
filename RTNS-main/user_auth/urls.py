from django.urls import path
from user_auth import views 

from django.urls import reverse
app_name="user_auth"

urlpatterns=[
    path("sign_up/",views.sign_up,name="user_signup"),
    path("sign_in/",views.login_view,name="user_signin"),
    path("sign_out/",views.LogOut_View,name="user_signout"),
    path("user_dashboard/",views.User_dashboard,name="user_dashboard"),
    #email verifications patterns
    path("error/",views.error_page,name="error"),
    path("token_send/",views.token_send,name="token_send"),
    path("verify/<uuid:email_token>",views.verify,name="verify"),
]