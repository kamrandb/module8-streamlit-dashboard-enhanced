# 2024 AHI 507 Enhanced Streamlit Dashboard

## Description
This dashboard provides an interactive exploration of the 2020-2021 school learning modalities dataset released by the National Center for Education Statistics (NCES). The data covers learning modalities such as Hybrid, In Person, and Remote during the 2021 school year. Users can filter and analyze trends, visualize distributions, and gain insights into how schools adapted during this period.

---

## Deployed Dashboard URL
You can access the deployed Streamlit dashboard at:
[Insert Streamlit dashboard URL here]

---

## Changes from the Original Dashboard

### 1. **Expanded Data Limit**
- Original: Limited the dataset to the first 50,000 rows.
- Enhanced: Increased the limit to 500,000 rows for a broader analysis.

### 2. **Improved Data Cleaning**
- Added a safeguard to handle invalid dates in the `week` column by coercing errors.
- Removed commas from the `district_nces_id` column and ensured its datatype is consistent.

### 3. **Sidebar with Interactive Widgets**
- **Filters**:
  - Added a dropdown to filter data by district.
  - Added a slider to filter data by date range.
- **Download Button**:
  - Added a download button to export the filtered data as a CSV.

### 4. **Enhanced Metrics**
- Original: Displayed the number of columns, rows, and unique districts.
- Enhanced: Retained these metrics but improved layout and added functionality to update dynamically based on filtered data.

### 5. **Enhanced Data Preview**
- Original: Displayed the entire dataset.
- Enhanced: Limited the dataset preview to the first few rows for readability while maintaining filters.

### 6. **Improved Visualizations**
- Original:
  - Used `st.bar_chart` to show individual charts for Hybrid, In Person, and Remote modalities.
- Enhanced:
  - Combined all learning modalities into a single, interactive line chart to display trends over time.
  - Added pie charts and bar charts with gradient colors to display the distribution of students by modality and across weeks.

### 7. **Error Handling and Data Validation**
- Added checks to handle missing or filtered-out data, with warnings when no data is available for visualizations.
- Ensured pivot tables always include all learning modalities, filling missing values with zeros.

### 8. **User Interface Enhancements**
- Added spaces between widgets in the sidebar for better visual separation.
- Alphabetized or kept the original order of district names based on user requirements.

---

## Summary of Features
1. **Interactive Filtering**:
   - Filter data by district and week range.
2. **Dynamic Metrics**:
   - Automatically updates metrics based on filtered data.
3. **Download Option**:
   - Export the filtered dataset as a CSV file.
4. **Enhanced Visualizations**:
   - Line charts, bar charts, and pie charts to visualize data trends and distributions.
5. **Error Handling**:
   - Clear warnings for empty or missing data after filtering.

---

## How to Run the Dashboard Locally
1. Clone this repository:
   ```bash
   git clone [repository URL]
   ```
2. Navigate to the project folder:
   ```bash
   cd [project folder]
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run dashboard.py
   ```

---

## Data Source
This dashboard uses the 2020-2021 school learning modalities dataset provided by the National Center for Education Statistics (NCES):  
[https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data](https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data)

---

## Authors
Developed as part of the 2024 AHI 507 coursework.
Dr. Hants Williams - Created original streamlit app.
Kamran Butt - Modified and enhanced streamlit app as part of course assignment.