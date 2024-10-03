import pandas as pd
from datetime import datetime, date
import os
from typing import Dict, Optional, Tuple, List

def get_file_list(folder: str) -> List[str]:
    """
    Возвращает список CSV файлов в указанной папке.
    """
    return [f for f in os.listdir(folder) if f.endswith('.csv')]

def select_file(files: List[str]) -> str:
    """
    Позволяет пользователю выбрать файл из списка.
    """
    print("Доступные файлы:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    while True:
        try:
            choice = int(input("Выберите номер файла: ")) - 1
            if 0 <= choice < len(files):
                return files[choice]
            print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def get_data_by_date_original(date: date, file_path: str) -> Optional[Dict[str, str]]:
    df: pd.DataFrame = pd.read_csv(file_path, parse_dates=['Дата'])
    df['Дата'] = df['Дата'].dt.date
    row: pd.DataFrame = df[df['Дата'] == date]
    if row.empty:
        return None
    return row.iloc[0].to_dict()

def get_data_by_date_split(date: date, x_file: str, y_file: str) -> Optional[Dict[str, str]]:
    x_df: pd.DataFrame = pd.read_csv(x_file, parse_dates=['Date'])
    x_df['Date'] = x_df['Date'].dt.date
    y_df: pd.DataFrame = pd.read_csv(y_file)
    
    row_index = x_df.index[x_df['Date'] == date]
    if row_index.empty:
        return None
    
    y_row = y_df.iloc[row_index[0]]
    return {'Дата': date, **y_row.to_dict()}

def get_data_by_date_yearly(date: date, folder: str) -> Optional[Dict[str, str]]:
    year_file = os.path.join(folder, f"{date.year}0101_{date.year}1231.csv")
    if not os.path.exists(year_file):
        print(f"Файл для {date.year} года не найден.")
        return None
    
    df: pd.DataFrame = pd.read_csv(year_file, parse_dates=['Дата'])
    df['Дата'] = df['Дата'].dt.date
    row: pd.DataFrame = df[df['Дата'] == date]
    if row.empty:
        return None
    return row.iloc[0].to_dict()

def get_data_by_date_weekly(date: date, folder: str) -> Optional[Dict[str, str]]:
    files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    for file in files:
        start_date, end_date = file.split('_')
        start_date = datetime.strptime(start_date, "%Y%m%d").date()
        end_date = datetime.strptime(end_date.split('.')[0], "%Y%m%d").date()
        if start_date <= date <= end_date:
            file_path = os.path.join(folder, file)
            df: pd.DataFrame = pd.read_csv(file_path, parse_dates=['Дата'])
            df['Дата'] = df['Дата'].dt.date
            row: pd.DataFrame = df[df['Дата'] == date]
            if not row.empty:
                return row.iloc[0].to_dict()
    
    print(f"Данные для даты {date} не найдены.")
    return None

class WeatherIterator:
    def __init__(self, input_file: str):
        self.df: pd.DataFrame = pd.read_csv(input_file, parse_dates=['Дата'])
        self.df['Дата'] = self.df['Дата'].dt.date
        self.df = self.df.sort_values('Дата')
        self.index: int = 0

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[date, Dict[str, str]]:
        if self.index >= len(self.df):
            raise StopIteration
        row: pd.Series = self.df.iloc[self.index]
        self.index += 1
        return (row['Дата'], row.to_dict())

def get_file_list(folder: str) -> List[str]:
    return [f for f in os.listdir(folder) if f.endswith('.csv')]

def select_file(files: List[str]) -> str:
    print("Доступные файлы:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    while True:
        try:
            choice = int(input("Выберите номер файла: ")) - 1
            if 0 <= choice < len(files):
                return files[choice]
            print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")