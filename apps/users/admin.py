from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Profile, Address, User

from django.utils.translation import gettext_lazy as _
# from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): ...
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete=False
#     verbose_plural_name="User Profile"
#     fk_name = 'user'  

class AddressInline(admin.StackedInline):
    model = Address
    can_delete=True
    verbose_plural_name="User Address"
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    list_display_links = ['username']
    search_fields = ('username',)
    ordering = ('username',)
    # inlines = (ProfileInline, AddressInline)
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

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         return self.model.objects.archive()
    #     return super().get_queryset(request)

admin.site.register(User, CustomUserAdmin)


