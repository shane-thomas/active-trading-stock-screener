import aiohttp
import asyncio
from io import BytesIO
from zipfile import ZipFile
from datetime import datetime, timedelta
import constants as c
import os

async def extract(response, counter):
    cwd = os.getcwd()
    resp = await response.read()
    z = ZipFile(BytesIO(resp))
    filename = z.namelist()[0]
    z.extract(filename, f"{cwd}/DATA/90 DAYS")
    path = f"{cwd}/DATA/90 DAYS/{filename}"
    await rename(path)
    if counter < 5:
        z.extract(filename, f"{cwd}/DATA/5 DAYS")
        path = f"{cwd}/DATA/5 DAYS/{filename}"
        await rename(path)
    if counter < 30:
        z.extract(filename, f"{cwd}/DATA/30 DAYS")
        path = f"{cwd}/DATA/30 DAYS/{filename}"
        await rename(path)
    
async def rename(path):
    date_str = path.split('cm')[1][:-8]
    date_obj = datetime.strptime(date_str, "%d%b%Y")
    new_path = path.split('cm')[0] + date_obj.strftime(c.DATE_FORMAT) + "-NSE-EQ.csv"
    try:
        os.rename(path, new_path)
    except FileExistsError:
        exit


async def get_files():
    cwd = os.getcwd()
    current_date = datetime.today()-timedelta(days=1)
    tasks = []
    files_list = []
    counter = 0
    async with aiohttp.ClientSession() as session:
        tasks = get_task(session)
        responses = await(asyncio.gather(*tasks))
        for response in responses:
            if counter == 90:
                break
            if response.status==200:
                await extract(response, counter)                
                counter+=1
            

def get_task(session):
    tasks = []
    counter = 0
    current_date = datetime.today() - timedelta(days=1)
    while counter < 200:
        if current_date.weekday() < 5:
            url = f"{c.URL}{current_date.strftime('%Y')}/{current_date.strftime('%b').upper()}"
            date_string = current_date.strftime("%d%b%Y").upper()
            filename = f"cm{date_string}bhav.csv.zip"
            url = f"{url}/{filename}"
            tasks.append(session.get(url, ssl = False))
        current_date = current_date - timedelta(days=1)
        counter=counter+1

    return tasks

if __name__ == "__main__":
    asyncio.run(get_files())