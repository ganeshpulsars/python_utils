class TableNotFoundError(Exception):
    """Custom exception for table not found condition in SQLite db"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
