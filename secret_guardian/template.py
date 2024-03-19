from pydantic import BaseModel
import toml
from loguru import logger
import json


class AWSConfig(BaseModel):
    AWS_PROFILE: str
    AWS_ACCOUNT_ID: str


class GCPConfig(BaseModel):
    GCP_PROFILE: str
    GCP_ACCOUNT_ID: str


class AzureConfig(BaseModel):
    AZURE_PROFILE: str
    AZURE_ACCOUNT_ID: str


class ProviderConfig(BaseModel):
    aws: AWSConfig
    gcp: GCPConfig
    azure: AzureConfig
    LOCAL_TEST: bool


class EnvironmentConfig(BaseModel):
    dev: ProviderConfig
    stage: ProviderConfig


def create_template(output_file_name="config.toml"):

    dev_provider_config = ProviderConfig(
        aws=AWSConfig(AWS_ACCOUNT_ID="", AWS_PROFILE="default"),
        gcp=GCPConfig(GCP_PROFILE="dev", GCP_ACCOUNT_ID="develop"),
        azure=AzureConfig(AZURE_PROFILE="dev", AZURE_ACCOUNT_ID="develop"),
        LOCAL_TEST=True,
    )
    stage_provider_config = ProviderConfig(
        aws=AWSConfig(AWS_ACCOUNT_ID="", AWS_PROFILE="default"),
        gcp=GCPConfig(GCP_PROFILE="stage", GCP_ACCOUNT_ID="staging"),
        azure=AzureConfig(AZURE_PROFILE="stage", AZURE_ACCOUNT_ID="staging"),
        LOCAL_TEST=False,
    )
    e = EnvironmentConfig(dev=dev_provider_config, stage=stage_provider_config)
    logger.debug(e.model_dump_json())

    with open(output_file_name, "w") as toml_file:
        toml.dump(json.loads(e.model_dump_json()), toml_file)


if __name__ == "__main__":
    config_file_name = "config.test.toml"
    create_template(output_file_name=config_file_name)
    # test
    with open(config_file_name, "r", encoding="utf-8") as f:
        config = toml.load(f)
        logger.debug(config)
