# -*- coding: utf-8 -*-
"""TSF_STUDENT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q-hoOMYWxmEKELCdDx78jQ4Asvvf3hvz

**GRIPNOV20**

**Name : Soumava Biswas**

**Data Science & Business Analytics Intern**

**GRIP TASK 1: Predict the percentage of a student based on no. of study hours.**
"""

#Reading the file through panda
import pandas as pd
import io
url='https://raw.githubusercontent.com/AdiPersonalWorks/Random/master/student_scores%20-%20student_scores.csv'
data=pd.read_csv(url)
data.head()

#Splitting data into regressor and regressand
x=data[['Hours']]
y=data['Scores']

# Plotting the scatter plot against Hours of study and percentage
import matplotlib.pyplot as plt
data.plot(x='Hours', y='Scores', style='*')  
plt.title('H.O.S vs Percentage')  
plt.xlabel('Hours of Study')  
plt.ylabel('Percentage')  
plt.show()

#splitting dataset into train data and test data
from sklearn.model_selection import  train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)

"""Now we will try different supervised learning algorithms and we will compare the predicted output.

1. Using Linear Regression
"""

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LinearRegression

#Learning our model on train data
regressor = LinearRegression()
regressor.fit(x_train, y_train)

#Predicting predicted Percentage against Hour of study on test data.
y_pred=regressor.predict(x_test)

# Plotting the regression line
line = regressor.coef_*x+regressor.intercept_

# Plotting for the test data
plt.scatter(x, y)
plt.plot(x, line);
plt.show()

# Comparing Actual vs Predicted
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})  
df

# You can also test with your own data
hours = 7
own_pred = regressor.predict([[hours]])
print("No of Hours = {}".format(hours))
print("Predicted Score = {}".format(own_pred[0]))

"""So far, so good. But when we increase study hours beyond 10, the result may surprise you."""

hours = 12
own_pred = regressor.predict([[hours]])
print("No of Hours = {}".format(hours))
print("Predicted Score = {}".format(own_pred[0]))

"""Well. Student may get a percentage of 120! To get rid of this kind of problem, here we will use some classification algorithm. But which one? Let's do some hypertuning between several parameters of Logistic regression and random forest classifier."""

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import numpy as np
pipe = Pipeline([('classifier' , RandomForestClassifier())])
pipe = Pipeline([('classifier', RandomForestClassifier())])

# Create param grid.

param_grid = [
    {'classifier' : [LogisticRegression()],
     'classifier__penalty' : ['l1', 'l2'],
    'classifier__C' : np.logspace(-4, 4, 20),
    'classifier__solver' : ['liblinear','lbfgs','newton-cg']},
    {'classifier' : [RandomForestClassifier()],
    'classifier__n_estimators' : list(range(10,101,10)),
    'classifier__max_features' : list(range(6,32,5))}
]

# Create grid search object

clf = GridSearchCV(pipe, param_grid = param_grid, cv = 2, verbose=True, n_jobs=-1)

# Fit on data

best_clf = clf.fit(x_train, y_train)

#Getting the best one
best_clf

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression

classifier=RandomForestClassifier(bootstrap=True,
                                                               ccp_alpha=0.0,
                                                               class_weight=None,
                                                               criterion='gini',
                                                               max_depth=None,
                                                               max_features='auto',
                                                               max_leaf_nodes=None,
                                                               max_samples=None,
                                                               min_impurity_decrease=0.0,
                                                               min_impurity_split=None,
                                                               min_samples_leaf=1,
                                                                min_weight_fraction_leaf=0.0,
                                                                n_estimators=100,
                                                                n_jobs=None,
                                                                oob_score=False,
                                                                random_state=None,
                                                                verbose=0,
                                                                warm_start=False)
classifier.fit(x_train,y_train)

#Predict the test data using the model
y_pred = classifier.predict(x_test)

#Let's test the model with study hours beyond 10
hours = 13
own_pred = classifier.predict([[hours]])
print("No of Hours = {}".format(hours))
print("Predicted Score = {}".format(own_pred[0]))

#Comparing predicted output and actual output through bar graph
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])

l1 = ax.bar(np.arange(len(x_test.to_numpy().flatten().tolist())),y_test.to_numpy().flatten().tolist(),width=0.2) # solid line with yellow colour and square marker
l2 = ax.bar(np.arange(len(x_test.to_numpy().flatten().tolist()))+0.2,y_pred.tolist(),width=0.2) # dash line with green colour and circle marker
ax.legend(labels = ('Actual', 'Predicted'), loc = 'lower right') # legend placed at lower right
ax.set_title("Study hour vs. Percentage")
ax.set_xlabel('Study hour')
ax.set_ylabel('Percentage')
ax.set_xticks(np.arange(len(x_test)))
ax.set_xticklabels(x_test.to_numpy().flatten().tolist())
plt.show()