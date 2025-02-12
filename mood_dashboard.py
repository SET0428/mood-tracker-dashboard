import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import requests

# Notion API credentials
NOTION_API_KEY = "your_secret_key"
DATABASE_ID = "your_database_id"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Fetch data from Notion
def fetch_notion_data():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    data = response.json()
    return data

# Process Notion data into a DataFrame
def process_data(data):
    records = []
    for result in data["results"]:
        props = result["properties"]
        records.append({
            "Date": props["Date"]["date"]["start"],
            "Mood Rating": props["Mood Rating"]["number"],
            "Mood Category": props["Mood Category"]["select"]["name"],
            "Energy Level": props["Energy Level"]["select"]["name"],
        })
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    return df.sort_values(by="Date")

# Streamlit app setup
st.title("Mood Tracker Dashboard")

# Load data
data = fetch_notion_data()
df = process_data(data)

# Mood Trend Chart
st.subheader("Mood Trends Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=df['Date'], y=df['Mood Rating'], marker='o', ax=ax)
plt.axhline(y=df['Mood Rating'].mean(), color='r', linestyle='--', label='Average Mood')
plt.xlabel('Date')
plt.ylabel('Mood Rating (1-10)')
plt.legend()
st.pyplot(fig)

# Mood Category Distribution
st.subheader("Mood Distribution")
fig, ax = plt.subplots(figsize=(7, 5))
sns.countplot(y=df['Mood Category'], palette='viridis', ax=ax)
st.pyplot(fig)

# Energy vs. Mood
st.subheader("Energy Level vs. Mood")
fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(x=df['Energy Level'], y=df['Mood Rating'], palette='coolwarm', ax=ax)
st.pyplot(fig)

st.write("Data updated from Notion in real-time!")
