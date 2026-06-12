import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("dataset/Disease_data.csv")

df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

# Convert date
df['date'] = pd.to_datetime(df['date'])
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df.drop('date', axis=1, inplace=True)

# Encode categorical columns
le_country = LabelEncoder()
le_occupation = LabelEncoder()

df['country'] = le_country.fit_transform(df['country'])
df['occupation'] = le_occupation.fit_transform(df['occupation'])

# Display columns
print(df.columns)

# Remove unnecessary columns if present
columns_to_drop = ['id']
for col in columns_to_drop:
    if col in df.columns:
        df = df.drop(col, axis=1)

print(df.dtypes)
# Display columns
print(df.columns)

# Features and target
X = df.drop('disease', axis=1)
y = df['disease']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)


print(X.columns.tolist())

# Save model
joblib.dump(model, "model.pkl")

print("Model saved successfully!")