import os
import xlsxwriter
from datetime import date, datetime, timedelta
import constants as c
from data_operations import reload

def read_date():
    with open('log.txt', 'r') as file:
        date_str = file.read().strip()
        return datetime.strptime(date_str, c.DATE_FORMAT).date()

def write_data(date):
    with open('log.txt', 'w') as file:
        file.write(date.strftime(c.DATE_FORMAT))

def main():
    current_date = date.today() 
    if os.path.exists('log.txt'):
        recorded_date = read_date()
        if current_date - recorded_date > timedelta(days=5):
            # Incase the date is past 5 days
            write_data(current_date)
            reload()
        else:
            # Incase the date is within 5 days
            print(f"File date is within 5 days: {recorded_date.strftime(c.DATE_FORMAT)}")
    else:
        # If no log file existed
        write_data(current_date)
        reload()
    result = c.RESULTS_FILE
    workbook = xlsxwriter.Workbook(result)
    workbook.add_worksheet('5 DAYS')
    workbook.add_worksheet('30 DAYS')
    workbook.add_worksheet('90 DAYS')
    workbook.close()




if __name__ == "__main__":
    main()
