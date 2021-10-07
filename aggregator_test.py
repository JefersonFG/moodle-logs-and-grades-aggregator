import csv
import os
import shutil
import unittest

import pandas as pd

import aggregator


class AggregatorTest(unittest.TestCase):
    test_logs_path = 'test_logs.csv'
    test_grades_path = 'test_grades.xlsx'
    test_results_path = 'test_results'

    def setUp(self):
        """"setUp creates the test dataset with valid data"""

        # Activity logs
        df = pd.DataFrame(
            {
                'Hora': [
                    '01/01/2001 10:00',
                    '01/01/2001 11:00',
                    '01/01/2001 12:00',
                    '01/01/2001 13:00',
                    '01/01/2001 14:00',
                    '01/01/2001 15:00',
                ],
                'Nome completo': [
                    'Test name 1',
                    'Test name 2',
                    'Administrador Moodle',
                    'Test name 3',
                    'Test name 2',
                    'Test name 1'
                ],
                '"Contexto do Evento"': [
                    'Test course 1',
                    'Test course 1',
                    'Test course 2',
                    'Test course 1',
                    'Test course 1',
                    'Test course 2'
                ],
                'Componente': [
                    'Tarefa',
                    'Tarefa',
                    'Lixeira',
                    'Tarefa',
                    'Fórum',
                    'Fórum'
                ],
                '"Nome do evento"': [
                    'O status da submissão foi visualizado.',
                    'Comentário visualizado',
                    'Item excluído',
                    'Curso visto',
                    'Post criado',
                    'Discussão visualizada'
                ],
            }
        )

        df.to_csv(self.test_logs_path, index=False, quoting=csv.QUOTE_NONE)

        # Grades
        # Here we assume the grades have had the name and surname columns combined into one full name column
        # We also ignore the email column, if you're editing this script you might want to test the support here
        df = pd.DataFrame(
            {
                'Nome completo': [
                    'Test name 1',
                    'Test name 2',
                    'Test name 3',
                    'Test name 4'
                ],
                'Tarefa 1': [
                    '10',
                    '20',
                    '30',
                    '0'
                ],
                'Tarefa 2': [
                    '40',
                    '50',
                    '60',
                    '0'
                ],
                'Tarefa 3': [
                    '70',
                    '80',
                    '90',
                    '0'
                ],
                'Total do curso (Real)': [
                    '50',
                    '50',
                    '50',
                    '0'
                ],
            }
        )

        with pd.ExcelWriter(self.test_grades_path) as writer:
            df.to_excel(writer, index=False)

    def tearDown(self):
        """tearDown deletes both the source and the target files to clean up after the tests"""
        if os.path.exists(self.test_logs_path):
            os.remove(self.test_logs_path)
        if os.path.exists(self.test_grades_path):
            os.remove(self.test_grades_path)
        if os.path.exists(self.test_results_path):
            shutil.rmtree(self.test_results_path)

    def test_create_results(self):
        """Tests that results are written to the disk, but doesn't validate their contents"""
        aggregator.aggregate_data(self.test_logs_path, self.test_grades_path, self.test_results_path)
        self.assertTrue(any(os.scandir(self.test_results_path)))


if __name__ == '__main__':
    unittest.main()
