"""
CONTRIBUTORS: dev-Lesser
Module
    secret_guardian
Description
    This is the main
    module for secret-guardian
"""

__version__ = "0.1.0"
__all__ = [
    "AWSSecretsHandler",
    "EnvironmentConfig",
    "ProviderConfig",
    "AWSConfig",
    "GCPConfig",
    "AzureConfig",
    "create_template",
    "AWSSecret",
    "AWSSecretKeys",
]

from .handlers import AWSSecretsHandler
from .template import (
    create_template,
    EnvironmentConfig,
    ProviderConfig,
    AWSConfig,
    GCPConfig,
    AzureConfig,
)
from .models import AWSSecret, AWSSecretKeys
