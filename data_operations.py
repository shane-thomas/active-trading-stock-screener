import os
import requests
from datetime import datetime, timedelta
from io import BytesIO
from zipfile import ZipFile
import constants as c


def download() -> None:
    files_list = []
    cwd = os.getcwd()
    current_date = datetime.today() - timedelta(days=1)
    while len(files_list) <= 90:
        if current_date.weekday() < 5:

            os.system('cls')
            print(f"{len(files_list)+1}/90 files downloaded successfully.")

            url = f"{c.URL}{current_date.strftime('%Y')}/{current_date.strftime('%b').upper()}"
            date_string = current_date.strftime("%d%b%Y").upper()
            filename = f"cm{date_string}bhav.csv.zip"
            url = f"{url}/{filename}"

            headers = {'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'}

            response = requests.get(
                url, stream=True, allow_redirects=False, headers=headers)
            if response.status_code == 200:
                z = ZipFile(BytesIO(response.content))
                z.extractall(f"{cwd}/DATA/90 DAYS")
                if len(files_list) < 5:
                    z.extractall(f"{cwd}/DATA/5 DAYS")
                if len(files_list) < 30:
                    z.extractall(f"{cwd}/DATA/30 DAYS")
                files_list.append(filename)
        current_date = current_date - timedelta(days=1)
    print(files_list)


if __name__ == "__main__":
    download()
