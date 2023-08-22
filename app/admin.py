from django.contrib import admin
from .models import Motes, Data, StatsHour, ExtendUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class MotesData(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'section', 'location']


class DataData(admin.ModelAdmin):
    list_display = ['id', 'mote', 'last_collection', 'total', 'collect_date']


class StatsHourStatsHour(admin.ModelAdmin):
    list_display = ['id', 'mote', 'mean', 'median',
                    'std', 'cv', 'max', 'min', 'fq', 'tq']


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            'Aditional Info',
            {
                'fields': (
                    'profile_photo',
                    'description',
                ),
            },
        ),
    )


admin.site.register(ExtendUser, CustomUserAdmin)
admin.site.register(Motes, MotesData)
admin.site.register(Data, DataData)
admin.site.register(StatsHour, StatsHourStatsHour)
