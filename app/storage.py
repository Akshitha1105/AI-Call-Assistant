import os
import uuid
from typing import Tuple

import boto3
from botocore.client import Config

from app.settings import settings


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def storage_save_bytes(content: bytes, ext: str, subdir: str = "") -> Tuple[str, str]:
    filename = f"{uuid.uuid4().hex}{ext}"
    if settings.storage_backend == "local":
        base_dir = settings.storage_local_dir
        if subdir:
            base_dir = os.path.join(base_dir, subdir)
        ensure_dir(base_dir)
        dst = os.path.join(base_dir, filename)
        with open(dst, "wb") as f:
            f.write(content)
        return dst, filename
    elif settings.storage_backend == "s3":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_default_region,
            config=Config(signature_version="s3v4"),
        )
        key = f"{subdir}/{filename}" if subdir else filename
        s3.put_object(Bucket=settings.s3_bucket_name, Key=key, Body=content)
        return key, filename
    else:
        raise ValueError("Unsupported storage backend")


def storage_path(subpath: str) -> str:
    if settings.storage_backend == "local":
        return os.path.join(settings.storage_local_dir, subpath)
    return subpath

