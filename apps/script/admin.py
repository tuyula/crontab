from django.contrib import admin

# Register your models here.
from apps.loon_model_base_admin import LoonModelBaseAdmin
from apps.script.models import CustomScript


class ScriptAdmin(LoonModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'description', 'type') + LoonModelBaseAdmin.list_display


admin.site.register(CustomScript, ScriptAdmin)
