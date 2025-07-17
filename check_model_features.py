import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

print("Trained model expects these features:")
print(model.feature_names_in_)
