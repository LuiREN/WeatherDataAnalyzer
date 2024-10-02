import pandas as pd
import os

def split_by_week(input_file):
    """
    Разделяет исходный CSV файл на отдельные файлы по неделям.
    
    Args:
        input_file (str): Путь к исходному CSV файлу.
    """
    # Проверяем существование файла
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден.")
        return

    # Читаем CSV файл
    df = pd.read_csv(input_file, parse_dates=['Дата'])

    # Группируем данные по неделям
    df['Week'] = df['Дата'].dt.to_period('W')
    grouped = df.groupby('Week')

    # Создаем папку для выходных файлов
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_folder = os.path.join('dataset', 'weekly_data', file_name)
    os.makedirs(output_folder, exist_ok=True)

    # Сохраняем данные каждой недели в отдельный файл
    for week, group in grouped:
        start_date = group['Дата'].min().strftime('%Y%m%d')
        end_date = group['Дата'].max().strftime('%Y%m%d')
        filename = f'{start_date}_{end_date}.csv'
        filepath = os.path.join(output_folder, filename)
        group.drop('Week', axis=1).to_csv(filepath, index=False)
        print(f"Создан файл: {filename}")

    print(f"Файлы по неделям созданы в папке {output_folder}.")

if __name__ == "__main__":
    input_file = input("Введите путь к исходному CSV файлу: ")
    split_by_week(input_file)