import os
os.environ["GEONAMES_USERNAME"] = "siddhyadav"

from kerykeion import AstrologicalSubject
from datetime import datetime
from csv_handler import append_to_csv
from s3_upload import upload_to_s3
from config import S3_BUCKET

def get_person_details(label):
    print(f"\nEnter details for {label}:")
    name = input("Name: ")
    
    # Input validation with error handling
    while True:
        try:
            day = int(input("Day of Birth (1-31): "))
            if 1 <= day <= 31:
                break
            else:
                print("Please enter a valid day (1-31)")
        except ValueError:
            print("Please enter a valid number")
    
    while True:
        try:
            month = int(input("Month of Birth (1-12): "))
            if 1 <= month <= 12:
                break
            else:
                print("Please enter a valid month (1-12)")
        except ValueError:
            print("Please enter a valid number")
    
    while True:
        try:
            year = int(input("Year of Birth (YYYY): "))
            if 1900 <= year <= 2100:
                break
            else:
                print("Please enter a valid year (1900-2100)")
        except ValueError:
            print("Please enter a valid number")
    
    while True:
        try:
            hour = int(input("Hour of Birth (0-23): "))
            if 0 <= hour <= 23:
                break
            else:
                print("Please enter a valid hour (0-23)")
        except ValueError:
            print("Please enter a valid number")
    
    while True:
        try:
            minute = int(input("Minute of Birth (0-59): "))
            if 0 <= minute <= 59:
                break
            else:
                print("Please enter a valid minute (0-59)")
        except ValueError:
            print("Please enter a valid number")
    
    place = input("Place of Birth (City name): ")

    # Try to create AstrologicalSubject with geonames, fallback to manual coordinates
    try:
        print(f"Fetching coordinates for {place}...")
        return AstrologicalSubject(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            city=place,
            online=True,
            geonames_username="siddhyadav"
        )
    except Exception as e:
        print(f"Could not find coordinates for '{place}'. Using default coordinates.")
        print("Please try a more specific city name (e.g., 'Varanasi, India' instead of 'Varanasi')")
        
        # Use default coordinates for India
        return AstrologicalSubject(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            lat=25.3176,  # Varanasi coordinates
            lng=82.9739,
            tz_str="Asia/Kolkata",
            online=False
        )

def compatibility_score(person1, person2):
    score = 0
    total_factors = 3  # Sun, Moon, Ascendant

    if person1.sun.sign == person2.sun.sign:
        score += 1
    if person1.moon.sign == person2.moon.sign:
        score += 1
    if person1.ascendant.sign == person2.ascendant.sign:
        score += 1

    percentage = (score / total_factors) * 100
    return percentage

def main():
    print("=== Astrology Compatibility Tool (Local Calculation) ===")
    
    # Get both people's details
    person1 = get_person_details("Person 1")
    person2 = get_person_details("Person 2")

    # Display their key chart info
    print(f"\n--- {person1.name}'s Chart ---")
    print("Sun Sign:", person1.sun.sign)
    print("Moon Sign:", person1.moon.sign)
    print("Ascendant:", person1.ascendant.sign)

    print(f"\n--- {person2.name}'s Chart ---")
    print("Sun Sign:", person2.sun.sign)
    print("Moon Sign:", person2.moon.sign)
    print("Ascendant:", person2.ascendant.sign)

    # Compatibility calculation
    score = compatibility_score(person1, person2)
    print(f"\nCompatibility Score: {score:.2f}%")

    # Save match to CSV if compatibility is above threshold
    if score >= 50:  # You can adjust this threshold
        match_data = {
            "person1_name": person1.name,
            "person1_sun_sign": person1.sun.sign,
            "person1_moon_sign": person1.moon.sign,
            "person1_ascendant": person1.ascendant.sign,
            "person2_name": person2.name,
            "person2_sun_sign": person2.sun.sign,
            "person2_moon_sign": person2.moon.sign,
            "person2_ascendant": person2.ascendant.sign,
            "compatibility_score": score,
            "match_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        csv_file = append_to_csv(match_data)
        print(f"\n✅ Match saved to {csv_file}")
        print(f"📊 Compatibility: {score:.2f}% - {person1.name} & {person2.name}")
        
        # Upload to S3
        try:
            s3_key = f"astrology-matches/matches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            upload_to_s3(str(csv_file), s3_key)
            print(f"☁️  CSV uploaded to S3: s3://{S3_BUCKET}/{s3_key}")
        except Exception as e:
            print(f"❌ S3 upload failed: {e}")
            print("💡 Make sure your AWS credentials are configured in .env file")
    else:
        print(f"\n❌ No match saved (score {score:.2f}% below 50% threshold)")

if __name__ == "__main__":
    main()
