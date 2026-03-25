import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('city_day.csv')

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Clean data
# Drop rows where AQI is missing
df = df.dropna(subset=['AQI'])

# Fill missing values with mean
df['PM2.5'] = df['PM2.5'].fillna(df['PM2.5'].mean())
df['PM10'] = df['PM10'].fillna(df['PM10'].mean())
df['NO2'] = df['NO2'].fillna(df['NO2'].mean())
df['CO'] = df['CO'].fillna(df['CO'].mean())
df['SO2'] = df['SO2'].fillna(df['SO2'].mean())

print("\nShape after cleaning:", df.shape)
print("Missing values after cleaning:")
print(df.isnull().sum())

print("\nData cleaned successfully!")

import matplotlib.pyplot as plt
import seaborn as sns

# Graph 1 - AQI Distribution
plt.figure(figsize=(10,6))
df['AQI'].hist(bins=50, color='steelblue', edgecolor='black')
plt.title('AQI Distribution across Indian Cities')
plt.xlabel('AQI Value')
plt.ylabel('Frequency')
plt.savefig('aqi_distribution.png')
plt.close()
print("Graph 1 saved!")

# Graph 2 - Average AQI by City
plt.figure(figsize=(14,6))
city_aqi = df.groupby('City')['AQI'].mean().sort_values(ascending=False)
city_aqi.plot(kind='bar', color='coral', edgecolor='black')
plt.title('Average AQI by City')
plt.xlabel('City')
plt.ylabel('Average AQI')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('city_aqi.png')
plt.close()
print("Graph 2 saved!")

# Graph 3 - Correlation Heatmap
plt.figure(figsize=(10,8))
features = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'AQI']
sns.heatmap(df[features].corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation between Pollutants and AQI')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.close()
print("Graph 3 saved!")

print("\nAll visualizations created successfully!")

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Prepare features and target
features = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2']
X = df[features]
y = df['AQI']

# Split data - 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training size:", X_train.shape)
print("Testing size:", X_test.shape)

# Model 1 - Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
print("\n--- Linear Regression ---")
print("R2 Score:", round(r2_score(y_test, lr_pred), 3))
print("MAE:", round(mean_absolute_error(y_test, lr_pred), 3))
print("RMSE:", round(mean_squared_error(y_test, lr_pred)**0.5, 3))

# Model 2 - Decision Tree
dt = DecisionTreeRegressor(random_state=42)
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)
print("\n--- Decision Tree ---")
print("R2 Score:", round(r2_score(y_test, dt_pred), 3))
print("MAE:", round(mean_absolute_error(y_test, dt_pred), 3))
print("RMSE:", round(mean_squared_error(y_test, dt_pred)**0.5, 3))

# Model 3 - Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
print("\n--- Random Forest ---")
print("R2 Score:", round(r2_score(y_test, rf_pred), 3))
print("MAE:", round(mean_absolute_error(y_test, rf_pred), 3))
print("RMSE:", round(mean_squared_error(y_test, rf_pred)**0.5, 3))

# Save best model
import joblib
joblib.dump(rf, 'aqi_model.pkl')
print("\nBest model (Random Forest) saved as aqi_model.pkl!")
