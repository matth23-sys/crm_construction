from apps.projects.models.entities import Project


class WorkforceProject(Project):
    """
    Proxy model para que workforce tenga permisos propios
    sin crear una nueva tabla de negocio.
    """

    class Meta:
        proxy = True
        app_label = "workforce"
        verbose_name = "Workforce project"
        verbose_name_plural = "Workforce projects"
        permissions = (
            ("view_assigned_projects", "Can view assigned projects in workforce"),
            ("submit_field_note", "Can submit field notes in workforce"),
            ("update_project_milestone", "Can update allowed project milestones in workforce"),
        )