import pandas as pd
from datetime import datetime
import os

def get_data_by_date(date: datetime, input_file: str) -> dict:
    """
    Возвращает данные для указанной даты из файла.
    
    Args:
        date (datetime): Дата для поиска данных.
        input_file (str): Путь к файлу с данными.
    
    Returns:
        dict: Словарь с данными для указанной даты или None, если данные не найдены.
    """
    df = pd.read_csv(input_file, parse_dates=['Дата'])
    row = df[df['Дата'] == pd.Timestamp(date)]
    if row.empty:
        return None
    return row.iloc[0].to_dict()

class WeatherIterator:
    def __init__(self, input_file: str):
        self.df = pd.read_csv(input_file, parse_dates=['Дата'])
        self.df = self.df.sort_values('Дата')
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.df):
            raise StopIteration
        row = self.df.iloc[self.index]
        self.index += 1
        return (row['Дата'], row.to_dict())

if __name__ == "__main__":
    input_file = input("Введите путь к CSV файлу: ")
    
    # Пример использования функции get_data_by_date
    date_str = input("Введите дату для поиска (YYYY-MM-DD): ")
    date = datetime.strptime(date_str, "%Y-%m-%d")
    data = get_data_by_date(date, input_file)
    print(f"Данные на {date_str}:")
    print(data if data else "Данные не найдены")
    
    # Пример использования итератора
    print("\nПример работы итератора:")
    iterator = WeatherIterator(input_file)
    for i, (date, data) in enumerate(iterator):
        print(f"Date: {date}, Data: {data}")
        if i >= 4:  # Выводим только первые 5 записей для примера
            break