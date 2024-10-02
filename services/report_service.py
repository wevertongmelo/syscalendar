# services/report_service.py

import os
from utils.report_generator import ReportGenerator

def generate_booking_report():
    try:
        report_generator = ReportGenerator()
        report_path = 'path/to/report.csv'
        report_generator.generate_booking_report(report_path)
        return report_path
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar o relatório: {e}")
