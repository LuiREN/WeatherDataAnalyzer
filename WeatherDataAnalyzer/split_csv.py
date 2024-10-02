import pandas as pd
import os

def split_csv(input_file):
    """
    Разделяет исходный CSV файл на X.csv (даты) и Y.csv (данные).
    
    Args:
        input_file (str): Путь к исходному CSV файлу.
    """
    # Проверяем существование файла
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден.")
        return

    # Создаем папку для выходных файлов
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_folder = os.path.join('dataset', 'split_csv', file_name)
    os.makedirs(output_folder, exist_ok=True)

    # Читаем CSV файл
    df = pd.read_csv(input_file)

    # Проверяем, что первый столбец содержит даты
    if not pd.to_datetime(df.iloc[:, 0], format='%Y-%m-%d', errors='coerce').notna().all():
        print("Первый столбец не содержит корректные даты в формате ISO 8601.")
        return

    # Разделяем на X (даты) и Y (данные)
    X = df.iloc[:, 0]
    Y = df.iloc[:, 1:]

    # Сохраняем файлы
    X.to_csv(os.path.join(output_folder, 'X.csv'), index=False, header=['Date'])
    Y.to_csv(os.path.join(output_folder, 'Y.csv'), index=False)

    print(f"Файлы X.csv и Y.csv успешно созданы в папке {output_folder}.")

if __name__ == "__main__":
    input_file = input("Введите путь к исходному CSV файлу: ")
    split_csv(input_file)