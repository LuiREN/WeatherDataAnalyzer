import pandas as pd
from datetime import datetime
import os
from typing import Dict, Optional, Tuple, Iterator

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
    input_file: str = input("Введите путь к CSV файлу: ")
    
    # Пример использования get_data_by_date
    date_str: str = input("Введите дату для поиска (YYYY-MM-DD): ")
    date: datetime = datetime.strptime(date_str, "%Y-%m-%d")
    data: Optional[Dict[str, str]] = get_data_by_date(date, input_file)
    print(f"Данные на {date_str}:")
    print(data if data else "Данные не найдены")
    
    # Пример использования WeatherIterator и функции next
    print("\nПример работы итератора:")
    iterator = WeatherIterator(input_file)
    for _ in range(5):  # Выводим первые 5 записей
        try:
            date, data = next(iterator)
            print(f"Дата: {date}, Данные: {data}")
        except StopIteration:
            print("Достигнут конец данных")
            break