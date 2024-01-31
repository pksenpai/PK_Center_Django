from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Profile, Address, User

from django.utils.translation import gettext_lazy as _


admin.site.register(Profile)
admin.site.register(Address)

class UserProfileInline(admin.TabularInline):
    model = Profile
    readonly_fields = ('id',)
    extra = 1

class UserAddressInline(admin.TabularInline):
    model = Address
    readonly_fields = ('id',)
    extra = 1

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    list_display_links = ['username']
    search_fields = ('username',)
    ordering = ('username',)
    list_display = ('username', 'email', 'is_active', 'is_seller', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_seller', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','is_seller')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_seller')}
         ),
    )
    inlines = [
        UserProfileInline,
        UserAddressInline,
    ]
    
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         return self.model.objects.archive()
    #     return super().get_queryset(request)


