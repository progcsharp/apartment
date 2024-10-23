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


def upload_file(files):
    urls = []
    for file in files:
        name = generate_unique_filename(file.filename)
        if check_for_duplicates(str(name)):
            print(s3_client.put_object(Body=file.file, Bucket="stayflex", Key=name))
            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': BUCKET,
                    'Key': name
                }
            )
            urls.append(url)
    return urls


def delete_file(files):
    for file in files:
        s3_client.delete_object(Bucket=BUCKET, Key=file)
