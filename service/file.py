import hashlib
import uuid

from service.s3_client import s3_client, BUCKET


def generate_unique_filename(filename: str) -> str:
    hash_value = int(hashlib.md5(filename.encode()).hexdigest(), 16)
    unique_filename = f"{hash_value}_{uuid.uuid4().hex[:8]}.jpg"
    return unique_filename


def check_for_duplicates(file_hash: str) -> bool:
    # Список уже существующих хешей
    existing_hashes = set()

    # Получаем список всех объектов в бакете
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET, Prefix='test/')

    for page in pages:
        for obj in page.get('Contents', []):
            obj_key = obj['Key'].split('/')[-1]
            obj_hash = int(hashlib.md5(obj_key.encode()).hexdigest(), 16)
            existing_hashes.add(str(obj_hash))

    return file_hash not in existing_hashes


def upload_file(files, bucket_name, link):
    urls = []
    for file in files:
        name = generate_unique_filename(file.filename)
        if check_for_duplicates(str(name)):
            print(s3_client.put_object(Body=file.file, Bucket=bucket_name, Key=name))
            url = f"{link}{name}"
            urls.append(url)
    return urls


def delete_file(files):
    for file in files:
        name = file.replace("https://b95b2fa5-a84e-458c-9dcd-0f6142437182.selstorage.ru/", '')
        s3_client.delete_object(Bucket=BUCKET, Key=name)
