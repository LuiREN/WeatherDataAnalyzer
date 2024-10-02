import os
from scraper import WeatherScraper
from split_csv import split_csv
from split_by_year import split_by_year
from split_by_week import split_by_week
from data_retrieval import get_data_by_date, WeatherIterator
from datetime import datetime

def get_csv_file():
    dataset_folder = 'dataset'
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    files = [f for f in os.listdir(dataset_folder) if f.endswith('.csv')]
    
    if not files:
        print("В папке dataset нет CSV файлов.")
        return None
    
    print("Доступные CSV файлы:")
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")
    
    while True:
        try:
            choice = int(input("Выберите номер файла для обработки: ")) - 1
            if 0 <= choice < len(files):
                return os.path.join(dataset_folder, files[choice])
            else:
                print("Неверный номер. Попробуйте еще раз.")
        except ValueError:
            print("Пожалуйста, введите число.")

def main():
    while True:
        print("\nМеню:")
        print("1. Запустить сбор данных")
        print("2. Разделить файл на X.csv и Y.csv")
        print("3. Разделить файл по годам")
        print("4. Разделить файл по неделям")
        print("5. Получить данные по дате")
        print("6. Использовать итератор")
        print("7. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            scraper = WeatherScraper()
            scraper.run()
        elif choice in ['2', '3', '4']:
            input_file = get_csv_file()
            if input_file:
                if choice == '2':
                    split_csv(input_file)
                elif choice == '3':
                    split_by_year(input_file)
                else:
                    split_by_week(input_file)
        elif choice == '5':
            input_file = get_csv_file()
            if input_file:
                date_str = input("Введите дату в формате YYYY-MM-DD: ")
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    data = get_data_by_date(date, input_file)
                    print(data if data else "Данные не найдены")
                except ValueError:
                    print("Неверный формат даты")
        elif choice == '6':
            input_file = get_csv_file()
            if input_file:
                iterator = WeatherIterator(input_file)
                for date, data in iterator:
                    print(f"Date: {date}, Data: {data}")
                    if input("Нажмите Enter для следующей записи или 'q' для выхода: ").lower() == 'q':
                        break
        elif choice == '7':
            print("Выход из программы.")
            return  # Используем return вместо sys.exit()
        else:
            print("Неверный выбор. Попробуйте еще раз.")

if __name__ == "__main__":
    main()