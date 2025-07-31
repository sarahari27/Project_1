# Project_1
SecureCheck: A Python-SQL Digital Ledger for Police Post Logs
SecureCheck is a real-time, interactive system for managing police check post data. This project aims to replace outdated manual logs with a digital solution built using Python, SQL, and Streamlit. It enables data-driven policing, real-time insights, and better public safety.

Problem Statement: Manual logging at police check posts leads to inefficiencies, poor data retrieval, and limited analytical insights. SecureCheck solves this by creating a centralized, SQL-based logging system with real-time data visualization and predictive insights.

💼 Business Use Cases:

⦁	Real-time vehicle and personnel logging.
⦁	Identifying high-risk violations or suspects.  
⦁	Check post efficiency monitoring through data analytics.  
⦁	Crime pattern analysis with Python scripts.  
⦁	Centralized access to check post records across regions.

Project Approach: Python for Data Processing, Database Design (SQL), Streamlit Dashboard.

🔧 Tech Stack:

⦁	Language: Python  
⦁	Database: PyMySQL / PostgreSQL  
⦁	Framework: Streamlit  
⦁	Libraries: pandas, sqlalchemy, pymysql  
⦁	Deployment: Streamlit Cloud or Localhost

SQL QUERIES :

1.	What are the top 10 vehicle_Number involved in drug-related stops?
2.	Which vehicles were most frequently searched?
3.	Which driver age group had the highest arrest rate?
4.	What is the gender distribution of drivers stopped in each country?
5.	Which race and gender combination has the highest search rate?
6.	What time of day sees the most traffic stops?
7.	What is the average stop duration for different violations?
8.	Are stops during the night more likely to lead to arrests?
9.	Which violations are most associated with searches or arrests?
10.	Which violations are most common among younger drivers (<25)?
11.	Is there a violation that rarely results in search or arrest?
12.	Which countries report the highest rate of drug-related stops?
13.	What is the arrest rate by country and violation?
14.	Which country has the most stops with search conducted?
15.	Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions).
16.	Driver Violation Trends Based on Age and Race (Join with Subquery).
17.	Time Period Analysis of Stops (Joining with Date Functions) , Number of Stops by Year,Month, Hour of the Day.
18.	Violations with High Search and Arrest Rates (Window Function).
19.	Driver Demographics by Country (Age, Gender, and Race).
20.	Top 5 Violations with Highest Arrest Rates.

Dataset Explanation:
1️⃣ stop_date – The date when the stop happened. 2️⃣ stop_time – The time of the stop. 3️⃣ country_name – The country where the stop took place. 4️⃣ driver_gender – The gender of the driver (Male or Female). 5️⃣ driver_age_raw – The recorded age of the driver (before cleaning). 6️⃣ driver_age – The actual age of the driver (after cleaning). 7️⃣ driver_race – The race/ethnicity of the driver. 8️⃣ violation_raw – The original reason for the stop (before cleaning). 9️⃣ violation – The type of violation (Speeding, DUI, etc.). 🔟 search_conducted – Whether the police searched the driver or vehicle (True/False). 1️⃣1️⃣ search_type – The type of search (Frisk, Vehicle Search, etc.). 1️⃣2️⃣ stop_outcome – The result of the stop (Warning, Citation, Arrest). 1️⃣3️⃣ is_arrested – Whether the driver was arrested (True/False). 1️⃣4️⃣ stop_duration – How long the stop lasted (<5 min, 6-15 min, etc.). 1️⃣5️⃣ drugs_related_stop – Whether the stop was drug-related (True/False).

Sample Insight: "A 27-year-old male was stopped for Speeding at 2:30 PM. No search conducted. He received a citation. The stop lasted 6–15 minutes and was not drug-related."

📂 Project Deliverables:

⦁	🗃️ SQL Schema & Database
⦁	🔁 Python ETL & Data Processing Scripts
⦁	📈 Streamlit Web Dashboard
⦁	🧾 README & Documentation 
⦁	
✅ Project Outcomes:

⦁	⚡ Faster check post logging and lookup
⦁	📊 Analytical insights for law enforcement
⦁	🧠 Predictive modeling for stop outcomes
⦁	🚨 Alert system for flagged vehicles
