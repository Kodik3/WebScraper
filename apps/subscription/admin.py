from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class BandAdmin(admin.ModelAdmin):
    readonly_fields = ('level',)