from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from core import models

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')
        }),
    )

admin.site.register(models.Question)
admin.site.register(models.Course)
admin.site.register(models.TestCase)
admin.site.register(models.Submission)