import os
import io
from datetime import datetime, date, time
import contextlib

import streamlit as st
from kerykeion import AstrologicalSubject

from enhanced_compatibility import (
    advanced_compatibility_score,
    display_detailed_chart,
)
from csv_handler import append_to_csv
from s3_upload import upload_to_s3
from config import S3_BUCKET


def create_astrological_subject(
    name: str,
    dob: date,
    tob: time,
    birthplace: str,
    geonames_username: str,
) -> AstrologicalSubject:
    """Create an AstrologicalSubject using geonames; fallback to default coordinates on failure."""
    # Ensure env var for kerykeion geonames
    if geonames_username:
        os.environ["GEONAMES_USERNAME"] = geonames_username

    try:
        return AstrologicalSubject(
            name=name,
            year=dob.year,
            month=dob.month,
            day=dob.day,
            hour=tob.hour,
            minute=tob.minute,
            city=birthplace,
            online=True,
            geonames_username=geonames_username,
        )
    except Exception:
        # Fallback to Varanasi coordinates if geonames lookup fails
        return AstrologicalSubject(
            name=name,
            year=dob.year,
            month=dob.month,
            day=dob.day,
            hour=tob.hour,
            minute=tob.minute,
            lat=25.3176,
            lng=82.9739,
            tz_str="Asia/Kolkata",
            online=False,
        )


def render_chart_details(person: AstrologicalSubject, label: str) -> None:
    """Render chart details by capturing existing print output."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        display_detailed_chart(person, label)
    st.code(buffer.getvalue())


def main() -> None:
    st.set_page_config(page_title="Astrology Compatibility Tool", page_icon="💞", layout="wide")
    st.title("💞 Astrology Compatibility Tool")
    st.caption("Powered by kerykeion and Streamlit")

    # Secrets/env configuration (not shown in UI) - moved after page config
    try:
        geonames_username = st.secrets.get("GEONAMES_USERNAME", "")
    except Exception:
        geonames_username = ""
    
    if not geonames_username:
        geonames_username = os.getenv("GEONAMES_USERNAME", "siddhyadav")

    # Sidebar configuration
    with st.sidebar:
        st.header("Settings")
        save_threshold = st.slider("Save match threshold (%)", min_value=0, max_value=100, value=50, step=5)
        upload_to_s3_opt = st.checkbox("Upload CSV to S3 after save", value=False)

    # Input forms
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Person 1")
        p1_name = st.text_input("Name", key="p1_name")
        p1_dob = st.date_input(
            "Date of Birth",
            key="p1_dob",
            value=date(1990, 1, 1),
            max_value=date(2020, 12, 31),
        )
        p1_tob = st.time_input("Time of Birth", key="p1_tob", value=time(12, 0))
        p1_place = st.text_input("Place of Birth (City, Country)", key="p1_place")

    with col2:
        st.subheader("Person 2")
        p2_name = st.text_input("Name", key="p2_name")
        p2_dob = st.date_input(
            "Date of Birth",
            key="p2_dob",
            value=date(1990, 1, 2),
            max_value=date(2020, 12, 31),
        )
        p2_tob = st.time_input("Time of Birth", key="p2_tob", value=time(12, 0))
        p2_place = st.text_input("Place of Birth (City, Country)", key="p2_place")

    compute = st.button("Compute compatibility", type="primary")

    if compute:
        # Basic validation
        missing = [
            label
            for label, val in [
                ("Person 1 name", p1_name),
                ("Person 1 place", p1_place),
                ("Person 2 name", p2_name),
                ("Person 2 place", p2_place),
            ]
            if not val
        ]
        if missing:
            st.error("Please fill the following fields: " + ", ".join(missing))
            st.stop()

        # Build subjects
        person1 = create_astrological_subject(p1_name, p1_dob, p1_tob, p1_place, geonames_username)
        person2 = create_astrological_subject(p2_name, p2_dob, p2_tob, p2_place, geonames_username)

        # Show chart summaries
        st.subheader("Charts")
        c1, c2 = st.columns(2)
        with c1:
            render_chart_details(person1, "Person 1")
        with c2:
            render_chart_details(person2, "Person 2")

        # Capture and compute advanced compatibility
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            percentage, points_scored, total_points = advanced_compatibility_score(person1, person2)
        details_text = buffer.getvalue()

        st.subheader("Compatibility analysis")
        st.metric("Final Score", f"{percentage:.2f}%")
        st.caption(f"Points: {points_scored}/{total_points}")
        if details_text:
            with st.expander("Show detailed factors"):
                st.code(details_text)

        # Save if meets threshold
        if percentage >= save_threshold:
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
                "compatibility_score": percentage,
                "compatibility_points": points_scored,
                "total_possible_points": total_points,
                "match_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            csv_file = append_to_csv(match_data)
            st.success(f"Match saved to {csv_file}")

            if upload_to_s3_opt:
                try:
                    s3_key = f"astrology-matches/enhanced_matches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    upload_to_s3(str(csv_file), s3_key)
                    st.info(f"Uploaded to s3://{S3_BUCKET}/{s3_key}")
                except Exception as e:
                    st.warning(f"S3 upload failed: {e}")
        else:
            st.warning(
                f"Score {percentage:.2f}% is below threshold {save_threshold}%. Not saved."
            )


if __name__ == "__main__":
    main()


