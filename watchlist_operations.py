import os
import constants as c
from tqdm import tqdm
import pandas as pd


def watchlist(folder):
    roc_dict = {}
    files_list = [file for file in os.listdir(folder) if file.endswith(".csv")]

    # Getting current report
    current_report = pd.read_csv(os.path.join(folder, files_list[-1]))
    df = pd.read_csv(os.path.join(folder, files_list[0]))

    for symbol in tqdm(current_report["SYMBOL"]):
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

    sheet_name = folder.split('/')[1]
    with pd.ExcelWriter(c.RESULTS_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        # sheet_names = ['90 DAYS', '30 DAYS', '5 DAYS']
        current_report.head(50).to_excel(writer, sheet_name, index=False)


if __name__ == "__main__":
    watchlist("DATA/5 DAYS")
