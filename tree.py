import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder#for train test splitting
from sklearn.model_selection import train_test_split#for decision tree object
from sklearn.tree import DecisionTreeClassifier#for checking testing results
from sklearn.metrics import classification_report, confusion_matrix#for visualizing tree 
from sklearn import tree
import datetime as dt
from sklearn.tree import plot_tree
import numpy as np 

df = pd.read_csv('tree_month_agg.csv')

df = df.drop('Latitude',1)
df = df.drop('Longitude',1)
df = df[df['A2_RSSI'].notna()]
df = df.drop('A2_RSSI',1)
df = df.drop('Unnamed: 0',1)
df = df.drop('DisruptionCode',1)
df = df.drop('EventCode',1)
df = df.drop('PositionNoLeap',1)
df = df.drop('Day.Month',1)

df['CurrentVelocity']=np.sqrt(df['CurrentVelocity'])
df = df.dropna()
#df['Day.Month']=pd.to_datetime(df['Day.Month'], format='%Y-%m-%d')
#df['Day.Month']=df['Day.Month'].map(dt.datetime.toordinal)
#df['Day.Month']=np.sqrt(np.sqrt(np.sqrt(df['Day.Month'])))
#sns_plot = sns.pairplot(data=df, hue = 'A2_RSSI_1')
#sns_plot.savefig('sns_plot.png')

print(df.head())
target = df['A2_RSSI_1']
df1 = df.copy()
df1 = df1.drop('A2_RSSI_1', axis =1)
X = df1
le = LabelEncoder()
target = le.fit_transform(target)
y = target
X_train, X_test, y_train, y_test = train_test_split(X , y, test_size = 0.2, random_state = 42)
print("Training split input- ", X_train.shape)
print("Testing split input- ", X_test.shape)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)

print('Decision Tree Classifier Created')

fig = plt.figure()
_ = tree.plot_tree(clf)
fig.savefig('test.png')
#tree.plot_tree(decision_tree=dtree, feature_names = df1.columns, 
#                     class_names =["Weak", "Fair", "Good","Excellent"] , filled = True , precision = 4, rounded = True)