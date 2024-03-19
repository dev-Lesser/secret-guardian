from abc import abstractmethod
from loguru import logger


class BaseSecretException(Exception):
    """Base Exception for all exceptions"""

    @abstractmethod
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidAccountID(BaseSecretException):
    """invalid account id exception"""

    def __init__(self, message: str, config_account_id, aws_account_id):
        super().__init__(message)
        logger.error(
            f"""Invalid Account ID. Set AWS_ACCOUNT_ID
            {config_account_id} != {aws_account_id}"""
        )


class NotFoundEnvironment(BaseSecretException):
    """Not Found Environment Exception"""

    def __init__(
        self,
        message: str,
    ):
        super().__init__(message)
        logger.error("Environment not found. Set AWS_ENVIRONMENT in {self.config_path}")


class NotFoundAccountID(BaseSecretException):
    """Not Found Account ID Exception"""

    def __init__(self, message: str):
        super().__init__(message)
        logger.error(message)


class NotFoundProfile(BaseSecretException):
    """Not Found Profile Exception"""

    def __init__(self, message: str):
        super().__init__(message)
        logger.error("Profile not found")
