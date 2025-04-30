# 📊 Instagram Trend Analysis

This project delves into analyzing a large-scale Instagram dataset to uncover patterns in user behavior, focusing on location-based posting trends. By leveraging both relational (PostgreSQL) and NoSQL (MongoDB) databases, the project processes and analyzes millions of Instagram posts, user profiles, and location data.

---

## 🧰 Tech Stack

- **Databases**: PostgreSQL, MongoDB
- **Languages**: SQL, Python
- **Libraries**: pandas, pymongo, itertools

---

[!InstagramAnalysis](/inst.png)

## 🗂️ Project Structure

Instagram_Trend_Analysis/ 
├── cleaning.sql # SQL script for data cleaning and normalization 
├── relational.py # Python script for relational database operations 
├── relational_itemset_mining.sql # SQL script for frequent itemset mining in PostgreSQL 
├── mongo_itemset_mining.py # Python script for frequent itemset mining in MongoDB 
└── README.md # Project documentation


---

## 🔍 Key Components

### 1. Data Cleaning and Preparation

- **Objective**: Normalize and structure raw Instagram data for efficient analysis.
- **Process**:
  - Utilize `cleaning.sql` to transform raw data into structured tables: `Addresses`, `Locations`, `Profiles`, and `Posts`.
  - Ensure data integrity and reduce redundancy through normalization.

### 2. Data Processing

- **Objective**: Handle large datasets efficiently.
- **Process**:
  - Implement scripts to process and analyze large volumes of data.
  - Create smaller subsets for testing and analysis without compromising performance.

### 3. Frequent Itemset Mining

- **Objective**: Identify frequently co-occurring locations in user posts.
- **Process**:
  - Apply frequent itemset mining algorithms using both SQL and Python.
  - Analyze patterns to uncover trends in location-based posting behavior.

---

## 📊 Sample Output

*Note: Replace this section with actual visualizations or findings from your analysis.*

---

## 🚀 Getting Started

### Prerequisites

- PostgreSQL installed and configured
- MongoDB installed and configured
- Python 3.x installed
- Required Python libraries installed (`pandas`, `pymongo`, etc.)

### Steps

1. **Clone the Repository**:
```
   git clone https://github.com/veeoid/Instagram_Trend_Analysis.git
   cd Instagram_Trend_Analysis
```
2. **Set Up Databases**:

PostgreSQL:
  Execute `cleaning.sql` to create and populate the necessary tables.
MongoDB:
  Import data into MongoDB collections as required.

3. **Run Analysis Scripts**:
  - For relational database analysis:
  ```
  python relational.py
  ```
  - For MongoDB Analysis:
  ```
  python mongo_itemset_mining.py
  ```
