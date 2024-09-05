# -*- coding: utf-8 -*-
"""Klasifikasi Iris - KNN.ipnyb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VHCRtgrJEcCzaWljBuiuemfU3BU58GS9

## **Penyiapan Dataset**
"""

# import library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn import datasets

import seaborn as sns

# load dataset
iris = datasets.load_iris()

# visualisasi dataset
df = pd.DataFrame(iris.data, columns = iris.feature_names)
df['Target'] = pd.Series(iris.target)
print("Data Head: \n", df.head(), "\n")
print("Data Distribution: \n", df.describe(), "\n")
sns.pairplot(df, hue='Target', palette=("tab10"))

"""## **Splitting, Standarisasi, dan Normalisasi Dataset**"""

# splitting dataset into train-set and test-set
from sklearn.model_selection import train_test_split
x = iris.data # feature
y = iris.target # label (3 kategori: 0, 1, 2)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

print("x_train: ", x_train.shape)
print("y_test: ", y_test.shape)
print("x_test: ", x_test.shape)
print("y_train: ", y_train.shape)

# standarisasi dataset (pemerataan distribusi)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# normalisasi dataset (mengecilkan/membesarkan jarak antar nilai)
from sklearn.preprocessing import Normalizer

normalizer = Normalizer().fit(x_train)
x_train = normalizer.transform(x_train)
x_test = normalizer.transform(x_test)

"""## **Training Model**"""

# pengecekan konstanta k-fold
# overfitting < k-fold < underfitting
# nilai kfold pada umumnya: dataset<100 -> 2-5; dataset=100-200 -> 5-10; dataset>200 -> 10 - 15
from sklearn import neighbors

error = []
for i in range(1, 40):
    knn = neighbors.KNeighborsClassifier(n_neighbors = i)
    knn.fit(x_train, y_train)

    prediction_i = knn.predict(x_test)
    error.append(np.mean(prediction_i != y_test))

plt.figure()
plt.plot(range(1, 40), error, color='red', marker='.', markerfacecolor='blue', markersize=10)
plt.xlabel('Nilai K')
plt.ylabel('Rata-Rata Error')
plt.show()

# training model dengan n yang sesuai

knn = neighbors.KNeighborsClassifier(n_neighbors = 4) # lakukan tuning pada n_neighbors
knn.fit(x_train, y_train)

"""## **Uji dan Validasi Model**"""

# uji coba dan evaluasi model menggunakan test_set
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

y_pred = knn.predict(x_test)
print(classification_report(y_test, y_pred))

print("Akurasi: ", round(accuracy_score(y_test, y_pred)*100, 2), "%\n")
print("Presisi: ", round(precision_score(y_test, y_pred, average='weighted') * 100, 2), "%\n")
print("Recall : ", round(recall_score(y_test, y_pred, average='weighted') * 100, 2), "%\n")

cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm).plot()

# pengujian dengan K-fold cross-validation
from sklearn.model_selection import KFold, cross_val_score

scores = (cross_val_score(knn, x, y, cv=5, scoring='accuracy'))*100
print("Accuracy per fold: ", scores)
print("Average accuracy : ", round(scores.mean(), 2), "%")