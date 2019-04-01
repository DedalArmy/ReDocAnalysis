import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("E:/SandBox2/results/complete_projects_metrics_3.csv", sep=",")

#print(df[(df['nbClasses'] > 10) & (df['nbSourceCodeClasses'] > 5)])
#print(df['nbClasses'].describe())
projectPaths = df['ProjectPath']
projectPaths = projectPaths.drop_duplicates()
classXML = ['nbClasses','nbArchi']
classXML_df = pd.DataFrame(columns=classXML)
classXML_df = classXML_df.append({'nbClasses':0, 'nbArchi':0}, ignore_index=True)

for p in projectPaths:
    p_df = df[df['ProjectPath'] == p]
    print(p)
    print(p_df)
    nbClasses = p_df['nbClasses'].max()
    nbArchi = p_df['ProjectPath'].count()
    tempClassXML_df = pd.DataFrame([[nbClasses,nbArchi]], columns=classXML)
    print(tempClassXML_df)
    classXML_df = classXML_df.append(tempClassXML_df, ignore_index=True)
    
print(classXML_df, sep='\n')
plt.plot(classXML_df['nbClasses'], classXML_df['nbArchi'], 'ro')
plt.ylabel('# Deployment Descriptors')
plt.xlabel('# Classes')
plt.show()

classXML_df.to_csv("E:/SandBox2/results/complete_projects_metrics_nbclass_archi.csv")