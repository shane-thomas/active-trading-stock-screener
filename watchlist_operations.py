import os
import constants as c
from tqdm import tqdm
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import time
from random import randint


def rand_color():
    alpha = "40"  # 50% transparent
    red = format(randint(128, 255), '02X')
    green = format(randint(128, 255), '02X')
    blue = format(randint(128, 255), '02X')
    return f"{alpha}{red}{green}{blue}"


def roc(directory: str, difference: int):
    sheet_name = directory.split('/')[1]
    roc_dict = {}
    files_list = [file for file in os.listdir(
        directory) if file.endswith(".csv")]

    # Getting current report
    current_report = pd.read_csv(os.path.join(directory, files_list[-1]))
    df = pd.read_csv(os.path.join(directory, files_list[0]))

    os.system('cls')
    for symbol in tqdm(current_report["SYMBOL"], desc=f"Generating report of last {sheet_name}"):
        if symbol in df["SYMBOL"].tolist():
            report_index = current_report.index.get_loc(
                current_report[current_report['SYMBOL'] == symbol].index[0])
            df_index = df.index.get_loc(df[df['SYMBOL'] == symbol].index[0])
            old_close = df.at[df_index, 'CLOSE']
            current_close = current_report.at[report_index, 'CLOSE']

            roc = ((current_close - old_close) / old_close) * 100
            roc_dict[symbol] = roc

    current_report = current_report.query('SERIES == "EQ"')
    df = df.query('SERIES == "EQ"')  # Adjust as needed

    # Adding ROC column mapping to Symbol names
    current_report.insert(len(current_report.columns),
                          'ROC', value=current_report['SYMBOL'].map(roc_dict))

    current_report = current_report.sort_values(by='ROC', ascending=False)

    workbook = load_workbook(c.ROC_FILE)
    worksheet = workbook[sheet_name]
    header_columns = current_report.columns.tolist()

    if worksheet.max_row == 1:
        for col_num, column_title in enumerate(header_columns, 1):
            worksheet.cell(row=1, column=col_num, value=column_title)

    workbook.save(c.ROC_FILE)
    workbook.close()

    with pd.ExcelWriter(c.ROC_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        start_row = writer.sheets[sheet_name].max_row
        current_report.head(50).to_excel(
            writer, sheet_name, index=False, startrow=start_row, header=None)

    argb = rand_color()
    workbook = load_workbook(c.ROC_FILE)
    worksheet = workbook[sheet_name]
    for row in range(start_row+1, start_row + 51):
        for col in range(1, worksheet.max_column + 1):
            worksheet.cell(row=row, column=col).fill = PatternFill(
                start_color=argb, end_color=argb, fill_type='solid')

    workbook.save(c.ROC_FILE)
    workbook.close()


if __name__ == "__main__":
    roc("DATA/5 DAYS", 2)
