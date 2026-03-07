# 🌱 Smart Farming Data Lifecycle Project

## 📌 Project Overview

This project explores a **Smart Farming dataset** consisting of **16,411
records** that capture environmental conditions influencing irrigation
decisions.\
The analysis focuses on understanding relationships between soil
characteristics, crop growth stages, and environmental sensor readings.

The project also demonstrates a **complete data lifecycle workflow**,
starting from raw dataset acquisition to building an **interactive
analytics dashboard using Streamlit**.

------------------------------------------------------------------------

## 🎯 Project Goals

The main objectives of this project include:

-   Conducting **Exploratory Data Analysis (EDA)** to understand data
    patterns
-   Cleaning and validating the dataset to ensure data reliability
-   Evaluating **data quality metrics**
-   Building an **interactive visualization dashboard**
-   Deploying the dashboard to the cloud for public access

------------------------------------------------------------------------

## 📊 Dataset Description

  Feature          Description
  ---------------- ------------------------------------------
  crop_id          Unique identifier for each crop
  soil_type        Category of soil used for planting
  seedling_stage   Growth stage of the crop
  moi              Moisture Index from soil sensor
  temp             Temperature measurement (°C)
  humidity         Relative air humidity (%)
  result           Irrigation requirement (1 = Yes, 0 = No)

------------------------------------------------------------------------

## 🔄 Data Lifecycle Workflow

The project follows a structured **Data Lifecycle Management process**:

1.  **Data Collection** -- Obtaining the raw dataset from Kaggle\
2.  **Data Cleaning** -- Handling missing values and formatting
    variables\
3.  **Exploratory Data Analysis (EDA)** -- Investigating distributions
    and correlations\
4.  **Data Quality Evaluation** -- Measuring data reliability using
    quality metrics\
5.  **Dashboard Development** -- Creating an interactive dashboard with
    Streamlit

------------------------------------------------------------------------

## 📈 Dashboard Features

The dashboard presents several visual analytics components:

### 1️⃣ Irrigation Trend Over Time

A time-series visualization displaying irrigation demand patterns across
the dataset timeline.

### 2️⃣ Average MOI Gauge Indicator

A gauge chart showing the average **Moisture Index (MOI)**, representing
soil moisture conditions.

### 3️⃣ Irrigation Alert Heatmap

A heatmap visualization highlighting irrigation likelihood based on
**soil type and seedling stage**.

### 4️⃣ Temperature vs Irrigation Analysis

A boxplot comparing temperature distributions for crops that **require
irrigation vs those that do not**.

------------------------------------------------------------------------

## 🌐 Live Dashboard

You can access the deployed dashboard here:

👉
https://data-lifecycle-smart-farming-23082010156-xfykwbc7opfmhlrruphqj.streamlit.app/

------------------------------------------------------------------------

## 📂 Project Directory Structure

    repo_github/
    │
    ├── README.md
    │
    ├── data/
    │   └── raw/
    │       └── smart_agriculture_dataset.csv
    │
    ├── Data_Lifecycle_Smart_Farming.ipynb
    │
    ├── dashboard/
    │   └── streamlit_app.py
    │
    └── outputs/
        ├── cleaned_data.csv
        ├── analysis_report.pdf
        └── dashboard_screenshot.png

------------------------------------------------------------------------

## 🛠 Technology Stack

This project uses the following tools and libraries:

-   Python
-   Pandas
-   NumPy
-   Matplotlib
-   Seaborn
-   Plotly
-   Streamlit

------------------------------------------------------------------------

## 📊 Data Quality Evaluation

Several metrics are used to evaluate dataset quality:

-   **Accuracy** -- Ensuring values correctly represent real-world
    conditions\
-   **Completeness** -- Checking for missing or incomplete records\
-   **Timeliness** -- Verifying that data is relevant and usable\
-   **Overall Data Quality Score** -- Final quality assessment derived
    from the metrics

------------------------------------------------------------------------

## 🚀 Running the Project Locally

### 1️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 2️⃣ Launch the Streamlit Dashboard

``` bash
streamlit run dashboard/streamlit_app.py
```

------------------------------------------------------------------------

## 📄 Generated Outputs

The project produces several output artifacts:

-   **cleaned_data.csv** -- Processed dataset after cleaning
-   **analysis_report.pdf** -- Summary report of analysis
-   **dashboard_screenshot.png** -- Visual preview of the dashboard

------------------------------------------------------------------------

## 📄 License

This project is released under the **Apache 2.0 License**.

------------------------------------------------------------------------

## 👨‍💻 Author

**Mochamad Rafi Djaenal Pratama**\
Information Systems Student
