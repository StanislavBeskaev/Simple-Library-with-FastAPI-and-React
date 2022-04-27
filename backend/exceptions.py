class LibraryValidationException(Exception):
    def __init__(self, errors: dict) -> None:
        self.errors = errors

    def __str__(self):
        return str(self.errors)
