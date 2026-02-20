import pickle

with open("label_encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

# Example: DiagnosisChapter
print(encoders['DiagnosisChapter'].classes_)

for col, le in encoders.items():
    print(f"Column: {col}")
    print("Classes:", le.classes_)
    print()
