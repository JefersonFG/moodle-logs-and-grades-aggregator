import argparse
import os

import pandas as pd

from student_data import StudentData

# Column names for the logs and grades files
complete_name_column = 'Nome completo'
final_grade_column = 'Total do curso (Real)'
hour_column = 'Hora'


# Main aggregation function
def aggregate_data(logs_path, grades_path, target_path) -> None:
    """Main function for data aggregation, writes results into json files on the target path."""
    # Checks if target_path is empty, if it is creates the directory, else checks that it is a directory
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    elif not os.path.isdir(target_path):
        raise Exception("Target path is not a directory")

    # Reads student data from input files
    logs_df = pd.read_csv(logs_path)
    grades_df = pd.read_excel(grades_path)

    # Sort log entries by their ascending time
    logs_df.sort_values(by=hour_column, key=lambda col: pd.to_datetime(col, dayfirst=True),
                        inplace=True, ascending=True)

    # Groups all entries by student name
    grouped_student_logs = logs_df.groupby(complete_name_column)
    grouped_student_grades = grades_df.groupby(complete_name_column)

    # Map of student names to their information, gathered on the StudentData class
    students = dict()

    # Starts with the grades list, as it should cover all students
    for group in grouped_student_grades.groups:
        student_info = grouped_student_grades.get_group(group)

        # Since grades have one entry for each student we can just get the data at the first index
        current_student = StudentData(student_info[complete_name_column].iat[0],
                                      int(student_info[final_grade_column].iat[0]))

        # Convert the df to a dictionary removing the indexes, creating a map of column to row
        current_student.grades = student_info.to_dict('records')[0]

        # Remove columns for name and final grade as we already took this data out
        del current_student.grades[complete_name_column]
        del current_student.grades[final_grade_column]

        # Save current student data with the name as the key
        students[current_student.name] = current_student

    # Looks for entries for each student on the logs, update the student entry on the map of student data
    for group in grouped_student_logs.groups:
        student_info = grouped_student_logs.get_group(group)

        # Look for the student data on the existing map, if it doesn't exist the student has no grades
        # Here we decide to warn about the error and skip the student, it might be wise to stop and raise an error
        student_name = student_info[complete_name_column].iat[0]
        if student_name not in students:
            print(f"Found interactions of student '{student_name}' but no grades, skipping the student")
            continue

        # Save interactions under student data
        current_student = students[student_name]
        current_student.interactions = student_info.to_dict('records')

        # Remove full name from internal interactions as well
        for interaction in current_student.interactions:
            del interaction[complete_name_column]

    # Save student info on the target folder
    for _, student in students.items():
        student.to_json(target_path)


# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Use this tool to aggregate student data from the interaction
        logs and grades exported from moodle, generating JSONs for each student on the target path''')
    parser.add_argument("source_logs_path", help="Path to the moodle logs")
    parser.add_argument("source_grades_path", help="Path to the moodle grades")
    parser.add_argument("target_result_path", help="Path to save the aggregated data, expected to be a folder")

    args = parser.parse_args()
    aggregate_data(args.source_logs_path, args.source_grades_path, args.target_result_path)
