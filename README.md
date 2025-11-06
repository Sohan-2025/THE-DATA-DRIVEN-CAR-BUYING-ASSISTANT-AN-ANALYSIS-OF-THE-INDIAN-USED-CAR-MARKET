# THE-DATA-DRIVEN-CAR-BUYING-ASSISTANT-AN-ANALYSIS-OF-THE-INDIAN-USED-CAR-MARKET

# Used Car Price Dataset (India)

This project contains a comprehensive, cleaned, and expanded dataset of used car listings from across India. It is ideal for data analysis, visualization, and building machine learning models for tasks like price prediction.



This dataset was compiled, cleaned for uniformity, and expanded to include a wider variety of models, especially newer (2023-2025) and electric/hybrid vehicles. The primary file is uniform_car_dataset.csv.

## Features of the Dataset

* *Cleaned & Uniform:* Categorical data like Fuel Type and Owner has been standardized (e.g., "CNG + CNG" and "CNG" are both unified as "CNG").
* *Lightweight:* Extraneous columns (like Max Torque, Max Power) have been removed for easier and faster processing, focusing on the key features for price analysis.
* *Expanded:* The dataset includes 200 rows, with many hypothetical additions for 2023-2025 models to provide a richer mix of modern vehicles.
* *Diverse:* Contains a wide variety of:
    * *Fuel Types:* Petrol, Diesel, CNG, Electric, and Hybrid.
    * *Transmissions:* Manual and Automatic.
    * *Price Brackets:* From budget hatchbacks to luxury EVs.
    * *Segments:* Hatchbacks, Sedans, SUVs, and MUVs.

## Data Dictionary (Schema)

Below is a description of each column found in uniform_car_dataset.csv.

| Column | Description | Data Type | Example |
| :--- | :--- | :--- | :--- |
| *Make* | The manufacturer of the car. | String | Maruti Suzuki |
| *Model* | The specific model of the car. | String | Swift VXi |
| *Price* | The selling price of the car in Indian Rupees (₹). | Integer | 505000 |
| *Year* | The year the car was manufactured. | Integer | 2017 |
| *Kilometer* | The total kilometers driven by the car. | Integer | 87150 |
| *Fuel Type* | The type of fuel the car uses. | String | Petrol |
| *Transmission*| The transmission type. | String | Manual |
| *Location* | The city where the car is being sold. | String | Pune |
| *Color* | The exterior color of the car. | String | Grey |
| *Owner* | The ownership history. | String | First |
| *Seller Type*| The type of seller. | String | Individual |
| *Drivetrain* | The drivetrain configuration. | String | FWD |
| *Length* | The overall length of the car in millimeters (mm). | Integer | 3990 |
| *Width* | The overall width of the car in millimeters (mm). | Integer | 1680 |
| *Height* | The overall height of the car in millimeters (mm). | Integer | 1505 |
| *Seating Capacity* | The total number of seats in the car. | Integer | 5 |

## Example Usage

Here is a simple example of how to load and inspect the dataset using Python and the pandas library.

```python
import pandas as pd

# Load the dataset
try:
    df = pd.read_csv('uniform_car_dataset.csv')
    
    # Display the first 5 rows
    print("Dataset Head:")
    print(df.head())
    
    # Get a quick summary of the data
    print("\nDataset Info:")
    df.info()
    
    # See the distribution of Fuel Types
    print("\nFuel Type Distribution:")
    print(df['Fuel Type'].value_counts())

except FileNotFoundError:
    print("Error: 'uniform_car_dataset.csv' not found.")
    print("Please make sure the file is in the same directory as your script.")


Potential Project Ideas
This dataset is well-suited for a variety of data science projects:
 * Price Prediction: Build a regression model (e.g., Linear Regression, Random Forest, XGBoost) to predict the Price of a used car based on its features.
 * Market Analysis: Analyze trends in the used car market.
   * How does the price of EVs and Hybrids compare to their petrol/diesel counterparts?
   * What is the most popular car make/model in different locations?
   * How much does Kilometer driven or Year manufactured impact resale value?
 * Feature Importance: Determine which features are the most important in determining a car's price.
 * Dashboarding: Create an interactive dashboard (using tools like Tableau, Power BI, or Streamlit) to filter and explore the listings.
<!-- end list -->
