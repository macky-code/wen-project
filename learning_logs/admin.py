from django.contrib import admin
from .models import Topic, Entry, Habit, HabitCheckin, HabitLog




@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'date_added')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'date_added')


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')


@admin.register(HabitCheckin)
class HabitCheckinAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date')
    list_filter = ('date',)
    search_fields = ('habit__name',)

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'completed', 'owner')
    list_filter = ('completed', 'date')
    search_fields = ('habit__name',)
