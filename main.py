import pymysql
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Create MySQL connection using pymysql
def create_connection():
    try:
        sp = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="SECURECHECK",
            cursorclass=pymysql.cursors.DictCursor  # So we get column names
        )
        return sp
    except pymysql.MySQLError as e:
        st.error(f"Connection Error: {e}")
        return None

# Fetch data from the database using function
def fetch_data(query):
    sp = create_connection()
    if sp:
        try:
            with sp.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
                df = pd.DataFrame(data)
                return df
        finally:
            sp.close()
    else:
        return pd.DataFrame()


print("All packages loaded successfully!")

# # Streamlit UI
# # snow animation
st.snow()

# # Streamlit App Title

st.set_page_config(page_title="🚓 SecureCheck: Police Post Logs", layout="wide")
st.title("🚓 SecureCheck: Police Post Log Ledger")

# Sidebar Menu

menu = st.sidebar.selectbox("Go to", ["Home","Data Analytics & Visuals","View Logs","Predict Logs"])

# Home Page

if menu == "Home":
    st.subheader("👋 Welcome to **SecureCheck**")
    st.markdown("""
    🔐 **SecureCheck** is a data-driven platform built for evaluating traffic stop outcomes and trends.  
    Here's what you can do:
    - 📊 View detailed traffic stop records
    - 🚗 Analyze violation patterns by category
    - ⏱️ Review stop durations and officer performance
    - 📍 Visualize trends over time and location
    """)
    st.success("Let's make policing smarter and safer! 🚓")

   

    st.header("📋Police Logs Overview")
    query="select * from securecheck.logs"
    data=fetch_data(query)
    st.dataframe(data,use_container_width=True)
    st.markdown("---")  
    st.subheader("📝 Description")
    st.markdown("""
    The table above showcases daily police log records, including incident types, dates, and locations.
    - **Traffic Violation**: Involves offenses like speeding, illegal parking, or reckless driving.
    - **Theft**: Incidents related to stolen property, burglary, or unauthorized access.
    """)
    st.write("Analyzing this data helps identify areas with frequent incidents and peak hours, supporting smarter police response strategies.")
    st.markdown("---")  

 # Data Analytics and Visuals

elif menu=='Data Analytics & Visuals':

    # Quick Metrics

    query="select * from securecheck.logs"
    data=fetch_data(query)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_stops=data.shape[0]
        st.metric("🚓 Total Police Stops", total_stops)

    with col2:
            
        arrests = data[data["stop_outcome"].str.contains("arrest", case=False, na=False)].shape[0]
        st.metric("🚨 Total Arrests", arrests)

    with col3:
        warnings = data[data["stop_outcome"].str.contains("Warning", case=False, na=False)].shape[0]
        st.metric("⚠️ Total Warnings", warnings)

    with col4:
        drug_stop = data[data["drugs_related_stop"] == 1].shape[0]
        st.metric("💊 Drug Related Stops", drug_stop)

 # Data Visulaization 

    st.header("📊 Visual Insights")      
    tab= st.tabs(['Stops By Violations', 'Driver Gender Distribution', 'Drug-Related Stops by Country'])
    
    with tab[0]:
    # SQL Query to fetch violation count

        query = "SELECT violation, COUNT(violation) AS counts FROM securecheck.logs GROUP BY violation"
        data = fetch_data(query)

        st.subheader("Violation Breakdown (Pie Chart)")
        st.dataframe(data)

    # Plot pie chart using Plotly
        fig = px.pie(data, names='violation', values='counts',
                    color_discrete_sequence=px.colors.sequential.RdPu,
                    title='Violation Distribution')
        st.plotly_chart(fig, use_container_width=True)

    

    with tab[1]:
         
    # SQL Query to fetch Gender of Driver and its counts
         
         st.subheader("Driver Gender Distribution (Donut chart)")
         query="select driver_gender, count(*) as count from securecheck.logs group by driver_gender"
         data=fetch_data(query)
         st.dataframe(data)


         # Donut chart using Plotly
         fig = px.pie(
            data,
            names='driver_gender',
            values='count',
            hole=0.5,  # This creates the "donut" hole
            title="Gender Breakdown of Drivers"
         )

         st.plotly_chart(fig, use_container_width=True)

    
    with tab[2]:
        # SQL Query to fetch Drug-Related Stops by Country

         st.subheader("Drug-Related Stops by Country(Stacked Bar Chart)")
         query = "SELECT country_name, drugs_related_stop, count(*) as count from securecheck.logs group by country_name, drugs_related_stop"
         data = fetch_data(query)
         st.dataframe(data)
     
         # Stacked Bar chart using Plotly
         fig = px.bar(
             data,
             x='country_name',
             y='count',
             color='drugs_related_stop',
             barmode='stack',
             labels={
                 'count': 'Number of Stops',
                 'country_name': 'Country',
                 'drugs_related_stop': 'Drugs Related'
             },
             title="Stacked: Drug-Related Stops by Country"
         )
         st.plotly_chart(fig, use_container_width=True)

# View Logs

elif menu=='View Logs':

    st.header("🧠 Advanced Insights")   
    st.subheader("📋 View Vehicle Logs with Filters")

    # Search filters in sidebar or main page
    st.write("Use the filters below to narrow down logs:")

    vehicle_input = st.text_input("🔍 Search by Vehicle Number")
    violation_input = st.text_input("🔍 Search by Violation")
    country_input = st.text_input("🌍 Search by Country")

    # Base query
    query = "SELECT * FROM securecheck.logs WHERE 1=1"

    # Dynamically add filters
    if vehicle_input:
        query += f" AND vehicle_number LIKE '%{vehicle_input}%'"

    if violation_input:
        query += f" AND violation LIKE '%{violation_input}%'"

    if country_input:
        query += f" AND country_name LIKE '%{country_input}%'"

    # # Fetch & show
    df = fetch_data(query)

    if not df.empty:
        if 'stop_time' in df.columns:
            df['stop_time'] = df['stop_time'].apply(lambda x: str(x).split()[-1] if pd.notnull(x) else '')

        
        st.success(f"✅ Showing {len(df)} matching logs")
        st.dataframe(df)
    else:
        st.warning("⚠️ No matching logs found.")
    
    st.markdown("---")  

    analysis_option = st.selectbox(
        "Choose 🚗 Vehicle/🧍Demographic/ 🕒 Time & Duration/ ⚖️ Violation-Based analysis to run:",
        [
            "Top 10 vehicle_Number involved in Drug-Related Stops",
            "Most Frequently Searched Vehicles",
            "Driver Age Group with Highest Arrest Rate",
            "Gender Distribution of Drivers Stopped in each Country",
            "Race & Gender Combination with Highest Search Rate",
            "Time of Day with Most Traffic Stops",
            "Average Stop Duration for different Violations",
            "Night Stops More Likely to Lead to Arrests",
            "Violations Most Associated with Searches or Arrests",
            "Most Common Violations for Young Drivers Under 25",
            "Violation Rarely Resulting in Search or Arrest",
            "Countries Report with Highest Drug-Related Stop Rates",
            "Arrest Rate by Country & Violation",
            "Country has the Most Stops with Search Conducted",
            "Yearly Breakdown of Stops and Arrests by Country",
            "Driver Violation Trends by Age & Race",
            "Time Period Analysis of Stops, Number of Stops by Year, Month, Hour of the Day",
            "Violations with High Search & Arrest Rates",
            "Driver Demographics by Country (Age, Gender and Race)",
            "Top 5 Violations with Highest Arrest Rates"
        ]
    )

    query_map = {
        "Top 10 vehicle_Number involved in Drug-Related Stops": """SELECT vehicle_number, COUNT(*) as COUNT
                                                                  FROM securecheck.logs WHERE drugs_related_stop = 'TRUE'
                                                                  GROUP BY vehicle_number
                                                                  ORDER BY COUNT DESC
                                                                  LIMIT 10""",

        "Most Frequently Searched Vehicles": """SELECT vehicle_number, COUNT(*) AS search_count
                                               FROM securecheck.logs
                                               GROUP BY vehicle_number
                                               ORDER BY vehicle_number DESC LIMIT 10""",
        
        "Driver Age Group with Highest Arrest Rate" : """SELECT CASE
                                                        when driver_age between 18 and 25 then '18-25'
                                                        when driver_age between 26 and 35 then '26-35'
                                                        when driver_age between 36 and 45 then '36-45'
                                                        when driver_age between 45 and 60 then '45-60'
                                                        else '60+'
                                                        end AS age_group,COUNT(*) AS total_driver,
                                                        sum(case when is_arrested=1 then 1 else 0 end) AS total_arrests,
                                                        round(sum(case when is_arrested=1 then 1 else 0 end)*100.0/count(*),2) AS arrest_rate_percent 
                                                        from securecheck.logs GROUP BY age_group
                                                        ORDER BY arrest_rate_percent desc limit 1
                                                        """,
                                            
        "Gender Distribution of Drivers Stopped in each Country" :"""SELECT country_name, driver_gender, COUNT(*) AS total_gender,
                                                                    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY country_name), 2) AS gender_percent
                                                                    FROM securecheck.logs
                                                                    GROUP BY country_name, driver_gender
                                                                    ORDER BY country_name, driver_gender""",

        "Race & Gender Combination with Highest Search Rate" :"""SELECT driver_race, driver_gender, COUNT(*) AS total_stops,
                                                                 SUM(CASE WHEN search_conducted  = 1 THEN 1 ELSE 0 END) AS total_searches,
                                                                 ROUND(SUM(CASE WHEN search_conducted  = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS search_percent_rate
                                                                 FROM securecheck.logs
                                                                 WHERE driver_race IS NOT NULL AND driver_gender IS NOT NULL
                                                                 GROUP BY driver_race, driver_gender
                                                                 ORDER BY search_percent_rate DESC LIMIT 1""",

       "Time of Day with Most Traffic Stops" :"""SELECT HOUR(stop_time) AS stop_hour, COUNT(*) AS total_stops
                                                FROM securecheck.logs
                                                WHERE stop_time IS NOT NULL
                                                GROUP BY stop_hour 
                                                ORDER BY total_stops DESC LIMIT 1""",

       "Average Stop Duration for different Violations" : """SELECT violation,
                                                            AVG(stop_duration) AS average_stop_duration
                                                            FROM securecheck.logs
                                                            WHERE stop_duration IS NOT NULL 
                                                            GROUP BY violation ORDER BY Average_stop_duration DESC""",

        "Night Stops More Likely to Lead to Arrests" : """SELECT 
                                                         CASE
                                                         WHEN HOUR(stop_time) BETWEEN 20 AND 23 OR HOUR(stop_time) BETWEEN 0 AND 5 THEN 'Night'
                                                         ELSE 'Day'
                                                         END AS time_of_day,
                                                         COUNT(*) AS total_stops,
                                                         SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests,
                                                         ROUND(SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate_percent
                                                         FROM securecheck.logs
                                                         WHERE stop_time IS NOT NULL
                                                         GROUP BY time_of_day
                                                         ORDER BY arrest_rate_percent DESC""",

        "Violations Most Associated with Searches or Arrests" :"""SELECT violation,
                                                                 COUNT(*) AS total_stops,
                                                                 SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests, 
                                                                 SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_searches, 
                                                                 SUM(CASE WHEN is_arrested = 1 OR search_conducted = TRUE THEN 1 ELSE 0 END) AS search_or_arrest_total
                                                                 FROM securecheck.logs
                                                                 GROUP BY violation
                                                                 ORDER BY search_or_arrest_total DESC LIMIT 10""",
      
        "Most Common Violations for Young Drivers Under 25" :"""SELECT violation,
                                                               COUNT(*) AS total_stops
                                                               FROM securecheck.logs
                                                               WHERE driver_age < 25
                                                               GROUP BY violation
                                                               ORDER BY total_stops DESC LIMIT 10""",

        "Violation Rarely Resulting in Search or Arrest" :"""SELECT violation,
                                                            COUNT(*) AS total_stops,
                                                            SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests
                                                            FROM securecheck.logs
                                                            GROUP BY violation
                                                            ORDER BY total_arrests ASC LIMIT 1""",
                                                               
        "Countries Report with Highest Drug-Related Stop Rates" :"""SELECT country_name,
                                                                   COUNT(*) AS total_stops,
                                                                   SUM(CASE WHEN drugs_related_stop = 1 THEN 1 ELSE 0 END) AS drug_related_stops,
                                                                   ROUND(SUM(CASE WHEN drugs_related_stop = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS drug_stop_rate_percent
                                                                   FROM securecheck.logs
                                                                   GROUP BY country_name
                                                                   ORDER BY drug_stop_rate_percent DESC""",

       "Arrest Rate by Country & Violation" :"""SELECT country_name,
                                               COUNT(*) AS total_stops,
                                               violation,
                                               SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests,
                                               ROUND(100.0 * SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS total_arrest_percent
                                               FROM securecheck.logs
                                               GROUP BY country_name, violation
                                               ORDER BY country_name""",
 
        "Country has the Most Stops with Search Conducted" :"""select country_name, count(*) as total_stops
                                                              from securecheck.logs
                                                              group by country_name
                                                              order by total_stops
                                                              desc limit 1""",

        "Yearly Breakdown of Stops and Arrests by Country" :"""SELECT country_name,
                                                              EXTRACT(YEAR FROM stop_date) AS year,
                                                              total_stops, total_arrests, 
                                                              ROUND(100.0 * total_arrests / total_stops, 2) AS arrest_rate_percent,
                                                              RANK() OVER (PARTITION BY year ORDER BY total_arrests DESC) AS arrest_rank_in_year

                                                              FROM (SELECT country_name, stop_date, 
                                                              COUNT(*) AS total_stops,
                                                              SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests
                                                              FROM securecheck.logs
                                                              WHERE stop_date IS NOT NULL
                                                              GROUP BY country_name, EXTRACT(YEAR FROM stop_date)) AS yearly_stats""" , 

        "Driver Violation Trends by Age & Race" :"""WITH age_groups AS (SELECT id,
                                                   CASE
                                                   WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                                                   WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
                                                   WHEN driver_age BETWEEN 36 AND 50 THEN '36-50'
                                                   ELSE '51+'
                                                   END AS age_group,
                                                   driver_race
                                                   FROM securecheck.logs
                                                   WHERE driver_age IS NOT NULL AND driver_race IS NOT NULL)

                                                   SELECT 
                                                   ag.age_group, ag.driver_race, l.violation, COUNT(*) AS total_violations
                                                   FROM securecheck.logs l
                                                   JOIN age_groups ag ON l.id = ag.id
                                                   WHERE l.violation IS NOT NULL
                                                   GROUP BY ag.age_group, ag.driver_race, l.violation
                                                   ORDER BY ag.age_group, ag.driver_race, total_violations DESC""",

        "Time Period Analysis of Stops, Number of Stops by Year, Month, Hour of the Day" :"""SELECT
                                                                                            EXTRACT(YEAR FROM stop_date) AS year,
                                                                                            EXTRACT(MONTH FROM stop_date) AS month, 
                                                                                            EXTRACT(HOUR FROM stop_time) AS hour,
                                                                                            COUNT(*) AS total_stops 
                                                                                            FROM securecheck.logs
                                                                                            WHERE stop_date IS NOT NULL AND stop_time IS NOT NULL
                                                                                            GROUP BY year, month, hour
                                                                                            ORDER BY year, month, hour""",  

       "Violations with High Search & Arrest Rates" :"""SELECT violation,
                                                       COUNT(*) AS total_stops,
                                                       SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) AS total_searches,
                                                       SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests,
                                                       ROUND(100.0 * SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate_percent,
                                                       ROUND(100.0 * SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_percent_rate,
                                                       RANK() OVER (ORDER BY SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) DESC) AS search_rank,
                                                       RANK() OVER (ORDER BY SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) DESC) AS arrest_rank
                                                       FROM securecheck.logs
                                                       WHERE violation IS NOT NULL
                                                       GROUP BY violation
                                                       ORDER BY search_rate_percent DESC, arrest_percent_rate DESC""",

        "Driver Demographics by Country (Age, Gender and Race)" :"""SELECT country_name, driver_gender, driver_race,
                                                                   CASE 
                                                                   WHEN driver_age < 20 THEN '<20'
                                                                   WHEN driver_age BETWEEN 20 AND 29 THEN '20-29'
                                                                   WHEN driver_age BETWEEN 30 AND 39 THEN '30-39'
                                                                   WHEN driver_age BETWEEN 40 AND 49 THEN '40-49'
                                                                   WHEN driver_age BETWEEN 50 AND 59 THEN '50-59'
                                                                   ELSE '60+'
                                                                   END AS age_group,
                                                                   COUNT(*) AS total_drivers
                                                                   FROM securecheck.logs
                                                                   WHERE driver_age IS NOT NULL 
                                                                   AND driver_gender IS NOT NULL 
                                                                   AND driver_race IS NOT NULL
                                                                   GROUP BY country_name, driver_gender, driver_race, age_group
                                                                   ORDER BY country_name, driver_gender, driver_race, age_group""",      

        "Top 5 Violations with Highest Arrest Rates" :"""SELECT violation,
                                                        COUNT(*) AS total_stops,
                                                        SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests,
                                                        ROUND(100.0 * SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS arrest_rate_percent
                                                        FROM securecheck.logs
                                                        WHERE is_arrested IS NOT NULL AND violation IS NOT NULL
                                                        GROUP BY violation
                                                        
                                                        ORDER BY arrest_rate_percent DESC LIMIT 5"""

    }
    
    result = pd.DataFrame()
    
    if st.button("Run Analysis"):
        query = query_map.get(analysis_option)
    if query:
        result = fetch_data(query)

     # Display result
    if not result.empty:
        st.write(result)
    else:
        st.warning("No Results Found")

    st.markdown("---") 
    # Predict Logs

elif menu=="Predict Logs":
               
            query="select * from securecheck.logs"
            data=fetch_data(query)
            st.markdown("---")
            st.markdown("Designed by SecureCheck to empower law enforcement efforts.")
            st.header("🔍 Custom Natural Language Filter")
            st.markdown("Use natural language to filter past police stops and analyze trends.")
            st.subheader("📝 Log a New Police Stop and Generate Outcome & Violation Prediction")
            st.markdown("Fill in the following details to log a new stop and predict likely outcomes and violations.")


            # Input Form

            with st.form("New_Log_Form"):
                
                vehicle_number=st.text_input("🚗 Vehicle Number")
                stop_date=st.date_input("📅 Stop Date")
                stop_time=st.time_input("⏰ Stop Time")
                country_name=st.selectbox("🌍 Country Name", ["Canada", "USA", "India"])                
                driver_age=st.number_input("👨‍✈️ Driver Age", min_value=16, max_value=100, value=20)
                driver_race=st.selectbox("👤 Driver Race", ["Asian", "Black", "White", "Hispanic", "Other"])
                search_type=st.selectbox("📝 Search Type", ["Vehicle Search", "Frisk", "None"])
                stop_duration=st.selectbox("⏱️ Stop Duration",data["stop_duration"].dropna().unique())
                driver_gender=st.radio("🚻 Driver Gender",["Male","Female"])
                st.write(driver_gender)
                drugs_related_stop=st.radio("💊 Drug Related?",["0","1"])
                st.write(drugs_related_stop)
                search_conducted=st.radio("🔎 Search Conducted?", ["0","1"])
                st.write(drugs_related_stop)
                submitted=st.form_submit_button("✅ Predict Stop Outcome & Violation")

                
            if submitted:
                filtered_data=data[
                    (data["driver_gender"]== driver_gender)&
                    (data["driver_age"]== driver_age)&
                    (data["search_conducted"]==int(search_conducted))&
                    (data["stop_duration"]==stop_duration)&
                    (data["drugs_related_stop"]==drugs_related_stop)
                ]
         # Predict Stop_Outcome

                if not filtered_data.empty:
                    predicted_outcome=filtered_data["stop_outcome"].mode()[0]
                    predicted_violation=filtered_data["violation"].mode()[0]
                else:
                    predicted_outcome="Warning"  # Default
                    predicted_violation="Speeding" # Default

         # Natural Language Summary

                search_text="A search was conducted" if int(search_conducted) else "No search was conducted"
                drug_text="Was Drug related" if int(drugs_related_stop) else "was not Drug related"
                st.markdown("---")  
                st.subheader("🚓 ** Prediction Summary**")

                st.markdown(f"""
                        
                         -  **Vehicle Number:** {vehicle_number}                
                         -  **Predicted Violation:** {predicted_violation}
                         -  **Predicted Stop Outcome:** {predicted_outcome}
                         -  **Stop Duration:** {stop_duration}

                            📝 A **{driver_age}**-year-old **{driver_gender}** driver in **{country_name}** was stopped for **{predicted_violation}** at {stop_time.strftime('%I:%M %p')} on {stop_date}.
                            **{search_text}**, received a **{predicted_outcome}** and **{drug_text}**.
                            """ )        
                st.markdown("---")  

    