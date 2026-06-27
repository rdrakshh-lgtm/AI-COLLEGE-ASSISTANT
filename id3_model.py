import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import mysql.connector
import joblib

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="demo",
    database="college_assistant1"
)

cursor = db.cursor()

# Read data
cursor.execute("SELECT * FROM student_records_new")
rows = cursor.fetchall()

columns = [desc[0] for desc in cursor.description]

df = pd.DataFrame(rows, columns=columns)

# Remove unnecessary columns
df = df.drop(columns=["id", "student_usn"])

# Encode categorical columns
print(df.columns.tolist())
le = LabelEncoder()
# Encode categorical columns
for col in df.columns:
    if not pd.api.types.is_numeric_dtype(df[col]):
        df[col] = pd.factorize(df[col])[0]
        print(df.dtypes)
        print(df.head())

# Check data types
print(df.dtypes)
print(df.head())

# Features and target
X = df.drop("job_offer", axis=1)
y = df["job_offer"]

print(X.dtypes)

# Train ID3
model = DecisionTreeClassifier(criterion="entropy")
print(df["job_offer"].unique())
model.fit(X, y)
# Save the trained model
joblib.dump(model, "placement_id3_model.pkl")

print("Model Saved Successfully!")
print("Model Trained Successfully")
print("Accuracy:", model.score(X, y) * 100)

print("Model Trained Successfully")
print("Accuracy:", model.score(X, y) * 100)