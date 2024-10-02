import pandas as pd
import os

def split_by_year(input_file):
    """
    Разделяет исходный CSV файл на отдельные файлы по годам.
    
    Args:
        input_file (str): Путь к исходному CSV файлу.
    """
    # Проверяем существование файла
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден.")
        return

    # Читаем CSV файл
    df = pd.read_csv(input_file, parse_dates=['Дата'])

    # Группируем данные по годам
    grouped = df.groupby(df['Дата'].dt.year)

    # Создаем папку для выходных файлов
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_folder = os.path.join('dataset', 'yearly_data', file_name)
    os.makedirs(output_folder, exist_ok=True)

    # Сохраняем данные каждого года в отдельный файл
    for year, group in grouped:
        start_date = group['Дата'].min().strftime('%Y%m%d')
        end_date = group['Дата'].max().strftime('%Y%m%d')
        filename = f'{start_date}_{end_date}.csv'
        filepath = os.path.join(output_folder, filename)
        group.to_csv(filepath, index=False)
        print(f"Создан файл: {filename}")

    print(f"Файлы по годам созданы в папке {output_folder}.")

if __name__ == "__main__":
    input_file = input("Введите путь к исходному CSV файлу: ")
    split_by_year(input_file)