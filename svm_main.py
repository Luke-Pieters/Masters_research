import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import dtreeviz

df = pd.read_csv("results\pm\MHWMA_ml_data.csv")

df = df[df['Delta']>0]

parm_names = {0:"B0",
              1:"B1",
              2:"B2",
              3:"S2"}

sift_sizes = {0.5:"small",1.5:"medium",3:"large"}

df['Shift_size'] = [sift_sizes[df['Delta'][i]] for i in df.index]

#SCALE PREDICTORS
df['B0'] -= np.mean(df['B0'])
df['B1'] -= np.mean(df['B1'])
df['B2'] -= np.mean(df['B2'])
df['S2'] -= np.mean(df['S2'])
# df['T2'] -= np.mean(df['T2'])

print(df.head())

#PARAMETER IDETIFIER
X_train, X_test, id_y_train, id_y_test = train_test_split(df[['B0','B1','B2','S2']], df['Parm'], test_size=0.3,random_state=109) # 70% training and 30% test

x_names = X_train.columns

print('Training ID Model: DT')
parm_mdl = DecisionTreeClassifier()
# parm_mdl = svm.LinearSVC(multi_class='ovr',max_iter=10000,C=0.8)
parm_mdl.fit(X_train, id_y_train)
parm_pred = parm_mdl.predict(X_test)

print("="*30)
print('ID Model Metrics')
print("Accuracy:",metrics.accuracy_score(id_y_test, parm_pred))
print("="*30)

print('Training Shift-Size Model: SVM')
# parm_mdl = DecisionTreeClassifier()
parm_mdl = svm.LinearSVC(multi_class='ovr',max_iter=10000,C=0.8)
parm_mdl.fit(X_train, id_y_train)
parm_pred = parm_mdl.predict(X_test)

print("="*30)
print('ID Model Metrics')
print("Accuracy:",metrics.accuracy_score(id_y_test, parm_pred))
print("="*30)

#SHIFT SIZE IDENTIFIEER
X_train, X_test, ss_y_train, ss_y_test = train_test_split(df[['B0','B1','B2','S2']], df['Shift_size'], test_size=0.3,random_state=109) # 70% training and 30% test

print('Training Shift-Size Model: DT')
ss_mdl = DecisionTreeClassifier()
ss_mdl.fit(X_train, ss_y_train)
ss_pred = ss_mdl.predict(X_test)

viz_model = dtreeviz.model(ss_mdl,
                           X_train=X_train, y_train=ss_y_train,
                           feature_names=x_names,
                           target_name='Shift_size',
                           class_names=["small","medium","large"])

v = viz_model.view()     # render as SVG into internal object 
v.show()   
             

print("="*30)
print('Shift-Size Model Metrics')
print("Accuracy:",metrics.accuracy_score(ss_y_test, ss_pred))
print("="*30)

print('Training Shift-Size Model: SVM')
ss_mdl = svm.LinearSVC(multi_class='ovr',max_iter=10000,C=0.8)
ss_mdl.fit(X_train, ss_y_train)
ss_pred = ss_mdl.predict(X_test)

print("="*30)
print('Shift-Size Model Metrics')
print("Accuracy:",metrics.accuracy_score(ss_y_test, ss_pred))
print("="*30)


