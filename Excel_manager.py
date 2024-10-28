import pandas as pd
from Metrics_manager import *
from datetime import datetime
from scipy.stats import spearmanr, kendalltau
import scipy.stats as st 
import numpy as np
import pdb

REQUEST_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.in"
REFS_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.out"
COLUMS = {"IN","REFS","HYPS","EM_M","ED_M","METEOR_M","HUMAN_E"}
METRICS_NAME = ["EM_M","ED_M","METEOR_M"]


class Excel_creator:

        def __init__(self,requests,hyps,refs,excel_name):
            if(requests != None):   
                self.req_path = requests
            if(refs != None):
                self.refs_path = refs
            if(hyps != None):
                self.model_output_path = hyps
            if(excel_name != None):
                self.excel_name = excel_name+".xlsx"
            self.m_m = Metrics_manager()
            self.excel_to_analyze = None

        def __confidence_interval_t_student(self,data):
            return st.t.interval(confidence=0.95, df=len(data)-1,loc=np.mean(data),scale=st.sem(data)) 
            
        def __confidence_interval_normal(self,data):
            return st.norm.interval(confidence=0.95,loc=np.mean(data),scale=st.sem(data)) 
        
        def __confidence_interval_calculation(self,data):
            if(len(data) < 30):
                ub,lb= self.__confidence_interval_t_student(data)
            else:
                ub,lb = self.__confidence_interval_normal(data)
            return f"[{lb},{ub}]"
            
        def __time_to_ms(self,time):
            minuti, secondi, millisecondi = map(int, time.split(':'))
            totale_millisecondi = (minuti * 60 * 1000) + (secondi * 1000) + millisecondi
            return totale_millisecondi
        
        def __max_elab_time_and_rows(self,analisis_df):
            elab_time_max = analisis_df["Time"].max()
            rows = analisis_df[analisis_df["Time"] == elab_time_max]["Righe"]
            return elab_time_max, rows
        
        def __millisecondi_in_tempo(self,millisecondi):
            minuti = millisecondi // (60 * 1000)
            millisecondi %= (60 * 1000)
            secondi = millisecondi // 1000
            millisecondi %= 1000
            return f"{minuti:2}:{secondi:2}:{millisecondi:2}" 

        def setAllParameters(self,requests,hyps,refs,excel_name):
            if(requests != None):   
                self.req_path = requests
            if(refs != None):
                self.refs_path = refs
            if(hyps != None):
                self.model_output_path = hyps
            if(excel_name != None):
                self.excel_name = excel_name+".xlsx"
            self.excel_to_analyze = None
            
        def clearExcel_to_analyze(self):
             self.excel_to_analyze = None

        def rom_phenomenaAnalisis(self):
            filtro =  self.excel_to_analyze[self.excel_to_analyze["HYPS"].str.contains('ROM|RAM', case=False, na=False)]
            filtro = filtro[~filtro["IN"].str.contains('ROM|RAM', case=False, na=False)]
            print(f"Entry with random ROM block: ")
            print(len(filtro["HYPS"]))

        def correlationAnalysis(self): #Assumo che il df sia stato caricato
            he_m = self.excel_to_analyze["HUMAN_E"]
            for metric in METRICS_NAME:
                print(f"Analizyng {metric}...")
                spearman_corr, spearman_p_value = spearmanr(he_m, self.excel_to_analyze[metric])
                kendall_corr, kendall_p_value = kendalltau(he_m, self.excel_to_analyze[metric])

                print("Spearman Correlation:", spearman_corr)
                print("Spearman P-value:", spearman_p_value)

                print("Kendall Correlation:", kendall_corr)
                print("Kendall P-value:", kendall_p_value)

                print("\n\n")

        def evaluationTimeAnalysis(self,evaluation_file_times):
            df = pd.read_csv(evaluation_file_times, header=None, names=['Righe', 'Time'], quotechar='"')
            times = [self.__time_to_ms(time) for time in df["Time"]]
            df["Time"] = times
            max_elab_time,rows = self.__max_elab_time_and_rows(df)
            for row in rows:
                print(f"Max Time: {max_elab_time} ms ({self.__millisecondi_in_tempo(max_elab_time)}  minuti:secondi:millisecondi) for {row} rows")
            avg_time = [time/5 for time in df["Time"]]
            print(f"AVG time for entry: {np.mean(avg_time)} ms C.I 95%:{self.__confidence_interval_calculation(avg_time)};({self.__millisecondi_in_tempo(int(np.mean(avg_time)))}  minuti:secondi:millisecondi)")

        def loadExcel(self,excel_path): #Sincera che l'excel a cui faccio riferimento ha il giusto formato (riporta le colonne che mi aspetto da un excel generato da questo manager)
            df = pd.read_excel(excel_path,engine='openpyxl')
            all_colums_in_file = all(item in df.columns for item in COLUMS)
            if(all_colums_in_file):
                self.excel_to_analyze = df
            else:
                raise Exception("[ERROR]: wrong excel format")
            
        def getHEImpact(self): #Estrapola le statistiche dell'excel a cui facciamo riferimento (numero di EM, media ED e Meteor etc)
            number_of_records = len(self.excel_to_analyze)
            print(f"Number of records: {number_of_records}")
            h_e_number_of_ones = (self.excel_to_analyze["HUMAN_E"] == 1).sum()
            number_one_before = (self.excel_to_analyze["EM_M"] == 1).sum()

            print(f"Human evaluation statistics: ones: {h_e_number_of_ones} zeros: {number_of_records-h_e_number_of_ones}")
            print(f"Human evaluation impact: ones_before: {number_one_before} ones_after: {h_e_number_of_ones} human evaluation impact: {h_e_number_of_ones-number_one_before}")
        
        def getMetricsStatistics(self):
            print(f"Meteor statistics, mean: {self.excel_to_analyze["METEOR_M"].mean()} std_dev: {self.excel_to_analyze["METEOR_M"].std()}")

        def createExcel(self):
            df = pd.DataFrame()
            in_text = []
            refs_text = []
            hyps_text = []
            with open(self.req_path, 'r') as file:
                line = file.readline().strip()  
                while line:
                    in_text.append(line)
                    line = file.readline().strip()  
            with open(self.refs_path, 'r') as file:
                line = file.readline().strip()   
                while line:
                    refs_text.append(line)
                    line = file.readline().strip()    
            with open(self.model_output_path, 'r') as file:
                line = file.readline().strip()  
                while line:
                    hyps_text.append(line)
                    line = file.readline().strip()    
            self.m_m.load_hyps(hyps_text)
            self.m_m.load_refs(refs_text)
            df['IN'] = in_text
            df['REFS'] = refs_text
            df['HYPS'] = hyps_text
            df['EM_M'] =  self.m_m.calc_EM()
            df['ED_M'] = self.m_m.calc_ed()
            df['METEOR_M'] = self.m_m.calc_meteor()
            df['HUMAN_E'] = df['EM_M']
            df.to_excel(self.excel_name,index=False)
        


    #C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Results\Open-source-models\Open-source-models\Open-source-models\CodeGen\finetuned\test-2024-07-06-23-49\hyps.txt
    #AnalisiCodeGen