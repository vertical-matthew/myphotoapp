import openpyxl  # Or 'import pandas' if you prefer that library
from django.core.management.base import BaseCommand, CommandError
from photos.models import Project, Repair

class Command(BaseCommand):
    help = "Import project and repair data from an Excel file."

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the Excel file")

    def handle(self, *args, **options):
        file_path = options['file_path']

        # Load the specified Excel workbook
        try:
            workbook = openpyxl.load_workbook(file_path)
        except FileNotFoundError:
            raise CommandError(f"File not found: {file_path}")

        # Assuming we use the first sheet
        sheet = workbook.active

        # Example: Expect columns:
        # A: Project Name  B: Repair ID  C: Repair Label  D: Area (sq ft)
        # Adjust as needed for your actual spreadsheet layout
        for row in sheet.iter_rows(min_row=2, values_only=True):
            project_name = row[0]
            repair_id = row[1]
            repair_label = row[2]
            area_val = row[3]

            # Create or get the Project
            project_obj, created = Project.objects.get_or_create(name=project_name)

            # Create a new Repair for that Project
            Repair.objects.create(
                project=project_obj,
                repair_id=repair_id,
                label=repair_label,
                area_sq_ft=area_val,
            )

        self.stdout.write(self.style.SUCCESS('Data import complete!'))
