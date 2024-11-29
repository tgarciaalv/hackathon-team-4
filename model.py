import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Step 1: Load the Data
file_path = '/workspaces/hackathon-team-4/data/FLIGHTS_CLEANED.CSV'
data = pd.read_csv(file_path)

# Step 2: Preprocess the Data
# Assuming 'DELAYED' is the target variable and is 1 if delayed > 15 mins, else 0
data['DELAYED'] = data['ArrDelay'].apply(lambda x: 1 if x > 15 else 0)

# Drop columns that won't be used as features
data = data.drop(columns=['ArrDelay'])

# Separate features and target
X = data.drop(columns=['DELAYED'])
y = data['DELAYED']

# Step 3: Feature Engineering
# Assuming 'DAY_OF_WEEK' and 'AIRPORT' are categorical features
categorical_features = ['DayOfWeek', 'OriginAirportID', 'DestAirportID', 'Carrier']
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Step 4: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Model Selection
# Using RandomForestClassifier for this example

# Step 6: Training the Model
# Preprocessing pipelines for numerical and categorical features
numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Create a pipeline that first preprocesses the data and then fits the model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
model.fit(X_train, y_train)

# Step 7: Evaluation
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Step 8: Save the Model
model_file_path = '/workspaces/hackathon-team-4/data/flight_delay_model.pkl'
joblib.dump(model, model_file_path)
print(f"Model saved to {model_file_path}")

# Expose the data variable
__all__ = ['data'] # Expose the data variable for use in the Flask app      

# Example of loading the model and making a prediction
# loaded_model = joblib.load(model_file_path)
# new_data = pd.DataFrame({
#     'DAY_OF_WEEK': [3],  # Example: Wednesday
#     'AIRPORT': ['JFK'],  # Example: JFK Airport
#     # Add other necessary features with example values
#     # Ensure these features match the training data structure
#     # Example: 'SOME_NUMERICAL_FEATURE': [value]
# })
# new_data = new_data.reindex(columns=X_train.columns, fill_value=0)
# probability = loaded_model.predict_proba(new_data)[:, 1]
# print("Probability of delay > 15 minutes:", probability)