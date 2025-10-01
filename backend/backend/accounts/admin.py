from django.contrib import admin

from .models import ExpenceTrackerUser, Profile


@admin.register(ExpenceTrackerUser)
class ExpenceTrackerUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('user__email', 'first_name', 'last_name')
    ordering = ('user__email',)




