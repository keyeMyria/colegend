# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm as AuthUserChangeForm, UserCreationForm as AuthUserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserChangeForm(AuthUserChangeForm):
    class Meta(AuthUserChangeForm.Meta):
        model = User


class UserCreationForm(AuthUserCreationForm):
    class Meta(AuthUserCreationForm.Meta):
        model = User


class UserInline(admin.TabularInline):
    fields = ['username', 'email']
    model = User
    extra = 0
    # max_num = 4


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'gender', 'birthday', 'email', 'phone', 'address', 'occupation')}),
        (_('Data'), {'fields': ('duo', 'clan', 'tribe')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'roles', 'checkpoints', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Meta'), {'fields': ('notes',)}),
    )
    list_display = ('username', 'name', 'email', 'phone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'roles', 'checkpoints', 'groups')
    filter_horizontal = ('roles', 'checkpoints', 'groups', 'user_permissions')
    form = UserChangeForm
    add_form = UserCreationForm
