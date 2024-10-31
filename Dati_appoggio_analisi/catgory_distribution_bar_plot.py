"""Bar plot distribuzione categorie in test"""

import matplotlib.pyplot as plt
import pandas as pd

def createCategDict(category_legend_path):
  categ_dict = dict()
  with open(category_legend_path, "r") as file:
      for linea in file:
          linea = linea.strip()
          elem = linea.split(",")
          categ_dict[elem[0].strip()] = elem[1].strip()
  return categ_dict

def createPlot(labels,valori):
  plt.figure(figsize=(10, 13))
  plt.barh(labels, valori, color='salmon')
  plt.xlabel('Valori')
  plt.ylabel('Categorie')
  plt.title('Esempio di Bar Plot Orizzontale')
  plt.savefig("bar_plot.png", format="png", dpi=300)  # Salva con alta risoluzione (300 dpi)
  plt.show()

def check(dic):
  sum = 0
  for element in dic.keys():
    sum += dic[element]
  print(sum)

df = pd.read_excel("TestInCateg.xlsx")
categ_dic = createCategDict("categories_legend.txt")
labels = list(categ_dic.values())
labels_key = categ_dic.keys()
histo_dict = dict()
for key in labels_key:
  for i in range(0,len(df)-1):
    if(df["Category"][i] == int(key)):
      histo_dict[int(key)] = histo_dict.get(int(key), 0) + 1
values = list(histo_dict.values())
createPlot(labels,values)