from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional


class AWSSecret(BaseModel):
    """AWS Secret Meta, No secret value"""

    ARN: str
    Name: str
    LastChangedDate: Optional[datetime]
    LastAccessedDate: Optional[datetime]
    Tags: Optional[List]
    SecretVersionsToStages: Optional[Dict]
    CreatedDate: Optional[datetime]


class AWSSecretValue(BaseModel):
    """AWS Secret Meta with Secret Value"""

    SecretString: str
    SecretBinary: bytes
    VersionId: str
    VersionStages: List[str]


class AWSSecretKeys(BaseModel):
    """AWS Secret Keys"""

    number: int
    list: List[str]
