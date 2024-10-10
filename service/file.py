import aiofiles


async def save_file(file):
    async with aiofiles.open(f"media/{file.filename}", mode='wb') as f:
        content = await file.read()
        await f.write(content)

    return f"media/{file.filename}"


async def save_file_list(files):
    file_list = []
    for file in files:
        async with aiofiles.open(f"media/{file.filename}", mode='wb') as f:
            content = await file.read()
            await f.write(content)
            file_list.append(f"media/{file.filename}")

    return file_list

