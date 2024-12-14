import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NCES: School Learning Modalities Dashboard", layout="wide")

# -----------------------------------------------
# Header and Introduction
# -----------------------------------------------
st.title("HHA 507: 2024 Streamlit Dashboard - Enhanced")
st.markdown("""
This dashboard provides an overview of school learning modalities during 2021. The data is sourced from the National Center for Education Statistics (NCES).
Explore various visualizations and interact with widgets to analyze trends and distributions across different weeks, districts, and modalities.
""")

# -----------------------------------------------
# Load and Clean Data
# -----------------------------------------------
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=500000")  # Limit dataset to 500,000 records
df['week_recoded'] = pd.to_datetime(df['week'], errors='coerce')  # Ensure valid date parsing
df['zip_code'] = df['zip_code'].astype(str)

# Remove commas from 'district_nces_id' after converting it to string
df['district_nces_id'] = df['district_nces_id'].astype(str).str.replace(",", "")

# Drop invalid dates in 'week_recoded'
df = df.dropna(subset=['week_recoded'])

# Handle min/max values for the week slider
if len(df['week_recoded']) > 1:
    min_week = df['week_recoded'].min().date()
    max_week = df['week_recoded'].max().date()
else:
    min_week = max_week = df['week_recoded'].iloc[0].date()

# -----------------------------------------------
# Sidebar Widgets
# -----------------------------------------------
st.sidebar.header("Filters")

# Add space after header
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# District Selector
district_options = ["All"] + df['district_name'].dropna().unique().tolist()
selected_district = st.sidebar.selectbox("Select a District", options=district_options)

# Add space after district selector
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Week Range Slider
if min_week < max_week:
    selected_week = st.sidebar.slider(
        "Select Week Range",
        min_value=min_week,
        max_value=max_week,
        value=(min_week, max_week),
    )
else:
    st.sidebar.warning("Not enough data to display a range. Showing all available data.")
    selected_week = (min_week, max_week)

# Add space after week slider
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Download Button
@st.cache_data
def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(df)
st.sidebar.download_button(
    label="Download Data as CSV",
    data=csv_data,
    file_name="nces_2021_data.csv",
    mime="text/csv"
)

# -----------------------------------------------
# Filter Data Based on Sidebar Widgets
# -----------------------------------------------
filtered_df = df[
    (df['district_name'] == selected_district) if selected_district != "All" else True
    & (df['week_recoded'].dt.date >= selected_week[0])
    & (df['week_recoded'].dt.date <= selected_week[1])
]

# Rename 'week_recoded' to 'week' and drop the original week column
filtered_df = filtered_df.drop(columns=["week"]).rename(columns={"week_recoded": "week"})

# -----------------------------------------------
# Overview Metrics
# -----------------------------------------------
st.markdown("### Data Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rows", f"{len(filtered_df):,}")
col2.metric("Total Columns", f"{filtered_df.shape[1]:,}")
col3.metric("Unique Districts", f"{filtered_df['district_name'].nunique():,}")

# -----------------------------------------------
# Dataset Preview
# -----------------------------------------------
st.markdown("### Dataset Preview")
st.dataframe(filtered_df)

# -----------------------------------------------
# Summary Statistics
# -----------------------------------------------
st.markdown("### Summary Statistics")
if len(filtered_df) > 0:
    summary_stats = filtered_df[['operational_schools', 'student_count']].describe()
    st.write(summary_stats)
else:
    st.warning("No data available for the selected filters to display summary statistics.")

# -----------------------------------------------
# Visualizations
# -----------------------------------------------

# Pivot Table for Visualizations
expected_modalities = ["Hybrid", "In Person", "Remote"]
pivot_table = pd.pivot_table(
    filtered_df,
    values="student_count",
    index=["week"],
    columns=["learning_modality"],
    aggfunc="sum",
    fill_value=0  # Fill missing values with 0
).reset_index()

# Ensure all expected modalities are in the pivot table
for modality in expected_modalities:
    if modality not in pivot_table:
        pivot_table[modality] = 0

# Line Chart for Learning Modalities Over Time
if len(pivot_table) > 0:
    st.markdown("### Trends in Learning Modalities Over Time")
    line_fig = px.line(
        pivot_table,
        x="week",
        y=expected_modalities,  # Use all expected modalities
        labels={"value": "Student Count", "week": "Week"},
        title="Student Count by Learning Modality Over Time",
        color_discrete_sequence=px.colors.qualitative.Set1  # Use a variable color scheme
    )
    st.plotly_chart(line_fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters to generate the line chart.")

# Weekly Breakdown Bar Charts
st.markdown("### Weekly Distribution of Learning Modalities")
if len(pivot_table) > 0:
    for modality in expected_modalities:
        st.subheader(f"{modality} Modality")
        bar_fig = px.bar(
            pivot_table,
            x="week",
            y=modality,
            labels={"week": "Week", modality: "Student Count"},
            title=f"{modality} Student Count Over Time",
            color=modality,  # Use the y-axis value as the gradient variable
            color_continuous_scale="Blues",  # Apply a gradient color scale
        )
        st.plotly_chart(bar_fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters to generate bar charts.")