from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.








class UserModelAdmin(UserAdmin):
   
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'number','name', 'is_admin')
    list_filter = ( 'is_admin','is_verified')
    fieldsets = (
        ('User Credential', {'fields': ('email', 'number','password','otp')}),
        ('Personal info', {'fields': ('name','description')}),
        ('Permissions', {'fields': ('is_admin','is_verified')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'number','name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'number','name',)
    ordering = ('email', 'number','name',)
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)