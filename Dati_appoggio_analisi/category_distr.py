
import pandas as pd

input_prompt = []
with open(r"C:\Users\marcd\Desktop\Tesi\Work\repo\Tesi_Generatore_VHDL\Dati_appoggio_analisi\data.in", "r") as file:
    # Leggi il file riga per riga
    for linea in file:
        # Rimuove eventuali spazi bianchi (come newline) alla fine della riga
        linea = linea.strip()
        input_prompt.append(linea)
category_distr = []
with open(r"C:\Users\marcd\Desktop\Tesi\Work\repo\Tesi_Generatore_VHDL\Dati_appoggio_analisi\categories_distrib-new.txt", "r") as file:
    # Leggi il file riga per riga
    for linea in file:
        # Rimuove eventuali spazi bianchi (come newline) alla fine della riga
        linea = linea.strip()
        category_distr.append(linea)

df = pd.DataFrame()
df["Prompt"] = input_prompt
df["Category"] = category_distr
df.to_excel("DataInCategClaudeSonnet.xlsx",index=False)

test_in_data = []
with open(r"C:\Users\marcd\Desktop\Tesi\Tools\ESCAPE-v2\datasets\vhdl\vhdl-test.in", "r") as file:
    # Leggi il file riga per riga
    for linea in file:
        # Rimuove eventuali spazi bianchi (come newline) alla fine della riga
        linea = linea.strip()
        test_in_data.append(linea)
category_data_for_test = [0] * len(test_in_data)
print(df.loc[df["Prompt"] == "use of std_logic library"].index.tolist())
for i in range(0,len(test_in_data)):
  print(i)
  category_data_for_test[i] = df["Category"][df.loc[df["Prompt"] == test_in_data[i]].index.tolist()].to_list()[0]

df_test_in = pd.DataFrame()
df_test_in["Prompt"] = test_in_data
df_test_in["Category"] = category_data_for_test
print(df_test_in)
df_test_in.to_excel("TestInCategClaudeSonnet.xlsx",index=False)