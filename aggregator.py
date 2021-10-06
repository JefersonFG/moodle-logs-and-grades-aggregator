import argparse


# Main aggregation function
def aggregate_data(logs_path, grades_path, target_path) -> None:
    """Main function for data aggregation, writes results into json files on the target path."""
    raise Exception("Not implemented")


# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Use this tool to aggregate student data from the interaction
        logs and grades exported from moodle, generating JSONs for each student on the target path''')
    parser.add_argument("source_logs_path", help="Path to the moodle logs")
    parser.add_argument("source_grades_path", help="Path to the moodle grades")
    parser.add_argument("target_result_path", help="Path to save the aggregated data, expected to be a folder")

    args = parser.parse_args()
    aggregate_data(args.source_logs_path, args.source_grades_path, args.target_result_path)
