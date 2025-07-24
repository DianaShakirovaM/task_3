from django.contrib import admin

from .models import Action, Follow, Task


admin.site.register(Action)
admin.site.register(Follow)
admin.site.register(Task)
