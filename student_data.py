import json
import os

# Definition of names of metadata keys
student_name = 'name'
student_final_grade = 'final_grade'
student_grades = 'grades'
student_interactions = 'interactions'


# Definition of student data to be exported to a JSON file
# Includes the student name and final grade directly
# Plus lists of grades on other activities and of interactions with moodle, sorted by time
class StudentData:
    def __init__(self, name, final_grade):
        self.name = name
        self.final_grade = final_grade

    def to_json(self, target_path) -> None:
        """Saves current student data as a JSON file inside the folder pointed to by target_path"""
        output_path = os.path.join(target_path, self.name + '.json')
        result = json.dumps(self.__dict__, indent=4)

        with open(output_path, "w") as output_file:
            output_file.write(result)
