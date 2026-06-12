import joblib
import pandas as pd

model = joblib.load("model1.pkl")

classifier = model.named_steps['classifier']

feature_names = model.named_steps[
    'preprocessor'
].get_feature_names_out()

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': classifier.feature_importances_
})

importance_df = importance_df.sort_values(
    by='Importance',
    ascending=False
)

print(importance_df.head(10))