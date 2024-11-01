import pylcs
import pandas as pd
import sys
import os

REQUEST_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.in"
REFS_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.out"
BASE_PATH =r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Results\Open-source-models\Open-source-models\Open-source-models"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Metrics_manager import *

def calc_lcs(hyps, refs):
	print("##### LCS #####\n")
	scores = []
	for hyp, ref in zip(hyps, refs):
		tmp = pylcs.lcs_sequence_length(hyp, ref)
		res_norm = tmp/max(len(hyp),len(ref))
		#print(res_norm)
		scores.append(str(res_norm))
	return scores

def calc_CB(hyps,refs):
    m_m = Metrics_manager()
    m_m.load_hyps(hyps)
    m_m.load_refs(refs)
    return m_m.calc_crystalBLEU(re_compute_ngrams=False)

req_path = REQUEST_PATH
refs_path = REFS_PATH

model_output_path = BASE_PATH+"\\CodeT5p_220"+"\\finetuned\\test-2024-07-06-16-09\\"+"hyps.txt"
excel_name = "CodeT5.xlsx"
df = pd.DataFrame()
in_text = []
refs_text = []
hyps_text = []
with open(req_path, 'r') as file:
    line = file.readline().strip()
    while line:
        in_text.append(line)
        line = file.readline().strip()
with open(refs_path, 'r') as file:
    line = file.readline().strip()
    while line:
        refs_text.append(line)
        line = file.readline().strip()
with open(model_output_path, 'r') as file:
    line = file.readline().strip()
    while line:
        hyps_text.append(line)
        line = file.readline().strip()

df['IN'] = in_text
df['REFS'] = refs_text
df['HYPS'] = hyps_text
df['LCS_M'] = calc_lcs(hyps_text,refs_text)
df['CRYSTALB_M'] = calc_CB(hyps_text,refs_text)
df.to_excel(excel_name,index=False)