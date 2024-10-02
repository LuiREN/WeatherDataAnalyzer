import pandas as pd
from datetime import datetime
import os
from typing import Dict, Optional, Tuple

def get_data_by_date(date: datetime, input_file: str) -> Optional[Dict[str, str]]:
    """
    Возвращает данные для указанной даты из файла.
    
    Args:
        date (datetime): Дата для поиска данных.
        input_file (str): Путь к файлу с данными.
    
    Returns:
        Optional[Dict[str, str]]: Словарь с данными для указанной даты или None, если данные не найдены.
    """
    df: pd.DataFrame = pd.read_csv(input_file, parse_dates=['Дата'])
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
        if self.index >= len(self.df):
            raise StopIteration
        row: pd.Series = self.df.iloc[self.index]
        self.index += 1
        return (row['Дата'], row.to_dict())

if __name__ == "__main__":
    input_file: str = input("Введите путь к CSV файлу: ")
    date_str: str = input("Введите дату для поиска (YYYY-MM-DD): ")
    date: datetime = datetime.strptime(date_str, "%Y-%m-%d")
    data: Optional[Dict[str, str]] = get_data_by_date(date, input_file)
    print(f"Данные на {date_str}:")
    print(data if data else "Данные не найдены")