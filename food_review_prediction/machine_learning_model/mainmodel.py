import pandas as pd
from sklearn.utils import resample
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.metrics import roc_auc_score


def phase1():
    # Loading the dataset
    food_data = pd.read_csv(r'D://education//projects//minor 1//food_review_prediction//dataset//Reviews.csv')

    # Taking only Score and Text columns
    food_data = food_data[['Score', 'Text']]
    # Removing the scores which have rating 3
    food_data = food_data[food_data.Score != 3]

    def f(r):
        if r > 3:
            return 1
        else:
            return 0

    food_data['Sentiment'] = food_data.Score.map(f)
    food_data = food_data.groupby('Sentiment')

    # Taking the scores of 1 and 2 as food_data_minor
    # Taking the scores of 4 and 5 as food_data_major
    for i, j in food_data:
        if i == 0:
            food_data_minor = j
        if i == 1:
            food_data_major = j

    # training dataset is highly imbalanced to balance the dataset we are downsampling of food_data_major which will be
    # equal to food_data_minor Taking 82,037 rows of both minor and major dataset

    food_data_major_downsampled = resample(food_data_major, replace=False, n_samples=82037, random_state=123)

    # Concatenating both the datasets
    food_data_balanced = pd.concat([food_data_minor, food_data_major_downsampled])
    food_data_balanced.drop(['Score'], axis=1, inplace=True)

    # Taking X as text column and Y as sentiment column
    X = food_data_balanced["Text"]
    y = food_data_balanced["Sentiment"]

    return X, y


def phase2(a, b):
    # Splitting the dataset to 70% as training and 30% for testing
    X_train, X_test, y_train, y_test = train_test_split(a, b, test_size=0.3, random_state=101)

    # Converting the datasets into vector model
    # CountVectorizer has default parameters as removing words,lemmatization,special characters and numbers
    vect = CountVectorizer(ngram_range=(1, 2)).fit(X_train)
    X_train_vectorized = vect.transform(X_train)

    # Pickling the model for deployment into flask web app
    pickle.dump(vect, open("D://education//projects//minor 1//food_review_prediction//output//vector.pkl", 'wb'))

    # Training the dataset with logistic regression model
    model1 = LogisticRegression(max_iter=200, multi_class='ovr', n_jobs=4)
    model1.fit(X_train_vectorized, y_train)

    # Pickling the trained model for deployment into flask web app
    pickle.dump(model1, open("D://education//projects//minor 1//food_review_prediction//output//model.pkl", 'wb'))
    predictions = model1.predict(vect.transform(X_test))
    print("Auc:", roc_auc_score(y_test, predictions))


if __name__ == "__main__":
    a, b = phase1()
    phase2(a, b)
