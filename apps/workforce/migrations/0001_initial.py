from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkforceProject",
            fields=[],
            options={
                "verbose_name": "Workforce project",
                "verbose_name_plural": "Workforce projects",
                "proxy": True,
                "indexes": [],
                "constraints": [],
                "permissions": (
                    ("view_assigned_projects", "Can view assigned projects in workforce"),
                    ("submit_field_note", "Can submit field notes in workforce"),
                    ("update_project_milestone", "Can update allowed project milestones in workforce"),
                ),
            },
            bases=("projects.project",),
        ),
    ]