import argparse
import csv
from collections import defaultdict
from pathlib import Path
from tabulate import tabulate
import sys

class ReportGenerator:
    def __init__(self):
        self.reports = {
            'average-gdp': self._generate_average_gdp_report
        }
    
    def _generate_average_gdp_report(self, data):
        country_gdp = defaultdict(list)
        
        for row in data:
            country = row['country']
            gdp = float(row['gdp'])
            country_gdp[country].append(gdp)
        
        result = []
        for country, gdp_values in country_gdp.items():
            avg_gdp = sum(gdp_values) / len(gdp_values)
            result.append({
                'country': country,
                'average_gdp': round(avg_gdp, 2)
            })
        
        result.sort(key=lambda x: x['average_gdp'], reverse=True)
        return result
    
    def generate_report(self, report_name, data):
        if report_name not in self.reports:
            raise ValueError(f"Unknown report: {report_name}")
        
        return self.reports[report_name](data)
    
    def get_available_reports(self):
        return list(self.reports.keys())


def read_csv_files(file_paths):
    data = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            print(f"Warning: File {file_path} does not exist", file=sys.stderr)
            continue
        
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)
            continue
    
    return data


def display_report(report_data, report_name):
    if not report_data:
        print("No data to display")
        return
    
    headers = report_data[0].keys()
    rows = [list(item.values()) for item in report_data]
    
    print(f"\n{report_name.replace('-', ' ').title()} Report")
    print("=" * 50)
    print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f"))


def main():
    parser = argparse.ArgumentParser(
        description='Generate macroeconomic reports from CSV files'
    )
    
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Paths to CSV files with economic data'
    )
    
    parser.add_argument(
        '--report',
        required=True,
        help='Name of the report to generate'
    )
    
    args = parser.parse_args()
    
    generator = ReportGenerator()
    
    if args.report not in generator.get_available_reports():
        print(f"Error: Unknown report '{args.report}'", file=sys.stderr)
        print(f"Available reports: {', '.join(generator.get_available_reports())}")
        sys.exit(1)
    
    data = read_csv_files(args.files)
    
    if not data:
        print("Error: No valid data found in the provided files", file=sys.stderr)
        sys.exit(1)
    
    try:
        report_data = generator.generate_report(args.report, data)
        display_report(report_data, args.report)
    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
