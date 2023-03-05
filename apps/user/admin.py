from django.contrib import admin

from django.contrib.auth import get_user_model
User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','is_staff','is_superuser','is_active','last_login' )
    list_display_links = ('email', )
    search_fields = ('email','is_staff','is_superuser','is_active','last_login' )

admin.site.register(User, UserAdmin)