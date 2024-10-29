import pandas as pd
from Metrics_manager import *
from datetime import datetime
from scipy.stats import spearmanr, kendalltau
import scipy.stats as st 
import numpy as np
import pdb

REQUEST_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.in"
REFS_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.out"
COLUMS = {"IN","REFS","HYPS","EM_M","ED_M","METEOR_M","LCS_M","HUMAN_E"}
METRICS_NAME = ["EM_M","ED_M","METEOR_M","LCS_M"]


class Evaluation_master:

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
        
        def model_accuracy_HE(self):
             return (((self.excel_to_analyze["HUMAN_E"] == 1).sum())/len(self.excel_to_analyze["HUMAN_E"]))
        
        def model_accuracy_pre_HE(self):
             return (((self.excel_to_analyze["EM_M"] == 1).sum())/len(self.excel_to_analyze["EM_M"]))
        
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

        def __createCategDict(self,category_legend_path):
            categ_dict = dict()
            with open(category_legend_path, "r") as file:
                for linea in file:
                    linea = linea.strip()
                    elem = linea.split(",")
                    categ_dict[elem[0].strip()] = elem[1].strip()
            return categ_dict
        
        def __getCategDistr(self,category_distr_file_path):
            df = pd.read_excel(category_distr_file_path)
            return df["Category"]
        
        def __categoryScore(self,categs,cat_distr):
            categ_score = dict()
            for categ in categs:
                score = 0
                e_numbers = 0
                for i in range(0,len(cat_distr)):
                    if(cat_distr[i] == int(categ)):
                        e_numbers += 1 
                        score += self.excel_to_analyze["HUMAN_E"][i]
                score = score/e_numbers
                categ_score[categ] = score           
            return categ_score

        
        def categoryAnalysis(self,category_distr_file,category_legend):
            cat_dict = self.__createCategDict(category_legend)
            cat_distr = self.__getCategDistr(category_distr_file)
            score_dict = self.__categoryScore(cat_dict.keys(),cat_distr)
            return score_dict,cat_dict
        
        def categoryTimeAnalysis(self,category_distr_file,category_legend,tim_file_path):
            cat_dict = self.__createCategDict(category_legend)
            cat_distr = self.__getCategDistr(category_distr_file)
            df = pd.read_csv(tim_file_path, header=None, names=['Righe', 'Time'], quotechar='"')
            times = [self.__time_to_ms(time) for time in df["Time"]]
            df["Time"] = times
            rows,max_elab_time_ms,max_elab_time,avg_time_ms,c_i,avg_time= self.evaluationTimeAnalysis(tim_file_path)
            row_categ = []
            for row in rows:
                lines = row.split(",")
                for line in lines:
                    categ_name = cat_dict[str(cat_distr[int(line)-2])]
                    row_categ.append([line,categ_name])
            return max_elab_time_ms,row_categ


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

        def __calculateAVGTime(self,time_df):
            return [time/5 for time in time_df["Time"]]
        
        def evaluationTimeAnalysis(self,evaluation_file_times):
            df = pd.read_csv(evaluation_file_times, header=None, names=['Righe', 'Time'], quotechar='"')
            times = [self.__time_to_ms(time) for time in df["Time"]]
            df["Time"] = times
            max_elab_time,rows = self.__max_elab_time_and_rows(df)
            return rows,max_elab_time,self.__millisecondi_in_tempo(max_elab_time),self.__calculateAVGTime(df),self.__confidence_interval_calculation(self.__calculateAVGTime(df)),self.__millisecondi_in_tempo(int(np.mean(self.__calculateAVGTime(df))))
           
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
            df['LCS_M'] = self.m_m.calc_lcs()
            df['HUMAN_E'] = df['EM_M']
            df.to_excel(self.excel_name,index=False)
        


#C:\Users\marcd\Desktop\Tesi\Work\GitRepo\Tesi_Generatore_VHDL\HE\W_in_progress\AnalisiCodeT5_225.xlsx

#C:\Users\marcd\Desktop\Tesi\Work\GitRepo\Tesi_Generatore_VHDL\Dati_appoggio_analisi\TestInCateg.xlsx

#C:\Users\marcd\Desktop\Tesi\Work\GitRepo\Tesi_Generatore_VHDL\Dati_appoggio_analisi\categories_legend.txt

#C:\Users\marcd\Desktop\Tesi\Work\GitRepo\Tesi_Generatore_VHDL\HE\W_in_progress\Tempi_di_valutazione\Tempi_di_valutazione_CodeT5_220.csv