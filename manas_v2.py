import os
from tqdm import tqdm
import xlsxwriter
from datetime import date, datetime, timedelta
import constants as c
from data_operations import reload
from watchlist_operations import calculate_roc, calculate_roc_subset, get_symbols_subset


def read_date():
    with open('log.txt', 'r') as file:
        data = {}
        for line in file:
            parts = line.strip().split(': ')
            key = parts[0]
            date_str = parts[1]
            data[key] = datetime.strptime(date_str, c.DATE_FORMAT).date()
        return data


def write_data(date, recorded_date):
    if (not recorded_date):
        with open('log.txt', 'w') as file:
            file.write(f"5 DAYS: {date.strftime(c.DATE_FORMAT)}\n")
            file.write(f"30 DAYS: {date.strftime(c.DATE_FORMAT)}\n")
            file.write(f"90 DAYS: {date.strftime(c.DATE_FORMAT)}\n")
    else:
        with open('log.txt', 'w') as file:
            file.write(f"5 DAYS: {recorded_date["5 DAYS"]}\n")
            file.write(f"30 DAYS: {recorded_date["30 DAYS"]}\n")
            file.write(f"90 DAYS: {recorded_date["90 DAYS"]}\n")


def main():
    os.system('cls')
    cwd = os.getcwd()
    roc_file = c.ROC_FILE
    diff = {}

    roc_path = os.path.join(cwd, roc_file)
    log_file = os.path.join(cwd, 'log.txt')
    results_path = os.path.join(cwd, c.RESULTS_FILE)
    # current_date = date.today()
    current_date = date(2024, 5, 30)
    if not os.path.isfile(log_file):
        write_data(current_date, diff)

    reload()

    recorded_date = read_date()

    for key, value in recorded_date.items():
        diff[key] = (current_date - value).days

    if diff["5 DAYS"] > 5:
        recorded_date["5 DAYS"] = current_date

    if diff["30 DAYS"] > 15:
        recorded_date["30 DAYS"] = current_date

    if diff["90 DAYS"] > 15:
        recorded_date["90 DAYS"] = current_date

    write_data(current_date, recorded_date)

    if not os.path.isfile(roc_path):
        workbook = xlsxwriter.Workbook(roc_file)
        workbook.add_worksheet('5 DAYS')
        workbook.add_worksheet('30 DAYS')
        workbook.add_worksheet('90 DAYS')
        workbook.close()

    if not os.path.isfile(results_path):
        workbook = xlsxwriter.Workbook(c.RESULTS_FILE)
        workbook.add_worksheet('5 DAYS')
        workbook.add_worksheet('30 DAYS')
        workbook.add_worksheet('90 DAYS')
        workbook.close()

    for directory in c.DIRECTORIES:
        calculate_roc(directory)

    for directory in c.DIRECTORIES:
        symbols = get_symbols_subset(directory)
        calculate_roc_subset(symbols, directory)


    os.system('cls')


if __name__ == "__main__":
    main()
