class AwsBucketCreationError(Exception):
    """
    Exception class for handling bucket creation error in AWS S3
    """

    def __init__(self, bucket_name: str) -> None:
        self.message = f"{bucket_name} was not created successfully"
        super().__init__(self.message)
