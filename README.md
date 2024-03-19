### usage
- config.toml file path
- set environment
```
if __name__ == "__main__":
    handler = AWSSecretsHandler(environment="dev", config_path="config.test.toml")
    handler.get(secret_name=SECRET_NAME)
    handler.save_to_environment("RDS_HOST")
    logger.debug(os.getenv("AWS__RDS_HOST"))  # None
    handler.save_to_environment("RDS_HOST", env_var_name="TEST")
    logger.debug(os.getenv("AWS__TEST"))


```
### aws configuration
- ```/root/.aws```
- ```C:\Users\[USERNAME]\.aws```

#### config file
```config
[default]
region = ap-northeast-2

[profile dev-general]
source_profile=default
region = ap-northeast-2
```
#### credential file
```credential
[default]
aws_access_key_id = XXXXXXX
aws_secret_access_key = XXXXXXX


[dev-general]
aws_access_key_id = XXXXXXX
aws_secret_access_key = XXXXXXX
role = AWS_DEV_ROLE_ARN # example


[dev-mlops]
aws_access_key_id = XXXXXXX
aws_secret_access_key = XXXXXXX
role = AWS_DEV_MLOPS_ROLE_ARN # example


```