from django.contrib import admin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','first_name','last_name','is_staff','is_active']
    list_filter = ['gender','is_staff','is_superuser','is_active']
    list_editable = ['is_staff','is_active']
    fieldsets = (
        (None, {
            'fields': ('username','password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name','email','gender','age','description')
        }),
        ('Contact info', {
            'fields': ('phone', 'address',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff','is_superuser','groups','user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login','date_joined')
        }),
    )
    filter_horizontal = ('user_permissions','groups')