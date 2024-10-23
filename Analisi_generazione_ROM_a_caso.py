# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime


CodeT5xlsx = "AnalisiCodeT5_225.xlsx"
CodeGenxlsx = "AnalisiCodeGen.xlsx"

df_code_T5 = pd.read_excel(CodeT5xlsx)
df_code_gen = pd.read_excel(CodeGenxlsx)

filtro_CodeGen =  df_code_gen[df_code_gen["HYPS"].str.contains('ROM|RAM', case=False, na=False)]
filtro_CodeT5 =  df_code_T5[df_code_T5["HYPS"].str.contains('ROM|RAM', case=False, na=False)]

#Tolgo le istanze dove mi è richiesta esplicitamente una ROM/RAM

filtro_CodeGen2 = filtro_CodeGen[~filtro_CodeGen["IN"].str.contains('ROM|RAM', case=False, na=False)]
filtro_CodeT52 = filtro_CodeT5[~filtro_CodeT5["IN"].str.contains('ROM|RAM', case=False, na=False)]

print(len(filtro_CodeGen2["HYPS"]))
print(len(filtro_CodeT52["HYPS"]))