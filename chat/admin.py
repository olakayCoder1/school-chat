from django.contrib import admin

from .models import Messages, Threads , CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomMessagesAdmin(admin.ModelAdmin):
    list_display = ['thread_name','content', 'created_at']
admin.site.register(Threads)
admin.site.register(Messages, CustomMessagesAdmin)
admin.site.register(CustomUser, UserAdmin)
