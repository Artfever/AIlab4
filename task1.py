# lab_eda_gui.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Configuration

st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Exploratory Data Analysis Interface")


# 2. Sidebar: Dataset Ingestion

#set header for sidebar
st.sidebar.header("Dataset Ingestion")

#create a file uploader in the sidebar for CSV files
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
   if not uploaded_file.name.lower().endswith(".csv"):
       st.error("Please upload a file with a .csv extension.")
       st.stop()

   # Read and validate the uploaded dataset.
   try:
       df = pd.read_csv(uploaded_file)
   except pd.errors.EmptyDataError:
       st.error("The uploaded CSV file is empty.")
       st.stop()
   except pd.errors.ParserError:
       st.error("The uploaded file is not a valid CSV.")
       st.stop()
   except UnicodeDecodeError:
       st.error("The CSV file must use UTF-8 text encoding.")
       st.stop()

   if df.empty or len(df.columns) == 0:
       st.error("The CSV file does not contain any data.")
       st.stop()

   # 3. Dataset Overview

   #set subheader for dataset overview
   st.subheader("Dataset Overview")
   st.write("**First 5 Rows:**")
   #display the first 5 rows of the dataset
   st.dataframe(df.head())

   #display the shape of the dataset
   st.write(f"**Shape:** {df.shape[0]} rows x {df.shape[1]} columns")
   st.write("**Column Data Types:**")
   #display the data types of each column in the dataset
   st.dataframe(df.dtypes.rename("Data Type"))

   # Missing value summary
   st.write("**Missing Values per Column:**")
   #display the count and percentage of missing values for each column in the dataset
   missing_values = pd.DataFrame(
       {
           "Missing Count": df.isna().sum(),
           "Missing Percentage": (df.isna().mean() * 100).round(2),
       }
   )
   st.dataframe(missing_values)

   # Basic statistics for numerical columns
   st.write("**Basic Numerical Statistics:**")
   numeric_columns = df.select_dtypes(include="number").columns
   if len(numeric_columns) > 0:
       numeric_summary = pd.DataFrame(
           {
               "Mean": df[numeric_columns].mean(),
               "Median": df[numeric_columns].median(),
               "Minimum": df[numeric_columns].min(),
               "Maximum": df[numeric_columns].max(),
           }
       )
       st.dataframe(numeric_summary)
   else:
       st.info("No numerical attributes are available for statistical summary.")

    
   # 4. Attribute Selection

   #set header for attribute selection in the sidebar
   #create a selectbox in the sidebar to choose an attribute for visualization
   st.sidebar.header("Attribute Selection")
   selected_column = st.sidebar.selectbox("Choose an attribute", df.columns)

   # Detect column type
   column_type = "Numerical" if pd.api.types.is_numeric_dtype(df[selected_column]) else "Categorical"
    
    
   # 5. Visualization Rendering

   st.subheader("Visualization")

   if column_type == "Numerical":
       # Histogram with seaborn
       fig, ax = plt.subplots()
       sns.histplot(df[selected_column].dropna(), kde=True, ax=ax)
       ax.set_title(f"Distribution of {selected_column}")
       ax.set_xlabel(selected_column)
       st.pyplot(fig)
   else:
       # Bar chart for categorical
       fig, ax = plt.subplots()
       value_counts = df[selected_column].value_counts(dropna=False).head(20)
       labels = value_counts.index.astype(str)
       sns.barplot(x=value_counts.values, y=labels, ax=ax)
       ax.set_title(f"Value Counts for {selected_column}")
       ax.set_xlabel("Count")
       ax.set_ylabel(selected_column)
       st.pyplot(fig)

else:
    st.info("Please upload a CSV file to start EDA.")
