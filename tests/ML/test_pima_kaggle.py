#%%
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, roc_curve, classification_report

# Load the dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
           'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
df = pd.read_csv(url, names=columns)

# Split features and target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Handle zero values for features where zero is not biologically valid
cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
#X[cols_with_zeros] = X[cols_with_zeros].replace(0, np.nan)
#X[cols_with_zeros] = X[cols_with_zeros].fillna(X[cols_with_zeros].median())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42, stratify=y)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_scaled, y_train)

# Predict probabilities
y_proba = clf.predict_proba(X_test_scaled)[:, 1]
y_pred = clf.predict(X_test_scaled)

# Compute AUROC
auroc = roc_auc_score(y_test, y_proba)
print(f"AUROC: {auroc:.4f}")

# Optional: classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# %%
X_scaled = scaler.fit_transform(X)

# Predict probabilities
y_proba = clf.predict_proba(X_scaled)[:, 1]
y_pred = clf.predict(X_scaled)
pd.Series(y_pred).value_counts()
# %%
