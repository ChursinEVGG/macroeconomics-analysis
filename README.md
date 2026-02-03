# Макроэкономический анализ данных

Скрипт для анализа макроэкономических данных из CSV файлов. Генерирует отчеты на основе предоставленных данных.

## Установка

1. Создайте виртуальное окружение:
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Установите зависимости:
bash
pip install -r requirements.txt
Использование

bash
python main.py --files file1.csv file2.csv --report average-gdp
Параметры:

--files: Пути к CSV файлам с данными (можно указать несколько)
--report: Название отчета (доступно: average-gdp)
Пример:

bash
python main.py --files economic1.csv economic2.csv --report average-gdp
Доступные отчеты

average-gdp

Вычисляет среднее значение ВВП по странам на основе всех предоставленных файлов.
Результат сортируется по убыванию среднего ВВП.

Добавление новых отчетов

Для добавления нового отчета:

Добавьте новую функцию в класс ReportGenerator в main.py
Зарегистрируйте отчет в словаре self.reports
Напишите тесты для нового отчета
Тестирование

Запуск тестов:

bash
pytest tests/ --cov=main --cov-report=term-missing
Запуск тестов с подробным выводом:

bash
pytest tests/ -v
Структура CSV файла

Файлы должны содержать следующие колонки:

country: Название страны
year: Год
gdp: ВВП
gdp_growth: Рост ВВП (%)
inflation: Инфляция (%)
unemployment: Безработица (%)
population: Население (миллионы)
continent: Континент
