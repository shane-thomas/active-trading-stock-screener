import os
from datetime import date, datetime, timedelta
import constants as c

def date_file() -> None:
    current_date = date.today()
    
    def read_date():
        with open('log.txt', 'r') as file:
            date_str = file.read().strip()
            return datetime.strptime(date_str, c.DATE_FORMAT).date()

    def write_data(date):
        with open('log.txt', 'w') as file:
            file.write(date.strftime(c.DATE_FORMAT))

    if os.path.exists('log.txt'):
        recorded_date = read_date()
        if current_date - recorded_date > timedelta(days=5):
            write_data(current_date)
            print(f"File updated with new date: {current_date.strftime(c.DATE_FORMAT)}")
        else:
            print(f"File date is within 5 days: {recorded_date.strftime(c.DATE_FORMAT)}")
    else:
        write_data(current_date)
        print(f"File created with date: {current_date.strftime(c.DATE_FORMAT)}")


if __name__ == "__main__":
    date_file()
