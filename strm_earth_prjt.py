import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:Vasanth%4022@localhost:3306/earth_quarke_project"
)
st.set_page_config(
    page_title="Global Seismic Trends",
    layout="wide"
)
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.block-container {
    border: 2px solid #3b82f6;
    border-radius: 15px;
    padding: 2rem;
    margin-top: 1rem;
    background-color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center;'>🌍 Global Seismic Trends</h1>",
    unsafe_allow_html=True
)
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Earthquakes", "114,535")
col2.metric("Highest Magnitude", "8.8")
col3.metric("Tsunamis", "659")
col4.metric("Average Depth", "200 km")
st.divider()


st.markdown("---")
def show_question(question, query, key):

    st.markdown(f"### {question}")

    if st.button("Show Answer", key=key):

        df = pd.read_sql(query, engine)

        st.dataframe(df, use_container_width=True)

    st.markdown("---")

questions = {

"1. Top 10 strongest earthquakes (mag).":
"""
SELECT id, country, mag, depth_km, time
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;
""",
"2.Top 10 deepest earthquakes (depth_km).":
 """
SELECT id, country, depth_km, mag
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;
""",
"3. Shallow earthquakes < 50 km and mag > 7.5.":
 """
SELECT id,  country, mag, depth_km
FROM earthquakes
WHERE depth_km < 50
AND mag > 7.5;
""",
"5. Average magnitude per magnitude type (magType).":
 """
SELECT magType,
ROUND(AVG(mag),2) AS avg_magnitude
FROM earthquakes
GROUP BY magType
ORDER BY avg_magnitude DESC;
""",
"6. Year with most earthquakes.": 
 """
SELECT year,
COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY year
ORDER BY total_earthquakes DESC;
""",
"7. Month with highest earthquakes.":
"""
SELECT month_name,
COUNT(*) AS total
FROM earthquakes
GROUP BY month_name
ORDER BY total DESC;
""",
"8. Day of week with most earthquakes.":
"""
SELECT day_name,
COUNT(*) AS total
FROM earthquakes
GROUP BY day_name
ORDER BY total DESC;
""",
"9. Earthquakes per hour.":
"""
SELECT hour,
COUNT(*) AS total
FROM earthquakes
GROUP BY hour
ORDER BY hour;
""",
"10.   Most active reporting network (net).":
"""
SELECT net,
COUNT(*) AS total_events
FROM earthquakes
GROUP BY net
ORDER BY total_events DESC;
""",
"14.  Count of reviewed vs automatic earthquakes (status).":
"""
SELECT status,
COUNT(*) AS total
FROM earthquakes
GROUP BY status;
""",
"15.  Count by earthquake type (type).":
"""
SELECT type,
COUNT(*) AS total
FROM earthquakes
GROUP BY type;
""",
"16.  Number of earthquakes by data type (types).":
"""
SELECT types,
COUNT(*) AS total
FROM earthquakes
GROUP BY types
ORDER BY total DESC;
""",
"18.  Events with high station coverage (nst > threshold).":
"""
SELECT id,

country,
nst,
mag
FROM earthquakes
WHERE nst > 100
ORDER BY nst DESC;
""",
"19.  Number of tsunamis triggered per year.":
"""
SELECT year,
COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami = 1
GROUP BY year
ORDER BY year;
""",
"20.  Count earthquakes by alert levels (red, orange, etc.).":
"""
SELECT alert,
COUNT(*) AS total
FROM earthquakes
GROUP BY alert;
""",
"21.Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years.":
"""
SELECT country,
ROUND(AVG(mag),2) AS avg_mag
FROM earthquakes
WHERE year >= YEAR(CURDATE())-5
GROUP BY country
ORDER BY avg_mag DESC
LIMIT 5;
""",
"22.Find countries that have experienced both shallow and deep earthquakes within the same month.":
"""
SELECT country,
year,
month_name
FROM earthquakes
GROUP BY country, year, month_name
HAVING
SUM(depth_km < 70) > 0
AND
SUM(depth_km > 300) > 0;
""",
"23.Compute the year-over-year growth rate in the total number of earthquakes globally.":
"""
SELECT
year,
COUNT(*) AS total_events,
LAG(COUNT(*)) OVER(ORDER BY year) AS previous_year
FROM earthquakes
GROUP BY year;
""",
"24. List the 3 most seismically active regions by combining both frequency and average magnitude.":
"""
SELECT
    country,
    COUNT(*) AS total_earthquakes,
    ROUND(AVG(mag), 2) AS avg_magnitude
FROM earthquakes
GROUP BY country
ORDER BY total_earthquakes DESC, avg_magnitude DESC
LIMIT 3;
""",
"25. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.":
"""
SELECT
    country,
    COUNT(*) AS total_earthquakes,
    ROUND(AVG(depth_km), 2) AS avg_depth_km
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country
ORDER BY avg_depth_km DESC;
""",
"26. Identify countries having the highest ratio of shallow to deep earthquakes.":
"""
SELECT
    country,
    SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) AS shallow_eq,
    SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END) AS deep_eq,
    ROUND(
        SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) /
        NULLIF(SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END), 0),
        2
    ) AS shallow_deep_ratio
FROM earthquakes
GROUP BY country
HAVING deep_eq > 0
ORDER BY shallow_deep_ratio DESC;
""",
"27. Find the average magnitude difference between earthquakes with tsunami alerts and those without.":
"""
SELECT tsunami_label,
ROUND(AVG(mag),2) AS avg_mag
FROM earthquakes
GROUP BY tsunami_label;
""",
"28. Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins).":
"""
SELECT id,

gap,
rms,
(gap+rms) AS error_margin
FROM earthquakes
ORDER BY error_margin DESC
LIMIT 10;
""",
"30. Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km).":
"""
SELECT
    country,
    COUNT(*) AS deep_focus_earthquakes
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
ORDER BY deep_focus_earthquakes DESC;
"""


}
for i, (question, query) in enumerate(questions.items()):

    st.markdown(f"## {question}")

    if st.button("Show Answer", key=i):

        result = pd.read_sql(query, engine)

        st.dataframe(result, use_container_width=True)

        st.download_button(
            "⬇ Download CSV",
            result.to_csv(index=False),
            file_name=f"Question_{i+1}.csv",
            mime="text/csv",
            key=f"download{i}"
        )

    st.divider()