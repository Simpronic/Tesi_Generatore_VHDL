import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

arr = {"CodeGen":-0.09 , "CodeT5_220": 0.02, "CodeT5_770": 0.05, "CodeGPT": -0.12,"ClaudeSonnet": -0.69}

plt.bar(arr.keys(), arr.values(), color='salmon', edgecolor='black', width=0.4)
simmetric_Value = max([abs(x) for x in arr.values()])+0.1
plt.ylim(-simmetric_Value, simmetric_Value)
# Aggiunta di titolo e etichette
plt.title('Bar Plot con Valori Negativi')
plt.xlabel('Categorie')
plt.ylabel('Valori')

# Mostra il grafico
plt.show()