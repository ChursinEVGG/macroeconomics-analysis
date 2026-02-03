
Как добавить новый отчет

Шаг 1: Добавить метод в ReportGenerator

В классе ReportGenerator добавьте новый метод для генерации отчета:

python
def _generate_new_report(self, data):
    # Обработка данных
    # data - список словарей с данными из CSV
    
    result = []
    # Ваша логика обработки
    
    return result  # список словарей
Шаг 2: Зарегистрировать отчет

В методе __init__ класса ReportGenerator добавьте отчет в словарь self.reports:

python
self.reports = {
    'average-gdp': self._generate_average_gdp_report,
    'new-report-name': self._generate_new_report  # добавьте эту строку
}
Шаг 3: Написать тесты

Создайте тесты для нового отчета в файле tests/test_reports.py:

python
def test_generate_new_report(self, generator, sample_csv_data):
    # Тестируйте вашу функцию
    pass
Требования к отчету:

Метод должен принимать data (список словарей)
Должен возвращать список словарей
Каждый словарь в результате представляет строку отчета
Ключи словаря станут заголовками таблицы
Значения должны быть простыми типами (str, int, float)
Пример нового отчета (средняя инфляция):

python
def _generate_average_inflation(self, data):
    country_inflation = defaultdict(list)
    
    for row in data:
        country = row['country']
        inflation = float(row['inflation'])
        country_inflation[country].append(inflation)
    
    result = []
    for country, inflation_values in country_inflation.items():
        avg_inflation = sum(inflation_values) / len(inflation_values)
        result.append({
            'country': country,
            'average_inflation': round(avg_inflation, 2)
        })
    
    result.sort(key=lambda x: x['average_inflation'], reverse=True)
    return result
Зарегистрируйте в __init__:

python
'average-inflation': self._generate_average_inflation
