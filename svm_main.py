import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

import Multivariate_Schemes_module as spm
from tabulate import tabulate
from os import makedirs
import re
# import dtreeviz

df = pd.read_csv("results\pm\MHWMA_ml_data.csv")

df = df[df['Delta']>0]

parm_names = {0:"B0",
              1:"B1",
              2:"B2",
              3:"S2",
              '-':'-'}

shift_sizes = {0:'-',0.5:"small",1.5:"medium",3:"large"}

df['Shift_size'] = [shift_sizes[df['Delta'][i]] for i in df.index]

#SCALE PREDICTORS
means = {"B0":3.0,
              "B1":2.0,
              "B2":5.0,
              "S2":0}
 
x_names = [f"X{i+1}" for i in range(3)]
x_values = np.arange(-4,4.5,0.5)
X_df = pd.DataFrame()
for i in range(3):
    X_df[x_names[i]] = x_values**(i)

print(X_df)

X_X = np.linalg.inv(np.array(X_df).T@np.array(X_df))

True_sig = np.zeros((4,4))

for i in range(3):
    for j in range(3):
        True_sig[i,j] = X_X[i,j]
        
True_sig[3,3] = 1

parm_vars = {"B0":True_sig[0,0],
        "B1":True_sig[1,1],
        "B2":True_sig[2,2],
        "S2":True_sig[3,3]}

df['B0'] = (df['B0'] - means['B0'])/np.sqrt(parm_vars['B0'])
df['B1'] = (df['B1'] - means['B1'])/np.sqrt(parm_vars['B1'])
df['B2'] = (df['B2'] - means['B2'])/np.sqrt(parm_vars['B2'])
df['S2'] = (df['S2'] - means['S2'])/np.sqrt(parm_vars['S2'])

print(df.head())

#PARAMETER IDETIFIER
X_train, X_test, id_y_train, id_y_test = train_test_split(df[['B0','B1','B2','S2']], df['Parm'], test_size=0.3,random_state=109) # 70% training and 30% test

x_names = X_train.columns

# print('Training ID Model: DT')
# parm_mdl = DecisionTreeClassifier()
# # parm_mdl = svm.LinearSVC(multi_class='ovr',max_iter=10000,C=0.8)
# parm_mdl.fit(X_train, id_y_train)
# parm_pred = parm_mdl.predict(X_test)

# print("="*30)
# print('ID Model Metrics')
# print("Accuracy:",metrics.accuracy_score(id_y_test, parm_pred))
# print("="*30)

print('Training ID Model: SVM')
# parm_mdl = DecisionTreeClassifier()
parm_mdl = svm.LinearSVC(multi_class='ovr',max_iter=10000,C=0.8)
parm_mdl.fit(X_train, id_y_train)
parm_pred = parm_mdl.predict(X_test)

print("="*30)
print('ID Model Metrics')
print("Accuracy:",metrics.accuracy_score(id_y_test, parm_pred))
print("="*30)

#SHIFT SIZE IDENTIFIEER
X_train, X_test, ss_y_train, ss_y_test = train_test_split(df[['B0','B1','B2','S2','T2']], df['Shift_size'], test_size=0.3,random_state=109) # 70% training and 30% test

print('Training Shift-Size Model: DT')
ss_mdl = RandomForestClassifier()
ss_mdl.fit(X_train, ss_y_train)
ss_pred = ss_mdl.predict(X_test)

# viz_model = dtreeviz.model(ss_mdl,
#                            X_train=X_train, y_train=ss_y_train,
#                            feature_names=x_names,
#                            target_name='Shift_size',
#                            class_names=["small","medium","large"])

# v = viz_model.view()     # render as SVG into internal object 
# v.show()   
             

print("="*30)
print('Shift-Size Model Metrics')
print("Accuracy:",metrics.accuracy_score(ss_y_test, ss_pred))
print("="*30)

# print('Training Shift-Size Model: SVM')
# ss_mdl = svm.LinearSVC(multi_class='ovr',max_iter=10000,C=0.8)
# ss_mdl.fit(X_train, ss_y_train)
# ss_pred = ss_mdl.predict(X_test)

# print("="*30)
# print('Shift-Size Model Metrics')
# print("Accuracy:",metrics.accuracy_score(ss_y_test, ss_pred))
# print("="*30)

#==================================================================================
#==================================================================================
#==================================================================================
#==================================================================================

#read data
exml_df = pd.read_csv('results/pm/ml_exmpl_data.csv')

#make latex table 
filepath = "./results/pm/tables"
makedirs(filepath, exist_ok=True)

cols = ['t','B0','B1','B2','S2']
col_symb = ['t','$\\beta_0$','$\\beta_1$','$\\beta_2$','$\\sigma^2$']
col_symb = ["{\color[HTML]{FFFFFF}" + x + "}" for x in col_symb]

spacing = "{ | " + ">{\\\\centering\\\\arraybackslash}m{0.03\\\\textwidth} | " + ">{\\\\centering\\\\arraybackslash}m{0.09\\\\textwidth} "*(len(cols)-1) + " | }"

raw_df = exml_df[cols]

float_fmt = ['.2f']*(len(cols)-1)
float_fmt = ['.0f'] + float_fmt
float_fmt = tuple(float_fmt)

tbl = str(tabulate(raw_df,col_symb,tablefmt="latex_raw",floatfmt=float_fmt,showindex="never"))
tbl = re.sub(r"\{r+\}",spacing,tbl)
tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)

filename = filepath + "/" + "_example_raw_table.txt"
with open(filename, "w") as f:
    print(tbl, file=f)

print(f"table saved in {filename}")

opt_k = lambda x: -x/2
phi = 0.25



print(True_sig)

true_parms = [3.0,2.0,5.0]
true_var = 0

true_mean = true_parms + [true_var]
true_mean = np.array(true_mean)

series = [true_mean]

mod_chart = spm.MHWMA(p=4,phi=phi,k=opt_k(phi),mean_0=true_mean,sig2_0=True_sig,L=14.1)
ex_chart = spm.EHWMA(p=4,phi=phi,phi2=0.05,mean_0=true_mean,sig2_0=True_sig,L=14.5)

mod_t2 = []
mod_ooc = []
ex_t2 = []
ex_ooc = []

for r in range(raw_df.shape[0]):
    row = raw_df.iloc[r,1:]
    series += [np.array(row)]

    mod_stat = mod_chart.chart_stat(series=series)
    ex_stat = ex_chart.chart_stat(series=series)

    mod_t2 += [mod_chart.T2_stat(mod_stat,t=(r+1))]
    ex_t2 += [ex_chart.T2_stat(ex_stat,t=(r+1))]

    mod_ooc += [mod_chart.check_ooc(mod_stat,t=(r+1))]
    ex_ooc += [ex_chart.check_ooc(ex_stat,t=(r+1))]

print(raw_df.iloc[-3:,1:])
print(raw_df.iloc[-3,1:])

pred_x_data_std = raw_df.copy()

pred_x_data_std['B0'] = (pred_x_data_std['B0'] - means['B0'])/np.sqrt(parm_vars['B0'])
pred_x_data_std['B1'] = (pred_x_data_std['B1'] - means['B1'])/np.sqrt(parm_vars['B1'])
pred_x_data_std['B2'] = (pred_x_data_std['B2'] - means['B2'])/np.sqrt(parm_vars['B2'])
pred_x_data_std['S2'] = (pred_x_data_std['S2'] - means['S2'])/np.sqrt(parm_vars['S2'])

pred_x_data_std = pred_x_data_std[['B0','B1','B2','S2']]
pred_x_data_std = pred_x_data_std.iloc[-3:,:]

print(pred_x_data_std)

parm = ['-']*5
mod_size = ['-']*5
ex_size = ['-']*5
pred_parm = parm_mdl.predict(X=pred_x_data_std)

pred_x_data_std['T2'] = mod_t2[-3:]
mod_pred_ss = ss_mdl.predict(X=pred_x_data_std)
pred_x_data_std['T2'] = ex_t2[-3:]
ex_pred_ss = ss_mdl.predict(X=pred_x_data_std)

print(pred_parm)

for i in range(3):
    parm += [pred_parm[i]] 
    mod_size += [mod_pred_ss[i]]
    ex_size += [ex_pred_ss[i]]

mod_tbl = raw_df.copy()
mod_tbl['T2'] = mod_t2
mod_tbl['OOC'] = mod_ooc
mod_tbl['Predicted Parameter'] = [parm_names[x] for x in parm]
mod_tbl['Predicted Shift Size'] = mod_size

ex_tbl = raw_df.copy()
ex_tbl['T2'] = ex_t2
ex_tbl['OOC'] = ex_ooc
ex_tbl['Predicted Parameter'] = [parm_names[x] for x in parm]
ex_tbl['Predicted Shift Size'] = ex_size

mod_tbl.to_csv('results/pm/MHWMA_ml_exmpl_data.csv',index=False,mode='w')
ex_tbl.to_csv('results/pm/EHWMA_ml_exmpl_data.csv',index=False,mode='w')


col_symb += ["{\color[HTML]{FFFFFF} $T^2$ }"]
col_symb += ["{\color[HTML]{FFFFFF} OOC }"]
col_symb += ["{\color[HTML]{FFFFFF} Predicted Parameter }"]
col_symb += ["{\color[HTML]{FFFFFF} Predicted Shift Size }"]

spacing = "{ | " + ">{\\\\centering\\\\arraybackslash}m{0.03\\\\textwidth} | " + ">{\\\\centering\\\\arraybackslash}m{0.09\\\\textwidth} "*(len(col_symb)-1) + " | }"

tbl = str(tabulate(mod_tbl,col_symb,tablefmt="latex_raw",floatfmt=float_fmt,showindex="never"))
tbl = re.sub(r"\{rrrrrrlll\}",spacing,tbl)
tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)

filename = filepath + "/" + "_example_mod_chart_table.txt"
with open(filename, "w") as f:
    print(tbl, file=f)
    
tbl = str(tabulate(ex_tbl,col_symb,tablefmt="latex_raw",floatfmt=float_fmt,showindex="never"))
tbl = re.sub(r"\{rrrrrrlll\}",spacing,tbl)
tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)

filename = filepath + "/" + "_example_ex_chart_table.txt"
with open(filename, "w") as f:
    print(tbl, file=f)