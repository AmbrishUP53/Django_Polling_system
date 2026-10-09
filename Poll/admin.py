from django.contrib import admin 
from django.contrib.admin import AdminSite
from .models import Candidate , Polls , Vote
# Register your models here.

class CustomModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("Poll/admin_custom.css",)
        }
@admin.register(Polls)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name' , 'description')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'candidate', 'created_at')
    readonly_fields = ('created_at',)
