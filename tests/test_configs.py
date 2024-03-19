import os
from secret_guardian import AWSSecretsHandler

os.environ["LOCAL_TEST"] = "1"


def test_handler_config_no_aws_profile():

    # 2nd way initialize
    pass
