import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.series import Series
from itertools import count
from unittest.mock import inplace
from numpy import NaN

df = pd.read_csv("E:/SandBox2/results/complete_projects_metrics_3.csv", sep=",")
project_path = 'ProjectPath'
nb_classes = 'nbClasses'
nb_archi = 'nbArchi'
nb_source_code_classes = 'nbSourceCodeClasses'
nb_outter_classes = 'nbOutterClasses'
mean_object_coupling = 'CouplingBetweenObjectsMean'
mean_inheritance_depth = 'DepthInheritanceTreeMean'
nb_comp_classes = 'nbCompClasses'
nb_comp_roles = 'nbCompRoles'
nb_connections = 'nbConnections'

df_0 = df
df_0.to_csv('E:/SandBox2/results/df_0.csv')
df_1 = df[
    (df[nb_comp_classes] > 0)
    ]
df_1.to_csv('E:/SandBox2/results/df_1.csv')
df_2 = df[
    (df[nb_comp_classes] > 0)
    & (df[nb_comp_classes] <= df[nb_comp_roles])
    ]
df_2.to_csv('E:/SandBox2/results/df_2.csv')
df_3 = df[
    (df[nb_comp_classes] > 0)
    & (df[nb_comp_classes] <= df[nb_comp_roles])
    & (df[nb_connections] > 0)
    ]
df_3.to_csv('E:/SandBox2/results/df_3.csv')
print('df_0 : ' + str(df_0[nb_classes].count()))
print('df_1 : ' + str(df_1[nb_classes].count()))
print('df_2 : ' + str(df_2[nb_classes].count()))
print('df_3 : ' + str(df_3[nb_classes].count()))
print('\n')

#
# set df to choose the base dataframe
#
df = df_3


#
# Getting relation between nbClasses and nbArchis
#

projectPaths = df[project_path]
projectPaths = projectPaths.drop_duplicates()
classXML = [nb_classes,nb_archi]
classXML_df = pd.DataFrame(columns=classXML)
classXML_df = classXML_df.append({nb_classes:0, nb_archi:0}, ignore_index=True)

for p in projectPaths:
    p_df = df[df[project_path] == p]
    nbClasses = p_df[nb_classes].max()
    nbArchi = p_df[project_path].count()
    tempClassXML_df = pd.DataFrame([[nbClasses,nbArchi]], columns=classXML)
    classXML_df = classXML_df.append(tempClassXML_df, ignore_index=True)
    
classXML_df.sort_values(by=[nb_classes], inplace=True)
classXML_df2 = classXML_df.drop(classXML_df.tail(1).index, inplace=False)

#
# Getting relation between nbClasses and ration of instantiated source code classes
#
grouped_by_project_path = df.groupby(by=project_path)
grouped_by_project_path_df = pd.DataFrame(grouped_by_project_path, columns=[project_path, 'df'])#[nb_classes].max().reset_index(name=nb_classes))

grouped_by_project_path_df_bis = pd.DataFrame(grouped_by_project_path[nb_classes].max().reset_index(name=nb_classes))

grouped_by_project_path_df['Range'] = Series(grouped_by_project_path_df_bis[nb_classes]//100*100, index=grouped_by_project_path_df.index)
grouped_by_project_path_df[nb_classes] = Series(grouped_by_project_path_df_bis[nb_classes], index=grouped_by_project_path_df.index)
grouped_by_nb_projects = grouped_by_project_path_df.groupby(by='Range')
range_cat = grouped_by_nb_projects.apply(list).count()
values = grouped_by_nb_projects.apply(list)
grouped_by_nb_projects_df = pd.DataFrame(grouped_by_nb_projects[project_path].count().reset_index(name='nbProjects'))


#
# fig1
#

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(9,9))
range_labels = ()


ax[0,0].plot(classXML_df[nb_classes], classXML_df[nb_archi], 'ro')
ax[0,0].set_title('Class and XML')
ax[0,0].set_ylabel('# Deployment Descriptors')
ax[0,0].set_xlabel('# Classes')

for x in grouped_by_nb_projects_df['Range'].values.tolist():
    range_labels = range_labels + ((str(int(x)) + '-' + str(int(x+99))),)

#print(range(len(grouped_by_nb_projects_df['Range'])))

#print(range_labels)
ax[0,1].bar(range(len(grouped_by_nb_projects_df['Range'])), grouped_by_nb_projects_df['nbProjects'].values.tolist())
ax[0,1].set_title('')
ax[0,1].set_ylabel('# Projects')
ax[0,1].set_xlabel('# Classes Range')
ax[0,1].set_xticklabels(('',)+range_labels)

grouped_by_nb_projects_df = pd.DataFrame(grouped_by_nb_projects, columns=['Range', 'df'])
#print(grouped_by_nb_projects_df)

data_violin_instantiated = []
data_violin_instantiated_outter = []
data_violin_instantiated_ratio = []
data_plot_instantiated_ratio = []
data_violin_archi = []
for key,val in grouped_by_nb_projects_df['df'].to_dict().items():
    temp_data_archi = []
    temp_data_inst_source = []
    temp_data_inst_source_ratio = []
    temp_data_inst_outter = []
    for x in val['df'].values.tolist():
        for y in range(len(x[nb_source_code_classes].values.tolist())) :
            if x[nb_comp_classes].values.tolist()[y] >0 :
                ratio = x[nb_source_code_classes].values.tolist()[y]/x[nb_comp_classes].values.tolist()[y]
                temp_data_inst_source_ratio.append(ratio)
                data_plot_instantiated_ratio.append(ratio)
            else : 
                ratio = NaN
                data_plot_instantiated_ratio.append(ratio)
            temp_data_inst_source.append(x[nb_source_code_classes].values.tolist()[y])
            temp_data_inst_outter.append(x[nb_outter_classes].values.tolist()[y])
        temp_data_archi.append(x[project_path].count())
    data_violin_archi.append(temp_data_archi)
    data_violin_instantiated.append(temp_data_inst_source)
    data_violin_instantiated_ratio.append(temp_data_inst_source_ratio)
    data_violin_instantiated_outter.append(temp_data_inst_outter)

#ax[1,0].violinplot(data_violin_archi, showmeans=False, showmedians=True)
ax[1,0].boxplot(data_violin_archi, showmeans=False)
ax[1,0].set_ylabel('# Architectures')
ax[1,0].set_xlabel('# Classes Range')
ax[1,0].set_xticklabels(range_labels)

#ax[1,1].violinplot(data_violin_instantiated, showmeans=False, showmedians=True)
ax[1,1].boxplot(data_violin_instantiated, showmeans=False)
ax[1,1].set_ylabel('# Instantiated Source Code Classes')
ax[1,1].set_xlabel('# Classes Range')
ax[1,1].set_xticklabels(range_labels)

#plt.setp(ax[0,1].get_xticklabels(), rotation=40, horizontalalignment='right')
#plt.setp(ax[1,0].get_xticklabels(), rotation=40, horizontalalignment='right')


fig2, ax2 = plt.subplots(nrows=2, ncols=2, figsize=(9,9))

ax2[0,0].boxplot(data_violin_instantiated_outter, showmeans=False)
ax2[0,0].set_title('')
ax2[0,0].set_ylabel('# Instantiated Outer Classes')
ax2[0,0].set_xlabel('# Classes Range')
ax2[0,0].set_xticklabels(range_labels)

ax2[0,1].boxplot(data_violin_instantiated_ratio, showmeans=False)
ax2[0,1].set_title('')
ax2[0,1].set_ylabel('Instantiated Source Code Class Ratio')
ax2[0,1].set_xlabel('# Classes Range')
ax2[0,1].set_xticklabels(range_labels)

nbsource_df = pd.DataFrame(grouped_by_project_path[nb_source_code_classes].sum().reset_index(name=nb_source_code_classes))

ax2[1,0].plot(grouped_by_project_path_df[nb_classes].values.tolist(),nbsource_df[nb_source_code_classes].values.tolist(), 'ro')
ax2[1,0].set_title('')
ax2[1,0].set_ylabel('Instantiated Source Code Classes (sum/projects)')
ax2[1,0].set_xlabel('# Classes')

ax2[1,1].plot(df[nb_comp_classes].values.tolist(),df[nb_source_code_classes].values.tolist(), 'ro')
ax2[1,1].set_title('')
ax2[1,1].set_ylabel('Instantiated Source Code Classes (sum/projects)')
ax2[1,1].set_xlabel('# components in architectures')

fig3, ax3 = plt.subplots(nrows=2, ncols=2, figsize=(9,9))
#ax3[0,0].plot(grouped_by_project_path_df[nb_classes].values.tolist(),data_plot_instantiated_ratio, 'ro')

fig.tight_layout()
fig2.tight_layout()
fig3.tight_layout()
classXML_df.to_csv("E:/SandBox2/results/complete_projects_metrics_nbclass_archi.csv")

abstracted_df = df[
    df['nbCompClasses'] != df['nbCompRoles']
    ]
print('abstracted architectures : ')
print(abstracted_df)
print()

grouped_by_sdslfile_df = pd.DataFrame(df_3.groupby(by=project_path))
print('Architectures grouped by sdsl file name')
print(grouped_by_sdslfile_df.to_dict())
grouped_by_sdslfile_df.to_csv('E:/SandBox2/results/grouped_by_sdslfile_df.csv')

fig4, ax4 = plt.subplots()
ax4.plot(df[nb_comp_classes].values.tolist(),df[nb_source_code_classes].values.tolist(), 'ro')
ax4.set_title('')
ax4.set_ylabel('Instantiated Source Code Classes (sum/projects)')
ax4.set_xlabel('# components in architectures')

plt.show() 
