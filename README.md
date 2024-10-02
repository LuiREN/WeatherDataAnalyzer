# WeatherDataAnalyzer

WeatherDataAnalyzer - это проект для анализа исторических данных о погоде в Самаре.

## Установка

1. Клонируйте репозиторий:
   https://github.com/LuiREN/WeatherDataAnalyzer.git
2. Перейдите в директорию проекта:
   cd WeatherDataAnalyzer
3. Установите зависимости:
   pip install -r requirements.txt
   
## Использование

Запустите main.py:
  python main.py

Следуйте инструкциям в консольном меню для выполнения различных операций с данными о погоде.

## Функциональность

- Сбор исторических данных о погоде в Самаре
- Разделение CSV файла на файлы с датами и данными
- Разделение данных по годам
- Разделение данных по неделям
- Получение данных по конкретной дате

## Структура проекта

- main.py: Основной файл для запуска программы
- scraper.py: Модуль для сбора данных о погоде
- split_csv.py: Модуль для разделения CSV файла
- split_by_year.py: Модуль для разделения данных по годам
- split_by_week.py: Модуль для разделения данных по неделям
- data_retrieval.py: Модуль для получения данных по дате
