from match import match_people
from csv_handler import append_to_csv
from s3_upload import upload_to_s3

def main():
    person1 = {
        "name": "John",
        "dob": "1990-05-15",
        "birth_time": "14:30",
        "birth_place": "New York, USA"
    }
    person2 = {
        "name": "Jane",
        "dob": "1992-07-10",
        "birth_time": "09:15",
        "birth_place": "Los Angeles, USA"
    }

    # Match data locally
    match_result = match_people(person1, person2)

    # Append to CSV
    csv_file_path = append_to_csv(match_result)

    # Upload to S3
    upload_to_s3(str(csv_file_path), "matches.csv")

if __name__ == "__main__":
    main()
