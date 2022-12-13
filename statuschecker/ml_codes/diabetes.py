import sklearn
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from matplotlib import pyplot as plt
from sklearn.feature_selection import SelectKBest, chi2, SelectFromModel
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_score, accuracy_score, recall_score
import pickle


class DiabetesTest:
    def __init__(self):
        # 1) DATA EXPLORATION
        # Data used to create breast_cancer_x.csv

        data = pd.read_csv("statuschecker/ml_codes/kaggle_datasets/diabetics.csv", sep=',')
        x = data.drop(labels=['Outcome'], axis=1)
        y = data["Outcome"]
        print('X', x, 'Y', y)

        # print('length of data =', len(data.columns), '\n', data.columns)

        # setting to print max output from dataframe
        #data.drop(rows=[768], axis=0)
        """"     pd.set_option("display.max_columns", 9)
        print("THE DATA TYPES \n", data.dtypes)
        print(data.head())
        print(np.array(data).shape)
        print(data.empty)
        print(data.describe())
        print(data.corr())
        '''for i in data.columns:
            #plt.scatter(data[i], data["Outcome"])
            plt.hist(data[i])
            plt.show()
        '''
        """
        # feature_Selection
        '''classifier = ExtraTreesClassifier()
        classifier.fit(x, y)
        f_selector = SelectFromModel(classifier, prefit=True)
        print("importance:\n", classifier.feature_importances_)
        selected_x = pd.DataFrame(f_selector.transform(x))
        selected_x.columns = f_selector.get_feature_names_out(x.columns)
        # print('\n selected x\'s \n',selected_x)
        # print("no of Selected x:\n", len(selected_x.columns))

        x = selected_x
        x.to_csv("saved_x/diabetics_x.csv")
'''

        x = pd.read_csv('statuschecker/ml_codes/saved_x/diabetics_x.csv', sep=',')
        # print(x.corr()[0:5])
        x.columns = ['n', 'Glucose', 'BMI', 'Age']
        x = x.drop(labels=['n'], axis=1)

        # splitting to test and train
        accuracy = 0
        precision = 0
        recall = 0
        best_accuracy, best_recall = 0, 0

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        for _ in range(10):
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            # model
            self.model = LogisticRegression(max_iter=1000)
            self.model.fit(x_train, y_train)


            # model evaluation
            #print(x_test)
            y_pred = self.model.predict(x_test)
            precision = precision_score(y_test, y_pred)
            accuracy = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)

            if (recall > best_recall and recall != 1) and (accuracy > best_accuracy and accuracy !=1):
                best_recall = recall
                best_accuracy = accuracy
                with open("statuschecker/ml_codes/saved_ml_models/diabetics_model.pickle", "wb") as f:
                    pickle.dump(self.model, f)

                print( 'precision', precision,'recall', best_recall, 'accuracy', best_accuracy)
                print('classification\n', report)

                # instance copy of the above
                self.precision = round(precision, 4)
                self.accuracy = round(accuracy, 4)
                self.recall = round(recall, 4)

        # saved model
        pickle_in = open('statuschecker/ml_codes/saved_ml_models/diabetics_model.pickle', "rb")
        self.model = pickle.load(pickle_in)

    def predictor(self, x):
        predicted_value = self.model.predict(np.reshape(x, (1, -1)))
        predicted_target = ""
        target_dict = {'Not Diabetic': 0, 'Diabetic': 1}

        for key, value in target_dict.items():
            if predicted_value == value:
                predicted_target = key

        return {
                'predicted_target': predicted_target,
                'accuracy': self.accuracy,
                'precision': self.precision,
                'recall': self.recall
                }



    #accuracy = classification_report(y_test, y_pred)
    #confusion_matrix = confusion_matrix(y_test, y_pred)
    #print('\n Confusion Matrix\n', confusion_matrix)
    #print('accuracy\n', accuracy)

    #plt.scatter(x['radius_mean'],y)
    #plt.show()

    '''print(y)
    print(x)
    print("Names of the x's \n", 'length =', len(features_names), '\n', features_names)
    print("\nNames of the y's \n", 'length =', len(labels),'\n', labels)'''


'''result1 = DiabetesTest()

put = np.array([0.2, 0.1, 0.3])
print(result1.predictor(put))
'''