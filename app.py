import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_diagnosis(vehicle_data, telemetry_summary):

    prompt = f"""
You are an AI-powered vehicle diagnostics assistant.

Analyze the following telemetry data and provide:

1. Vehicle Health Status
2. Critical Issues (if any)
3. Severity Level (Low / Medium / High)
4. Likely Causes
5. Recommended Actions

Telemetry Data:
- Speed: {vehicle_data['speed']} km/h
- RPM: {vehicle_data['rpm']}
- Engine Temperature: {vehicle_data['engine_temp']} °C
- Battery Voltage: {vehicle_data['battery_voltage']} V
- Fuel Level: {vehicle_data['fuel_level']} %
- Oil Pressure: {vehicle_data['oil_pressure']}
- Throttle Position: {vehicle_data['throttle_position']}

Detected Anomalies:
{anomalies}

Predictive Maintenance Warnings:
{predictive_warnings}

Telemetry Summary:
- Average Engine Temperature: {telemetry_summary['avg_engine_temp']}
- Maximum Engine Temperature: {telemetry_summary['max_engine_temp']}
- Average Battery Voltage: {telemetry_summary['avg_battery_voltage']}
- Minimum Battery Voltage: {telemetry_summary['min_battery_voltage']}
- Average RPM: {telemetry_summary['avg_rpm']}
- Maximum RPM: {telemetry_summary['max_rpm']}

Keep the response short,concise, technical, and structured like an automotive monitoring system.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an intelligent automotive diagnostics assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content




data = pd.read_csv("data/vehicle_data.csv")

telemetry_summary = {
    "avg_engine_temp": data['engine_temp'].mean(),
    "max_engine_temp": data['engine_temp'].max(),
    "avg_battery_voltage": data['battery_voltage'].mean(),
    "min_battery_voltage": data['battery_voltage'].min(),
    "avg_rpm": data['rpm'].mean(),
    "max_rpm": data['rpm'].max()
}



st.title("AI-Based Vehicle Health Monitoring and Alert System")
page = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "AI Diagnostics",
        "Telemetry Trends",
        "Predictive Insights",
        "About Project"
    ]
)

####### Dashboard Page



######## Live Vehicle Status
if page == "Dashboard":
  st.subheader("Vehicle Telemetry Data")

  st.dataframe(data)
  latest = data.iloc[-1]

  st.subheader("Live Vehicle Status")

  col1, col2, col3 = st.columns(3)

  col1.metric("Speed", f"{latest['speed']} km/h")
  col2.metric("RPM", latest['rpm'])
  col3.metric("Engine Temp", f"{latest['engine_temp']} °C")

  col4, col5, col6 = st.columns(3)

  col4.metric("Battery Voltage", f"{latest['battery_voltage']} V")
  col5.metric("Fuel Level", f"{latest['fuel_level']} %")
  col6.metric("Oil Pressure", latest['oil_pressure'])

#Add Anomaly Detection Logic
latest = data.iloc[-1]
anomalies = []

if latest['engine_temp'] > 110:
    anomalies.append(("High Engine Temperature", "High"))

elif latest['engine_temp'] > 100:
    anomalies.append(("High Engine Temperature", "Medium"))

if latest['battery_voltage'] < 11.8:
    anomalies.append(("Low Battery Voltage", "High"))

elif latest['battery_voltage'] < 12.2:
    anomalies.append(("Low Battery Voltage", "Medium"))

if latest['rpm'] > 4000:
    anomalies.append(("Critical RPM Spike", "High"))

elif latest['rpm'] > 3500:
    anomalies.append(("High RPM Spike", "Medium"))

predictive_warnings = []
#######
if page == "Dashboard":

  if data['engine_temp'].iloc[-1] > data['engine_temp'].mean() + 10:
      predictive_warnings.append(
          "Engine temperature trend indicates potential overheating risk."
      )
  if data['battery_voltage'].iloc[-1] < data['battery_voltage'].mean() - 0.3:
      predictive_warnings.append(
          "Battery voltage trend indicates possible battery degradation."
      )
  if data['rpm'].std() > 500:
      predictive_warnings.append(
          "RPM instability detected. Possible engine performance irregularity."
      )


if page == "Dashboard":
  st.subheader("System Alerts")

  if anomalies:

      for anomaly, severity in anomalies:

          if severity == "High":
              st.error(f"🔴 {anomaly} | Severity: {severity}")

          elif severity == "Medium":
              st.warning(f"🟠 {anomaly} | Severity: {severity}")

          else:
              st.info(f"🟡 {anomaly} | Severity: {severity}")

  else:
      st.success("✅ No anomalies detected")

health_score = 100
####### AI Diagnostic Analysis
if page == "AI Diagnostics":
  st.subheader("AI Diagnostic Analysis")

  if anomalies:

      if st.button("Generate AI Diagnosis"):

          ai_response = generate_ai_diagnosis(latest, telemetry_summary)

          st.write(ai_response)

######## Vehicle Health Score Calculation
if page == "Dashboard":
  st.subheader("Vehicle Health Score")
  for anomaly, severity in anomalies:

      if severity == "High":
          health_score -= 30

      elif severity == "Medium":
          health_score -= 15

      else:
          health_score -= 5

  health_score = max(0, health_score)



if health_score >= 90:
    system_status = "Healthy"
    print(system_status)

elif health_score >= 70:
    system_status = "Warning"
    print(system_status)

else:
    system_status = "Critical"
    print(system_status)


############ Telemetry Trends Visualization
if page == "Telemetry Trends":
    st.subheader("Vehicle Telemetry Trends")

    st.line_chart(data[['speed', 'engine_temp']])

    st.line_chart(data[['rpm']])


if page == "Dashboard":
  st.subheader("Overall Vehicle Condition")

  if system_status == "Healthy":
      st.success(f" System Status: {system_status}")

  elif system_status == "Warning":
      st.warning(f" System Status: {system_status}")

  else:
      st.error(f" System Status: {system_status}")

  if page == "Predictive Insights":
    st.subheader("Predictive Maintenance Insights")

    if predictive_warnings:

        for warning in predictive_warnings:
            st.warning(f"🔮 {warning}")

    else:
        st.success("✅ No predictive maintenance risks detected")

if page == "About Project":

    st.title("About Project")

    st.write(
        '''
        This project is an AI-powered vehicle health monitoring and alert system
        designed to analyze telemetry data, detect anomalies,
        evaluate vehicle health, and generate predictive maintenance insights.
        '''
    )

    st.subheader("Technologies Used")

    st.write("""
    - Python
    - Streamlit
    - OpenAI API
    - Pandas
    """)



report = f"""
AI-Based Vehicle Health Monitoring Report

====================================

Vehicle Health Score: {health_score}/100

System Status:
{system_status}

Detected Anomalies:
{anomalies}

Predictive Maintenance Warnings:
{predictive_warnings}
"""

st.download_button(
    label="📥 Download Diagnostic Report",
    data=report,
    file_name="vehicle_diagnostic_report.txt",
    mime="text/plain"
)