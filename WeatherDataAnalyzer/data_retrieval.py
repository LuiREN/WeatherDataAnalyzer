import pandas as pd
from datetime import datetime
import os
from typing import Dict, Optional, Tuple, Iterator, List

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

def get_data_by_date_original(date: datetime, file_path: str) -> Optional[Dict[str, str]]:
    """
    Возвращает данные для указанной даты из оригинального CSV файла.
    """
    df: pd.DataFrame = pd.read_csv(file_path, parse_dates=['Дата'])
    row: pd.DataFrame = df[df['Дата'] == pd.Timestamp(date)]
    if row.empty:
        return None
    return row.iloc[0].to_dict()

def get_data_by_date_split(date: datetime, x_file: str, y_file: str) -> Optional[Dict[str, str]]:
    """
    Возвращает данные для указанной даты из разделенных X.csv и Y.csv файлов.
    """
    x_df: pd.DataFrame = pd.read_csv(x_file, parse_dates=['Date'])
    y_df: pd.DataFrame = pd.read_csv(y_file)
    
    row_index = x_df.index[x_df['Date'] == pd.Timestamp(date)]
    if row_index.empty:
        return None
    
    y_row = y_df.iloc[row_index[0]]
    return {'Дата': date.strftime('%Y-%m-%d'), **y_row.to_dict()}

def get_data_by_date_yearly(date: datetime, file_path: str) -> Optional[Dict[str, str]]:
    """
    Возвращает данные для указанной даты из годовых файлов.
    """
    df: pd.DataFrame = pd.read_csv(file_path, parse_dates=['Дата'])
    row: pd.DataFrame = df[df['Дата'] == pd.Timestamp(date)]
    if row.empty:
        return None
    return row.iloc[0].to_dict()

def get_data_by_date_weekly(date: datetime, file_path: str) -> Optional[Dict[str, str]]:
    """
    Возвращает данные для указанной даты из недельных файлов.
    """
    df: pd.DataFrame = pd.read_csv(file_path, parse_dates=['Дата'])
    row: pd.DataFrame = df[df['Дата'] == pd.Timestamp(date)]
    if row.empty:
        return None
    return row.iloc[0].to_dict()

class WeatherIterator:
    def __init__(self, input_file: str):
        self.df: pd.DataFrame = pd.read_csv(input_file, parse_dates=['Дата'])
        self.df = self.df.sort_values('Дата')
        self.index: int = 0

    def __iter__(self) -> 'WeatherIterator':
        return self

    def __next__(self) -> Tuple[datetime, Dict[str, str]]:
        while self.index < len(self.df):
            row: pd.Series = self.df.iloc[self.index]
            self.index += 1
            if pd.notna(row['Дата']):  # Проверяем, что дата не NaT
                return (row['Дата'], row.to_dict())
        raise StopIteration

def next(iterator: Iterator) -> Tuple[datetime, Dict[str, str]]:
    """
    Возвращает данные для следующей валидной даты.
    
    Args:
        iterator (Iterator): Итератор WeatherIterator.
    
    Returns:
        Tuple[datetime, Dict[str, str]]: Кортеж с датой и данными.
    """
    return next(iterator)

if __name__ == "__main__":
    print("Выберите тип входных данных:")
    print("1. Оригинальный CSV")
    print("2. X.csv и Y.csv")
    print("3. Годовые файлы")
    print("4. Недельные файлы")
    
    choice = input("Ваш выбор: ")
    date_str = input("Введите дату (YYYY-MM-DD): ")
    date = datetime.strptime(date_str, "%Y-%m-%d")
    
    base_folder = "dataset"  # Базовая папка для всех данных
    
    if choice == '1':
        data = get_data_by_date_original(date, base_folder)
    elif choice == '2':
        x_folder = os.path.join(base_folder, "split_csv")
        y_folder = os.path.join(base_folder, "split_csv")
        data = get_data_by_date_split(date, x_folder, y_folder)
    elif choice == '3':
        yearly_folder = os.path.join(base_folder, "yearly_data")
        data = get_data_by_date_yearly(date, yearly_folder)
    elif choice == '4':
        weekly_folder = os.path.join(base_folder, "weekly_data")
        data = get_data_by_date_weekly(date, weekly_folder)
    else:
        print("Неверный выбор")
        exit()
    
    print(f"Данные на {date_str}:")
    print(data if data else "Данные не найдены")