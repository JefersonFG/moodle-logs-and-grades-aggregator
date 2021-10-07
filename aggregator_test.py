import csv
import json
import os
import shutil
import unittest
from datetime import datetime

import pandas as pd

import aggregator
import student_data


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
                    '01/02/2001 10:00',
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
        with os.scandir(self.test_results_path) as scan_object:
            self.assertTrue(any(scan_object), "no file created on the results folder")

    def test_main_metadata(self):
        """Tests that the main metadata of the student trajectory is present on the resulting jsons"""
        aggregator.aggregate_data(self.test_logs_path, self.test_grades_path, self.test_results_path)
        with os.scandir(self.test_results_path) as scan_object:
            for entry in scan_object:
                with open(os.path.join(self.test_results_path, entry.name), 'r') as file:
                    file_content = file.read()
                content_json = json.loads(file_content)

                # Checks for name and final grade
                self.assertIn(student_data.student_name, content_json)
                self.assertIn(student_data.student_final_grade, content_json)

    def test_grades_and_interactions(self):
        """Tests that grades are present for the student and validates interactions if present (may not be)"""
        aggregator.aggregate_data(self.test_logs_path, self.test_grades_path, self.test_results_path)
        with os.scandir(self.test_results_path) as scan_object:
            for entry in scan_object:
                with open(os.path.join(self.test_results_path, entry.name), 'r') as file:
                    file_content = file.read()
                content_json = json.loads(file_content)

                # Checks for a dictionary of grades, must be present
                self.assertIn(student_data.student_grades, content_json)
                self.assertTrue(isinstance(content_json[student_data.student_grades], dict))
                for key, value in content_json[student_data.student_grades].items():
                    self.assertTrue(isinstance(key, str))
                    self.assertTrue(isinstance(value, int))

                # Check for interactions, which may be missing if student didn't interact with moodle
                if student_data.student_interactions in content_json:
                    self.assertTrue(isinstance(content_json[student_data.student_interactions], list))
                    for interaction in content_json[student_data.student_interactions]:
                        for key, value in interaction.items():
                            self.assertTrue(isinstance(key, str))
                            self.assertTrue(isinstance(value, str))

    def test_interactions_in_timeline(self):
        """Tests that students interactions are sorted in ascending time, so a timeline of events can be created"""
        aggregator.aggregate_data(self.test_logs_path, self.test_grades_path, self.test_results_path)
        with os.scandir(self.test_results_path) as scan_object:
            for entry in scan_object:
                with open(os.path.join(self.test_results_path, entry.name), 'r') as file:
                    file_content = file.read()
                content_json = json.loads(file_content)

                # Check for interactions, which may be missing if student didn't interact with moodle
                if student_data.student_interactions in content_json:
                    previous_time = ""
                    for interaction in content_json[student_data.student_interactions]:
                        current_time = datetime.strptime(interaction[aggregator.hour_column], "%d/%m/%Y %H:%M")
                        if previous_time != "":
                            self.assertGreater(current_time, previous_time)
                        previous_time = current_time


if __name__ == '__main__':
    unittest.main()
