### usage
- config.toml file path
- set environment
```
if __name__ == "__main__":
    secret = AWSSecrets(environment="dev", config_path="config.toml")
    secret.set(secret_name="dev/secret-name")
    secret.get()

    logger.debug(secret.keys().list)
    logger.debug(secret.get__("RDS_HOST"))


    secret = AWSSecrets(environment="dev", config_path="config.toml")
    secret.get(secret_name="dev/secret-name")
    logger.debug(secret.get__("RDS_HOST"))


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