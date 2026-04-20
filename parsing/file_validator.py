class FileValidator:
    """
    Validates and opens a file with a given permission.

    Attributes:
        path (str): Path to the file.
        permissions (str): File open mode (e.g., 'r', 'w', 'a', 'r+', 'w+').
        errors (list[str]): List of errors encountered during validation.
        data (list[str]): Lines read from the file (only when permission
            is 'r' or 'r+').
        is_validate (bool): False if any error was encountered, True otherwise.
    """

    VALIDATE_PERMISSION: set[str] = {"r", "w", "a"}

    def __init__(self, path: str, permissions: str = "r") -> None:
        self.path: str = path
        self.permissions: str = permissions
        self.error: list[str] = []
        self.data: list[str] = []
        self.is_validate: bool = True
        self._validate()

    def _validate(self) -> None:
        """Runs all validation steps in order."""
        self._validate_permission()
        if not self.is_validate:
            return
        self._open_check()

    def _validate_permission(self) -> None:
        """Checks that the given permission is one of the allowed modes."""
        if self.permissions not in FileValidator.VALIDATE_PERMISSION:
            self.error.append(f"InvalidPermission: {self.permissions}")
            self.is_validate = False

    def _open_check(self) -> None:
        """Opens the file and reads its content
            if permission is 'r' or 'r+'."""
        try:
            with open(self.path, self.permissions) as file:
                if self.permissions in {"r"}:
                    self.data = file.readlines()
        except NotADirectoryError:
            self.error.append(f"NotADirectoryError: {self.path}")
            self.is_validate = False
        except IsADirectoryError:
            self.error.append(f"IsADirectoryError: {self.path}")
            self.is_validate = False
        except PermissionError:
            self.error.append(f"PermissionError: {self.path}")
            self.is_validate = False
        except UnicodeDecodeError:
            self.error.append(f"UnicodeDecodeError: {self.path}")
            self.is_validate = False
        except FileNotFoundError:
            self.error.append(f"FileNotFoundError: {self.path}")
            self.is_validate = False
        except OSError:
            self.error.append(f"OSError: {self.path}")
            self.is_validate = False
