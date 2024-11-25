import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def createCategDict(category_legend_path):
  categ_dict = dict()
  with open(category_legend_path, "r") as file:
      for linea in file:
          linea = linea.strip()
          elem = linea.split(",")
          categ_dict[elem[0].strip()] = elem[1].strip()
  return categ_dict

def check(dic):
  sum = 0
  for element in dic.keys():
    sum += dic[element]
  print(sum)

def plt_common_failure(indices,values,name,xlable_n,y_label_n,h_title,save_f,h_type=None):
    """! Utility to plot histograms
        @param indices,values,name,xlable_n,y_label_n,h_title,save_f
        @param h_type: histogram type h for horizontal otherwise is standard
        @return None
    """
    plt.figure(figsize=(30, 15))
    if(h_type == 'h'):
        plt.barh(indices, values, edgecolor='black',color='salmon')
    else:
        plt.bar(indices, values, edgecolor='black',color='salmon')
    plt.xticks(rotation=45)
    plt.title(h_title)
    plt.xlabel(xlable_n)
    plt.ylabel(y_label_n)
    plt.savefig(save_f+name+".png")

def plt_residual(data,save_f,name):
    plt.bar(data.keys(), data.values(), color='salmon', edgecolor='black', width=0.4)
    simmetric_Value = max([abs(x) for x in data.values()])+0.1
    plt.ylim(-simmetric_Value, simmetric_Value)
    plt.title('Residual Bar Plot')
    plt.xlabel('Models')
    plt.ylabel('Residuals')
    plt.savefig(save_f+name+".png",format="png", dpi=300)




def createPlot(labels,valori,save_f,name):
  plt.figure(figsize=(27, 19))
  plt.barh(labels, valori, color='salmon')
  plt.xlabel('Distribution')
  plt.ylabel('Category')
  plt.title('Category distribution')
  plt.savefig(save_f+name+".png",format="png", dpi=300)



def plt_categ_distribution(test_in_path,cat_legend_path,save_f,name):
    df = pd.read_excel(test_in_path)
    categ_dic = createCategDict(cat_legend_path)
    labels = list(categ_dic.values())
    labels_key = categ_dic.keys()
    histo_dict = dict()
    for key in labels_key:
        for i in range(0,len(df)-1):
            if(df["Category"][i] == int(key)):
                histo_dict[int(key)] = histo_dict.get(int(key), 0) + 1
    values = list(histo_dict.values())
    createPlot(labels,values,save_f,name)
    