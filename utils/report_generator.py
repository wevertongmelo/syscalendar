# utils/report_generator.py

import csv

class ReportGenerator:
    def generate_booking_report(self, output_path):
        # Exemplo de lógica para gerar o relatório
        bookings = [
            {'id': 1, 'user': 'John Doe', 'equipment': 'Laptop', 'date': '2024-08-18'},
            {'id': 2, 'user': 'Jane Doe', 'equipment': 'Projector', 'date': '2024-08-19'},
        ]
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['id', 'user', 'equipment', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for booking in bookings:
                writer.writerow(booking)
