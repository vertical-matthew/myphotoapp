from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

# Import your existing views
from photos.views import main_page, project_list, project_detail, repair_detail

urlpatterns = [
    path('admin/', admin.site.urls),

    # Original main page route
    path('', main_page, name='main_page'),

    # New routes for Projects and Repairs
    path('projects/', project_list, name='project_list'),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),
    path('projects/<int:project_id>/repairs/<int:repair_id>/', repair_detail, name='repair_detail'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
