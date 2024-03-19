"""_summary_

1. AWS Secrets Manager implementation
2. Check Auth
    2.1 AWS config, credentials file
    2.2 check access auth to secret manager
"""

import json
import sys
import os
from abc import ABC, abstractmethod
from typing import List, Dict

import toml
import boto3
from loguru import logger
from pydantic import TypeAdapter, SecretStr

from .models import AWSSecret, AWSSecretKeys
from .exceptions import (
    InvalidAccountID,
    NotFoundEnvironment,
    NotFoundAccountID,
    NotFoundProfile,
)
from .utils import process


class Secrets(ABC):
    """base abstract class for secrets management"""

    LOGGER = logger

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set(self, secret_name):
        """set secret value"""

    @abstractmethod
    def get(self):
        """get secret value"""

    @abstractmethod
    def keys(self):
        """get secret keys"""

    @abstractmethod
    def all(self):
        """all secret key list"""

    @abstractmethod
    def get__(self):
        """get secret revealed value"""

    @abstractmethod
    def save_to_environment(self, key, env_var_name=None):
        """save secret value to environment variable"""


# config file read
class AWSSecretsHandler(Secrets):
    """AWS Secrets Manager implementation"""

    PREFIX = "AWS__"
    PROVIDER = "aws"
    ENVIRONMENTS = ["dev", "stage"]

    def __init__(
        self,
        environment: str = "dev",
        config_path: str = "config.toml",
    ):
        assert environment in self.ENVIRONMENTS, NotFoundEnvironment(
            f"Invalid environment '{environment}'\nGet dev, stage"
        )
        self.secret_name = None
        self.obj = None
        self.environment = environment
        self.config_path = config_path

        self.set_environment(self.config_path)
        self.client = boto3.client("secretsmanager")

    def set_environment(self, config_path: str) -> None:
        """set environment variables"""

        with open(config_path, "r", encoding="utf-8") as f:
            config = toml.load(f)

        aws_config = config.get(self.environment)[self.PROVIDER]  # dev

        assert aws_config.get("AWS_ACCOUNT_ID"), NotFoundAccountID(
            f"Account ID not found. Set AWS_ACCOUNT_ID in {self.config_path}"
        )

        assert aws_config.get("AWS_PROFILE"), NotFoundProfile("Profile not found")
        assert self.account_id() == aws_config["AWS_ACCOUNT_ID"], InvalidAccountID(
            message="",
            config_account_id=self.account_id(),
            aws_account_id=aws_config["AWS_ACCOUNT_ID"],
        )
        # set environment variables
        os.environ["AWS_PROFILE"] = aws_config["AWS_PROFILE"]
        os.environ["AWS_ACCOUNT_ID"] = aws_config["AWS_ACCOUNT_ID"]

        if os.getenv("LOCAL_TEST") is None:
            self.LOGGER.warning("Delete local aws profile")
            del os.environ["AWS_PROFILE"]
            del os.environ["AWS_ACCOUNT_ID"]

        return aws_config

    def set(self, secret_name: str) -> None:
        self.secret_name = secret_name

    def get(self, secret_name=None) -> dict:
        if secret_name:
            self.set(secret_name=secret_name)

        response = self.client.get_secret_value(SecretId=self.secret_name)

        results = json.loads(response["SecretString"])
        self.obj = self.hidden_secret(results)
        return self.obj

    def keys(self) -> AWSSecretKeys:
        response = self.get()
        type_adapter = TypeAdapter(AWSSecretKeys)
        response = type_adapter.validate_python(
            {"number": len(response.keys()), "list": sorted(response.keys())}
        )
        return response

    def all(self) -> List[AWSSecret]:
        response = self.client.list_secrets()["SecretList"]
        type_adapter = TypeAdapter(List[AWSSecret])
        response = type_adapter.validate_python(response)
        return response

    def account_id(self) -> str:
        """get aws account id"""
        sts = boto3.client("sts")
        account_id = sts.get_caller_identity()["Account"]
        return account_id

    def profile(self) -> str:
        return os.getenv("AWS_PROFILE")

    @staticmethod
    def hidden_secret(obj: dict = {}) -> Dict:
        return {k: SecretStr(v) for k, v in obj.items()}

    @process()
    def get__(self, key: str) -> str:
        try:
            return self.obj.get(key).get_secret_value()
        finally:
            self.LOGGER.debug(f"{key} : {self.obj.get(key)}")

    def __repr__(self):
        return f"{self.__class__.__name__}(secret_name={self.secret_name})"

    def save_to_environment(self, key, env_var_name=None):
        """save to environment variable with PREFIX default AWS__"""
        if env_var_name:
            os.environ[self.PREFIX + env_var_name] = self.get__(key)
        else:
            os.environ[self.PREFIX + key] = self.get__(key)
        logger.info(f"Save '{key}' to environment variable")


if __name__ == "__main__":
    SECRET_NAME = "pipeline/ds"
    os.environ["LOCAL_TEST"] = "1"

    # 2nd way initialize
    handler = AWSSecretsHandler(environment="dev", config_path="config.test.toml")
    handler.get(secret_name=SECRET_NAME)
    handler.save_to_environment("RDS_HOST")
    logger.debug(os.getenv("AWS__RDS_HOST"))  # None
    handler.save_to_environment("RDS_HOST", env_var_name="TEST")
    logger.debug(os.getenv("AWS__TEST"))

    # if local, set local aws profile value
    # if stage, no need to set local aws profile value
    # cannot access to aws secret manager production environment
