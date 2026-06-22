import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
data = pd.read_csv("data/student_data.csv")

# Features and target
X = data[["Study_Hours", "Attendance", "Previous_Marks"]]
y = data["Final_Marks"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "models/student_model.pkl")

print("AI model trained and saved successfully!")