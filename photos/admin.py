# myphotoapp/photos/admin.py

from django.contrib import admin
from .models import Project, Repair, Photo

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Fields to show in the project list
    search_fields = ('name',)               # Add a search box on the top of the admin page

@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('repair_id', 'project', 'label', 'area_sq_ft')
    list_filter = ('project', 'label')      # Filters on the right side

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('repair', 'category', 'uploaded_at')
    list_filter = ('category', 'repair__project')
