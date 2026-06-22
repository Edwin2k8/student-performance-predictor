print("Step 1: Starting script")

import pandas as pd

df = pd.read_csv("data/data.csv")

print("Step 2: Data loaded")

X = df[['study_hours', 'attendance', 'previous_marks']]
y = df['final_marks']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Step 3: Split done")

from sklearn.linear_model import LinearRegression

model = LinearRegression()

print("Step 4: Training model...")

model.fit(X_train, y_train)

print("Step 5: Model trained")

import pickle

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Step 6: Saved successfully")