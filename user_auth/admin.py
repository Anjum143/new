from django.contrib import admin
from user_auth.models import User
from user_auth.models import Profile
class UserList(admin.ModelAdmin):
    list_display=['email','verified']
    readonly_fields=['username','email','password','image','first_name','last_name','last_login','date_joined']
    list_editable=['verified']
    def has_add_permission(self, request):
        return False

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_username')

    def has_add_permission(self, request):
        return False
    
    def get_email(self, obj):
        return obj.user.email

    def get_username(self, obj):
        return obj.user.username

    get_email.admin_order_field = 'user__email'
    get_username.admin_order_field = 'user__username'
    get_email.short_description = 'Email'
    get_username.short_description = 'Username'
# Register your models here.
admin.site.register(User,UserList)
admin.site.register(Profile,ProfileAdmin)