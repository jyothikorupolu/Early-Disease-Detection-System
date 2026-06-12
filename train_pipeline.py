import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("dataset/Data_file - data_file.csv")


print(df.dtypes)
print(df.columns)

df.drop(['date', 'id'], axis=1, inplace=True)
print(df.columns)

# Features and target
X = df.drop('disease', axis=1)
y = df['disease']

# Text columns
categorical_features = ['country', 'occupation']

# Remaining columns
numeric_features = [col for col in X.columns
                    if col not in categorical_features]

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'),
         categorical_features)
    ],
    remainder='passthrough'
)

# Pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ))
])
print(df.dtypes)
print(X.columns.tolist())

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train
pipeline.fit(X_train, y_train)

# Accuracy
accuracy = pipeline.score(X_test, y_test)

print("Accuracy:", accuracy)

# Save
joblib.dump(pipeline, "model1.pkl")

print("Professional model saved successfully!")