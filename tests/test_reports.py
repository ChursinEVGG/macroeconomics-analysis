import pytest
import csv
import tempfile
from pathlib import Path
from main import ReportGenerator, read_csv_files

def create_test_csv(content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        return f.name

@pytest.fixture
def sample_csv_data():
    return """country,year,gdp,gdp_growth,inflation,unemployment,population,continent
United States,2023,25462,2.1,3.4,3.7,339,North America
United States,2022,23315,2.1,8.0,3.6,338,North America
China,2023,17963,5.2,2.5,5.2,1425,Asia
China,2022,17734,3.0,2.0,5.6,1423,Asia
Germany,2023,4086,-0.3,6.2,3.0,83,Europe"""

@pytest.fixture
def generator():
    return ReportGenerator()

class TestReportGenerator:
    def test_available_reports(self, generator):
        reports = generator.get_available_reports()
        assert 'average-gdp' in reports
        assert len(reports) == 1
    
    def test_generate_average_gdp_report(self, generator, sample_csv_data):
        tmp_file = create_test_csv(sample_csv_data)
        
        try:
            data = read_csv_files([tmp_file])
            result = generator.generate_report('average-gdp', data)
            
            assert len(result) == 3
            
            countries = [item['country'] for item in result]
            assert 'United States' in countries
            assert 'China' in countries
            assert 'Germany' in countries
            
            for item in result:
                assert 'country' in item
                assert 'average_gdp' in item
                assert isinstance(item['average_gdp'], float)
            
            sorted_gdp = [item['average_gdp'] for item in result]
            assert sorted_gdp == sorted(sorted_gdp, reverse=True)
            
            us_data = next(item for item in result if item['country'] == 'United States')
            expected_avg = (25462 + 23315) / 2
            assert us_data['average_gdp'] == pytest.approx(expected_avg)
            
        finally:
            Path(tmp_file).unlink()
    
    def test_generate_unknown_report(self, generator, sample_csv_data):
        tmp_file = create_test_csv(sample_csv_data)
        
        try:
            data = read_csv_files([tmp_file])
            with pytest.raises(ValueError, match="Unknown report"):
                generator.generate_report('unknown-report', data)
        finally:
            Path(tmp_file).unlink()

class TestReadCSVFiles:
    def test_read_single_file(self, sample_csv_data):
        tmp_file = create_test_csv(sample_csv_data)
        
        try:
            data = read_csv_files([tmp_file])
            assert len(data) == 5
            assert data[0]['country'] == 'United States'
            assert data[0]['gdp'] == '25462'
            assert data[2]['country'] == 'China'
        finally:
            Path(tmp_file).unlink()
    
    def test_read_multiple_files(self, sample_csv_data):
        tmp_file1 = create_test_csv(sample_csv_data)
        tmp_file2 = create_test_csv(sample_csv_data)
        
        try:
            data = read_csv_files([tmp_file1, tmp_file2])
            assert len(data) == 10
        finally:
            Path(tmp_file1).unlink()
            Path(tmp_file2).unlink()
    
    def test_read_nonexistent_file(self):
        data = read_csv_files(['nonexistent.csv'])
        assert data == []
    
    def test_read_invalid_csv(self):
        tmp_file = create_test_csv("invalid,csv,content\n1,2")
        
        try:
            data = read_csv_files([tmp_file])
            assert len(data) == 1
        finally:
            Path(tmp_file).unlink()

class TestIntegration:
    def test_full_pipeline(self, sample_csv_data):
        tmp_file = create_test_csv(sample_csv_data)
        
        try:
            generator = ReportGenerator()
            data = read_csv_files([tmp_file])
            report = generator.generate_report('average-gdp', data)
            
            assert len(report) == 3
            
            us_item = next(item for item in report if item['country'] == 'United States')
            china_item = next(item for item in report if item['country'] == 'China')
            germany_item = next(item for item in report if item['country'] == 'Germany')
            
            assert us_item['average_gdp'] > china_item['average_gdp']
            assert china_item['average_gdp'] > germany_item['average_gdp']
            
        finally:
            Path(tmp_file).unlink()
