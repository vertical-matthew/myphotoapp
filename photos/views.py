from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Repair, Photo

"""
This file defines the views (controller logic) for:

1. main_page       - The main landing page that now includes a real form for 
                     uploading images to a chosen project + repair.
2. project_list    - Lists all projects.
3. project_detail  - Shows detail for a single project & its repairs.
4. repair_detail   - Shows detail for a single repair, including photo uploads.
"""

def main_page(request):
    """
    Original main page view. Now enhanced to:
      - Display dropdowns for Project and Repair.
      - Let the user select which 'category' each photo belongs to (Survey, Demo, etc.).
      - Upload actual images to the server, storing them in the media/photos/ folder.

    The user can still see the placeholder 4-photo layout if they wish, and
    the 'repairIdBtn' + modal remain for consistency.
    """
    # We'll pass all Projects and all Repairs to the template
    # so the user can pick which ones they want.
    projects = Project.objects.all().order_by('name')
    repairs = Repair.objects.all().order_by('repair_id')

    # Handle file uploads if this is a POST request:
    if request.method == 'POST' and 'upload_photo' in request.POST:
        # Retrieve the user selections from the form
        project_id = request.POST.get('project_id')
        repair_num = request.POST.get('repair_id')
        category = request.POST.get('category')
        image_file = request.FILES.get('image')

        # If the user provided all necessary info, attempt to create a new Photo
        if project_id and repair_num and category and image_file:
            # Try to find the matching Project
            project_obj = Project.objects.filter(id=project_id).first()
            if project_obj:
                # Find the matching Repair by project + repair_id
                repair_obj = Repair.objects.filter(project=project_obj, repair_id=repair_num).first()
                if repair_obj:
                    # Create the new Photo entry and store the file
                    Photo.objects.create(
                        repair=repair_obj,
                        category=category,
                        image=image_file
                    )
                    # After saving, you can redirect or simply show a success message
                    return redirect('main_page')  # Refresh the main page

    # Render the main page template
    return render(request, 'photos/main.html', {
        'projects': projects,
        'repairs': repairs
    })


def project_list(request):
    """
    View to list all projects with basic styling.
    """
    projects = Project.objects.all().order_by('name')
    return render(request, 'photos/project_list.html', {
        'projects': projects
    })


def project_detail(request, project_id):
    """
    Shows the details of a single project, including all its repairs.
    """
    project = get_object_or_404(Project, id=project_id)
    repairs = project.repairs.all().order_by('repair_id')
    return render(request, 'photos/project_detail.html', {
        'project': project,
        'repairs': repairs
    })


def repair_detail(request, project_id, repair_id):
    """
    Shows one repair's details (coordinates, label, area) and
    lists all photos associated with it.

    Allows file uploads. If the user submits a file, we save it
    to the Photo model and redirect back to this detail view.
    """
    project = get_object_or_404(Project, id=project_id)
    repair = get_object_or_404(Repair, project=project, repair_id=repair_id)
    photos = repair.photos.all()

    if request.method == 'POST':
        if 'upload_photo' in request.POST:
            category = request.POST.get('category')
            image_file = request.FILES.get('image')

            if category and image_file:
                Photo.objects.create(
                    repair=repair,
                    category=category,
                    image=image_file
                )
                return redirect('repair_detail', project_id=project.id, repair_id=repair.repair_id)

    return render(request, 'photos/repair_detail.html', {
        'project': project,
        'repair': repair,
        'photos': photos
    })
