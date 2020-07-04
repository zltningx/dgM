from django.contrib import admin
from apps.backend.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'full_name', 'user_id',
        'is_superuser', 'last_login',
    )
    search_fields = ('username', 'full_name', 'email')

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data['password']
        if change:
            user_obj = User.objects.get(id=obj.id)
            if password != user_obj.password:
                obj.set_password(password)
                obj.save()
            else:
                obj.save()
        else:
            obj.set_password(password)
            obj.save()


admin.site.register(User, UserAdmin)
