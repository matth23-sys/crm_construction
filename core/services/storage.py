from django.core.files.storage import FileSystemStorage

from core.utils.files import build_dated_upload_path


class OverwriteFileSystemStorage(FileSystemStorage):
    """
    Permite reemplazar archivos si se reusa exactamente el mismo nombre.
    """

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name


def upload_to_factory(base_dir):
    def _upload_to(instance, filename):
        return build_dated_upload_path(filename=filename, base_dir=base_dir)

    return _upload_to