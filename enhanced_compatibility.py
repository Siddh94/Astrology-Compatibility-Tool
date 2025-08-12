import os
os.environ["GEONAMES_USERNAME"] = "siddhyadav"

from kerykeion import AstrologicalSubject, SynastryAspects, RelationshipScore
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

def display_detailed_chart(person, label):
    """Display detailed chart information."""
    print(f"\n{'='*50}")
    print(f"📊 {label}: {person.name}'s Detailed Chart")
    print(f"{'='*50}")
    
    # Personal Planets
    print("\n🌟 PERSONAL PLANETS:")
    print(f"Sun: {person.sun.sign} {person.sun.position:.1f}° ({person.sun.element} {person.sun.quality})")
    print(f"Moon: {person.moon.sign} {person.moon.position:.1f}° ({person.moon.element} {person.moon.quality})")
    print(f"Mercury: {person.mercury.sign} {person.mercury.position:.1f}°")
    print(f"Venus: {person.venus.sign} {person.venus.position:.1f}°")
    print(f"Mars: {person.mars.sign} {person.mars.position:.1f}°")
    
    # Social Planets
    print("\n🌍 SOCIAL PLANETS:")
    print(f"Jupiter: {person.jupiter.sign} {person.jupiter.position:.1f}°")
    print(f"Saturn: {person.saturn.sign} {person.saturn.position:.1f}°")
    
    # Outer Planets
    print("\n🪐 OUTER PLANETS:")
    print(f"Uranus: {person.uranus.sign} {person.uranus.position:.1f}°")
    print(f"Neptune: {person.neptune.sign} {person.neptune.position:.1f}°")
    print(f"Pluto: {person.pluto.sign} {person.pluto.position:.1f}°")
    
    # Angles
    print("\n📐 ANGLES:")
    print(f"Ascendant: {person.ascendant.sign} {person.ascendant.position:.1f}°")
    print(f"Descendant: {person.descendant.sign} {person.descendant.position:.1f}°")
    
    # Check if midheaven and IC exist
    if hasattr(person, 'midheaven'):
        print(f"Midheaven: {person.midheaven.sign} {person.midheaven.position:.1f}°")
    if hasattr(person, 'ic'):
        print(f"IC: {person.ic.sign} {person.ic.position:.1f}°")
    
    # Houses
    print("\n🏠 HOUSE CUSPS:")
    print(f"1st House: {person.first_house.sign} {person.first_house.position:.1f}°")
    print(f"2nd House: {person.second_house.sign} {person.second_house.position:.1f}°")
    print(f"3rd House: {person.third_house.sign} {person.third_house.position:.1f}°")
    print(f"4th House: {person.fourth_house.sign} {person.fourth_house.position:.1f}°")
    print(f"5th House: {person.fifth_house.sign} {person.fifth_house.position:.1f}°")
    print(f"6th House: {person.sixth_house.sign} {person.sixth_house.position:.1f}°")
    print(f"7th House: {person.seventh_house.sign} {person.seventh_house.position:.1f}°")
    print(f"8th House: {person.eighth_house.sign} {person.eighth_house.position:.1f}°")
    print(f"9th House: {person.ninth_house.sign} {person.ninth_house.position:.1f}°")
    print(f"10th House: {person.tenth_house.sign} {person.tenth_house.position:.1f}°")
    print(f"11th House: {person.eleventh_house.sign} {person.eleventh_house.position:.1f}°")
    print(f"12th House: {person.twelfth_house.sign} {person.twelfth_house.position:.1f}°")

def advanced_compatibility_score(person1, person2):
    """Advanced compatibility calculation using multiple factors."""
    score = 0
    total_factors = 0
    
    # Element compatibility
    elements = {
        'Fire': ['Ari', 'Leo', 'Sag'],
        'Earth': ['Tau', 'Vir', 'Cap'],
        'Air': ['Gem', 'Lib', 'Aqu'],
        'Water': ['Can', 'Sco', 'Pis']
    }
    
    # Get elements for each person
    p1_sun_element = next((k for k, v in elements.items() if person1.sun.sign in v), 'Unknown')
    p1_moon_element = next((k for k, v in elements.items() if person1.moon.sign in v), 'Unknown')
    p2_sun_element = next((k for k, v in elements.items() if person2.sun.sign in v), 'Unknown')
    p2_moon_element = next((k for k, v in elements.items() if person2.moon.sign in v), 'Unknown')
    
    print(f"\n🔥 ELEMENT COMPATIBILITY:")
    print(f"{person1.name}: Sun {p1_sun_element}, Moon {p1_moon_element}")
    print(f"{person2.name}: Sun {p2_sun_element}, Moon {p2_moon_element}")
    
    # Sun sign compatibility (30 points)
    total_factors += 30
    if person1.sun.sign == person2.sun.sign:
        score += 30
        print(f"✅ Same Sun sign: +30 points")
    elif p1_sun_element == p2_sun_element:
        score += 20
        print(f"✅ Same element Sun signs: +20 points")
    elif (p1_sun_element in ['Fire', 'Air'] and p2_sun_element in ['Fire', 'Air']) or \
         (p1_sun_element in ['Earth', 'Water'] and p2_sun_element in ['Earth', 'Water']):
        score += 15
        print(f"✅ Compatible element groups: +15 points")
    else:
        print(f"❌ Different Sun elements: +0 points")
    
    # Moon sign compatibility (25 points)
    total_factors += 25
    if person1.moon.sign == person2.moon.sign:
        score += 25
        print(f"✅ Same Moon sign: +25 points")
    elif p1_moon_element == p2_moon_element:
        score += 20
        print(f"✅ Same element Moon signs: +20 points")
    elif (p1_moon_element in ['Fire', 'Air'] and p2_moon_element in ['Fire', 'Air']) or \
         (p1_moon_element in ['Earth', 'Water'] and p2_moon_element in ['Earth', 'Water']):
        score += 15
        print(f"✅ Compatible Moon element groups: +15 points")
    else:
        print(f"❌ Different Moon elements: +0 points")
    
    # Ascendant compatibility (15 points)
    total_factors += 15
    if person1.ascendant.sign == person2.ascendant.sign:
        score += 15
        print(f"✅ Same Ascendant: +15 points")
    else:
        print(f"❌ Different Ascendants: +0 points")
    
    # Venus-Mars compatibility (20 points)
    total_factors += 20
    if person1.venus.sign == person2.mars.sign or person1.mars.sign == person2.venus.sign:
        score += 20
        print(f"✅ Venus-Mars conjunction: +20 points")
    elif person1.venus.sign == person2.venus.sign:
        score += 15
        print(f"✅ Same Venus sign: +15 points")
    else:
        print(f"❌ Different Venus signs: +0 points")
    
    # Jupiter-Saturn compatibility (10 points)
    total_factors += 10
    if person1.jupiter.sign == person2.saturn.sign or person1.saturn.sign == person2.jupiter.sign:
        score += 10
        print(f"✅ Jupiter-Saturn aspect: +10 points")
    else:
        print(f"❌ No Jupiter-Saturn aspect: +0 points")
    
    percentage = (score / total_factors) * 100
    return percentage, score, total_factors

def main():
    print("=== 🌟 Enhanced Astrology Compatibility Tool ===")
    print("Using advanced kerykeion features for detailed analysis")
    
    # Get both people's details
    person1 = get_person_details("Person 1")
    person2 = get_person_details("Person 2")

    # Display detailed charts
    display_detailed_chart(person1, "Person 1")
    display_detailed_chart(person2, "Person 2")

    # Advanced compatibility calculation
    print(f"\n{'='*50}")
    print("💕 COMPATIBILITY ANALYSIS")
    print(f"{'='*50}")
    
    score, points, total = advanced_compatibility_score(person1, person2)
    
    print(f"\n📊 FINAL SCORE: {points}/{total} points = {score:.2f}%")
    
    # Compatibility interpretation
    if score >= 80:
        print("🌟 EXCELLENT MATCH! Very high compatibility")
    elif score >= 65:
        print("💫 GREAT MATCH! High compatibility")
    elif score >= 50:
        print("✨ GOOD MATCH! Moderate compatibility")
    elif score >= 35:
        print("🤝 FAIR MATCH! Some compatibility")
    else:
        print("⚠️  CHALLENGING MATCH! Low compatibility")

    # Save match to CSV if compatibility is above threshold
    if score >= 50:
        match_data = {
            "person1_name": person1.name,
            "person1_sun_sign": person1.sun.sign,
            "person1_moon_sign": person1.moon.sign,
            "person1_ascendant": person1.ascendant.sign,
            "person1_venus": person1.venus.sign,
            "person1_mars": person1.mars.sign,
            "person2_name": person2.name,
            "person2_sun_sign": person2.sun.sign,
            "person2_moon_sign": person2.moon.sign,
            "person2_ascendant": person2.ascendant.sign,
            "person2_venus": person2.venus.sign,
            "person2_mars": person2.mars.sign,
            "compatibility_score": score,
            "compatibility_points": points,
            "total_possible_points": total,
            "match_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        csv_file = append_to_csv(match_data)
        print(f"\n✅ Match saved to {csv_file}")
        print(f"📊 Compatibility: {score:.2f}% - {person1.name} & {person2.name}")
        
        # Upload to S3
        try:
            s3_key = f"astrology-matches/enhanced_matches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            upload_to_s3(str(csv_file), s3_key)
            print(f"☁️  Enhanced CSV uploaded to S3: s3://{S3_BUCKET}/{s3_key}")
        except Exception as e:
            print(f"❌ S3 upload failed: {e}")
            print("💡 Make sure your AWS credentials are configured in .env file")
    else:
        print(f"\n❌ No match saved (score {score:.2f}% below 50% threshold)")

if __name__ == "__main__":
    main()
