import pickle
vectorizer = pickle.load(open("D://education//projects//minor 1//food_review_prediction//output//vector.pkl", "rb"))
model = pickle.load(open("D://education//projects//minor 1//food_review_prediction//output//model.pkl", "rb"))
print(model.predict(vectorizer.transform([input()])))