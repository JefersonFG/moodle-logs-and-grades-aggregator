import json
import os

# Definition of names of metadata keys
student_name = 'name'
student_final_grade = 'final_grade'
student_grades = 'grades'
student_interactions = 'interactions'
student_forum_interactions = 'forum_interactions'
student_total_moodle_interactions = 'total_moodle_interactions'


# Definition of student data to be exported to a JSON file
# Includes the student name and final grade directly
# As well as number of interactions on the forum and on moodle as a whole
# Plus lists of grades on other activities and of interactions with moodle, sorted by time
class StudentData:
    def __init__(self, name, final_grade):
        self.name = name
        self.final_grade = final_grade
        self.forum_interactions = 0
        self.total_moodle_interactions = 0

    def to_json(self, target_path) -> None:
        """Saves current student data as a JSON file inside the folder pointed to by target_path"""
        output_path = os.path.join(target_path, self.name + '.json')
        result = json.dumps(self.__dict__, indent=4)

        with open(output_path, "w") as output_file:
            output_file.write(result)
