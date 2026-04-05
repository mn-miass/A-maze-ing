class FileValidator():
    """Hundle the file with different permissions"""
    VALIDATE_PERMISSION = {"r", "w", "a", "r+", "w+"}
    def __init__(self, path, permissions="r") -> None:
        self.path = path
        self.permissions = permissions
        self.errors = []
        self.data = []
        self.is_validate = True
        self._validate()

    def _validate(self):
        self._validate_permission()
        self._open_check()
        if len(self.errors):
            self.is_validate = False

   
    def _validate_permission(self):
        """The first step is checking the valid permission to read the file"""
        if self.permissions not in FileValidator.VALIDATE_PERMISSION:
            self.errors.append(f"InvalidPermission: {self.permissions}") #tested

   
    def _open_check(self):
            """The second step is opening the file if the permission is read store all the data"""
            try:
                with open(self.path, self.permissions) as file:
                    if self.permissions in {"r", "r+"}:
                        self.data = file.readlines()
            except IsADirectoryError:
                self.errors.append(f"IsADirectoryError = {self.path}") #tested
            except PermissionError:
                self.errors.append(f"PermissionError = {self.path}") #tested
            except UnicodeDecodeError:
                self.errors.append(f"UnicodeDecodeError = {self.path}") #tested
            except FileNotFoundError:
                self.errors.append(f"FileNotFoundError = {self.path}") #tested
