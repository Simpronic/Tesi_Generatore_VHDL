
"""! @brief Class that let you perform the analysis on file."""

import pandas as pd
from Metrics_manager import *
from datetime import datetime
from scipy.stats import spearmanr, kendalltau,pearsonr
import scipy.stats as st 
import numpy as np
import configparser


class Evaluation_master:
        """! The Evaluation_master class.
        Defines operations that you can do for Analysis purposes.
        """
        def __init__(self,requests,hyps,refs,excel_name):
            """! The Evaluation_master base class initializer.
                @param requests: file path with input model request.
                @param hyps: file path with answers of the model.
                @param refs: file path with correct answers.
                @param excel_name: excel file name.
                @return  None
            """
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
            self.config_p = configparser.ConfigParser()
            self.config_p.read('config.cfg')

        def __confidence_interval_t_student(self,data):

            """! Calculates the confidence interval for data series in relation with t-student distribution.
                @param data: data series.
                @return  confidence_interval
            """
            return st.t.interval(confidence=0.95, df=len(data)-1,loc=np.mean(data),scale=st.sem(data)) 
            
        def __confidence_interval_normal(self,data):
            """! Calculates the confidence interval for data series in relation with normal distribution.
                @param data: data series.
                @return  confidence_interval
            """
            return st.norm.interval(confidence=0.95,loc=np.mean(data),scale=st.sem(data)) 
        
        def __confidence_interval_calculation(self,data):
            """! Calculates the confidence interval for data series by using t-student or normal based on the samples.
                @param data: data series.
                @return  [lower_bound,upper_bound]
            """
            if(len(data) < 30):
                ub,lb= self.__confidence_interval_t_student(data)
            else:
                ub,lb = self.__confidence_interval_normal(data)
            return f"[{lb},{ub}]"
            
        def __time_to_ms(self,time):
            """! Converts a time in minutes:seconds:milliseconds in milliseconds only
                @param time: time to convert.
                @return milliseconds
            """
            minuti, secondi, millisecondi = map(int, time.split(':'))
            totale_millisecondi = (minuti * 60 * 1000) + (secondi * 1000) + millisecondi
            return totale_millisecondi
        
        def __max_elab_time_and_rows(self,analisis_df):
            """! Calculates the max evaluation time
                @param analisis_df: the dataframe with times recorded during HE.
                @return elab_time_max,rows
            """
            elab_time_max = analisis_df["Time"].max()
            rows = analisis_df[analisis_df["Time"] == elab_time_max]["Righe"]
            return elab_time_max, rows
        
        def __millisecondi_in_tempo(self,millisecondi):
            """! Converts a time in milliseconds in minutes:seconds:milliseconds 
                @param milliseconds: time to convert.
                @return f"{ore}:{minuti}:{secondi}:{millisecondi:.0f}"
            """
            ore = int(millisecondi // 3600000)
            millisecondi = millisecondi % 3600000
            minuti = int(millisecondi // 60000)
            millisecondi = millisecondi % 60000
            secondi = int(millisecondi // 1000)
            millisecondi = millisecondi % 1000
            return f"{ore}:{minuti}:{secondi}:{millisecondi:.0f}" 
        
        def model_accuracy_HE(self):
            """! Calculates the model accuracy post-HE by doing number_of_ones/total_number_of_records
                @note You need to load the excel to analyze first
                @param None
                @return accuracy
            """
            return (((self.excel_to_analyze["HUMAN_E"] == 1).sum())/len(self.excel_to_analyze["HUMAN_E"]))
        
        def model_accuracy_pre_HE(self):
            """! Calculates the model accuracy pre-HE by doing number_of_ones/total_number_of_records
                @note You need to load the excel to analyze first
                @param None
                @return accuracy
            """
            return (((self.excel_to_analyze["EM_M"] == 1).sum())/len(self.excel_to_analyze["EM_M"]))
        
        def setAllParameters(self,requests,hyps,refs,excel_name):
            """! Let you set the parameters after the initialization
                @param requests
                @param hyps
                @param refs
                @param excel_name
                @return None
            """
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
            """! Create a dictionary for identify the category using a number 
                @param category_legend_path: the path of the legend file
                @return categ_dict
            """
            categ_dict = dict()
            with open(category_legend_path, "r") as file:
                for linea in file:
                    linea = linea.strip()
                    elem = linea.split(",")
                    categ_dict[elem[0].strip()] = elem[1].strip()
            return categ_dict
        
        def __getCategDistr(self,category_distr_file_path):
            """! Create a vector for category distribution
                @param category_distr_file_path: the path of the distribution of Test In file 
                @return df["Category"]
            """
            df = pd.read_excel(category_distr_file_path)
            return df["Category"]
        
        def __categoryScore(self,categs,cat_distr):
            """! Calculate the score for each category 
                @note You need to load the excel to analyze first
                @param categs: dictionary of caategory 
                @param cat_distr: category distribution file
                @return categ_score: dictionary of scores
            """
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
        

        def __CommonFailurecategoryScore(self,categs,cat_distr,common_failure_csv):
            """! Calculate the score for each category 
                @note You need to load the excel to analyze first
                @param categs: dictionary of caategory 
                @param cat_distr: category distribution file
                @return categ_score: dictionary of scores
            """
            categ_score = dict()
            for categ in categs:
                categ_fail = 0
                for i in range(0,len(common_failure_csv)):
                    if(str(cat_distr[int(common_failure_csv["Righe"][i])]) == categ):
                        categ_fail += int(common_failure_csv["FAIL_TIME"][i])
                categ_score[categ] = categ_fail           
            return categ_score
        
        def categoryAnalysis(self):
            """! Driver for category analysis 
                @note You need to load the excel to analyze first
                @param None
                @return score_dict,cat_dict
            """
            cat_dict = self.__createCategDict(self.config_p["DEFAULT"]["category_legend"])
            cat_distr = self.__getCategDistr(self.config_p["DEFAULT"]["category_path"])
            score_dict = self.__categoryScore(cat_dict.keys(),cat_distr)
            return score_dict,cat_dict
        
        def categoryTimeAnalysis(self,tim_file_path):
            """! Driver for category Time analysis 
                @note You need to load the excel to analyze first
                @param tim_file_path
                @return max_elab_time_ms,row_categ : maximum elaboration time and a dictionary with the correspondence
            """
            cat_dict = self.__createCategDict(self.config_p["DEFAULT"]["category_legend"])
            cat_distr = self.__getCategDistr(self.config_p["DEFAULT"]["category_path"])
            df = pd.read_csv(tim_file_path, header=None, names=['Righe', 'Time'], quotechar='"')
            times = [self.__time_to_ms(time) for time in df["Time"]]
            df["Time"] = times
            rows,max_elab_time_ms,max_elab_time,avg_time_ms,c_i,avg_time,total_evaluation_time= self.evaluationTimeAnalysis(tim_file_path)
            row_categ = []
            for row in rows:
                lines = row.split(",")
                for line in lines:
                    categ_name = cat_dict[str(cat_distr[int(line)-2])]
                    row_categ.append([line,categ_name])
            return max_elab_time_ms,row_categ


        def clearExcel_to_analyze(self):
            """! Clears the excel 
                @param None
                @return none
            """
            self.excel_to_analyze = None

        def commonFailureAnalysis(self,f_p):
            """! Makes analysis on common models failure
                @Note all the classification file must be in a folder
                @param f_p: path to the analysis folder
                @return failure_array_count
            """
            file_xlsx = [file for file in os.listdir(f_p) if file.endswith(".xlsx")]
            file_xlsx = [os.path.join(f_p, file) for file in file_xlsx]
            file_len = len(pd.read_excel(file_xlsx[0]))
            failure_array = [0] * file_len
            for file in file_xlsx:
                df = pd.read_excel(file)
                for i in range(len(failure_array)):
                    if(df["HUMAN_E"][i] == 0):
                        failure_array[i] += 1
            return failure_array
        
        def commonFailureAnalysis_category(self,f_p):
            """! Makes analysis on common models failure gruping by category
                @Note you need to generate the common failure csv
                @param f_p: path to failure csv file
                @return category_failure_array_count
                @return cat_dict
            """
            cat_dict = self.__createCategDict(self.config_p["DEFAULT"]["category_legend"])
            cat_distr = self.__getCategDistr(self.config_p["DEFAULT"]["category_path"])
            common_failure_csv_file = pd.read_csv(f_p, header=None, names=['Righe', 'FAIL_TIME'], quotechar='"').drop(0)
            common_failure_csv_file.reset_index(drop=True, inplace=True)
            common_failure_dict = self.__CommonFailurecategoryScore(cat_dict,cat_distr,common_failure_csv_file)
            return common_failure_dict,cat_dict

        def globalCorrelation(self,gdf,metric):
            """! Makes the global correlation analysis with the metric with Kendall, Spearman,pearson
                @param Metric: the name of the metric into the xlsx
                @param gdf: the global dataframe resulting from the concatenation of all the files into the specified folder 
                @return kendall,kendall_p,spearman,spearman_p,pearson,pearson_p
            """
            ex_df =  self.excel_to_analyze
            self.excel_to_analyze = gdf
            kendall_corr,kendall_p_value,spearman_corr,spearman_p_value,pearson_corr, pearson_p_value = self.correlationAnalysis(metric)
            self.excel_to_analyze = ex_df
            return kendall_corr,kendall_p_value,spearman_corr,spearman_p_value,pearson_corr, pearson_p_value

        def correlationAnalysis(self,metric): #Assumo che il df sia stato caricato
            """! Makes the correlation analysis with the metric with Kendall, Spearman,pearson
                @note You need to load the excel to analyze first
                @param Metric: the name of the metric into the xlsx
                @return kendall,kendall_p,spearman,spearman_p,pearson,pearson_p
            """
            print(f"Analizyng {metric}...")
            he_m = self.excel_to_analyze["HUMAN_E"]
            spearman_corr, spearman_p_value = spearmanr(he_m, self.excel_to_analyze[metric])
            kendall_corr, kendall_p_value = kendalltau(he_m, self.excel_to_analyze[metric])
            pearson_corr, pearson_p_value = pearsonr(he_m, self.excel_to_analyze[metric])
            return kendall_corr,kendall_p_value,spearman_corr,spearman_p_value,pearson_corr, pearson_p_value

        def __calculateAVGTime(self,time_df):
            """! Calculate th average time in a time series
                @param time_df
                @return time_avg: array of averages of group of 5 row 
            """
            return [time/5 for time in time_df["Time"]]
        
        def __TotalEvaluationTime(self,df):
            """! Stimate the total time taken to evaluate a output model, sum over the time recorded and sum the average time for the not recorded rows
                @param time_df
                @return time_avg: array of averages of group of 5 row 
            """
            total_evaluated_entry = 5*len(df)
            avg_time_for_entry = np.mean(self.__calculateAVGTime(df))
            h_e_number_of_ones,number_of_records,number_one_before = self.getHEImpact()
            total_zeros = number_of_records-number_one_before
            mean_entry_evaluation = avg_time_for_entry*(total_zeros-total_evaluated_entry)
            evaluated_time = df["Time"].sum()

            return self.__millisecondi_in_tempo(evaluated_time+mean_entry_evaluation)
            


        def evaluationTimeAnalysis(self,evaluation_file_times):
            """! Performs the evaluation time analysis 
                @param evaluation_file_times
                @return rows,max_elab_time,max_elab_time_ms,avg_time,c_i,avg_time_ms,total_evaluation_time
            """
            df = pd.read_csv(evaluation_file_times, header=None, names=['Righe', 'Time'], quotechar='"')
            times = [self.__time_to_ms(time) for time in df["Time"]]
            df["Time"] = times
            max_elab_time,rows = self.__max_elab_time_and_rows(df)
            total_evaluation_time = self.__TotalEvaluationTime(df)
            return rows,max_elab_time,self.__millisecondi_in_tempo(max_elab_time),np.mean(self.__calculateAVGTime(df)),self.__confidence_interval_calculation(self.__calculateAVGTime(df)),self.__millisecondi_in_tempo(int(np.mean(self.__calculateAVGTime(df)))),total_evaluation_time
           
        def loadExcel(self,excel_path): #Sincera che l'excel a cui faccio riferimento ha il giusto formato (riporta le colonne che mi aspetto da un excel generato da questo manager)
            """! Loads the excel for analysis
                @note can return an eexception if the format is wrong
                @param excel_path
                @return None
            """
            df = pd.read_excel(excel_path,engine='openpyxl')
            cols = self.config_p.get("STATISTICS","colums").split(",")
            all_colums_in_file = all(item in df.columns for item in cols)
            if(all_colums_in_file):
                self.excel_to_analyze = df
            else:
                raise Exception("[ERROR]: wrong excel format")
            
        def getHEImpact(self): #Estrapola le statistiche dell'excel a cui facciamo riferimento (numero di EM, media ED e Meteor etc)
            """! Prints the HE impact on the LLM output file
                @note You need to load the excel to analyze first
                @param None
                @return h_e_number_of_ones,number_of_records,number_one_before
            """
            number_of_records = len(self.excel_to_analyze)
            h_e_number_of_ones = (self.excel_to_analyze["HUMAN_E"] == 1).sum()
            number_one_before = (self.excel_to_analyze["EM_M"] == 1).sum()
            return h_e_number_of_ones,number_of_records,number_one_before
    
        
        def getMetricsStatistics(self):
            """! Prints the Other metrics statistics like std. dev, average.
                @note You need to load the excel to analyze first
                @param None
                @return statistics_dict: key -> Array of statistics, [0] --> mean, [1] --> std, [2] --> median
            """
            statistics_dict = {}
            metrics = self.config_p.get("STATISTICS","metrics_name").split(",")
            for metric in metrics:
                statistics_dict.setdefault(metric,[]).append(self.excel_to_analyze[metric].mean())
                statistics_dict.setdefault(metric,[]).append(self.excel_to_analyze[metric].std())
                statistics_dict.setdefault(metric,[]).append(self.excel_to_analyze[metric].median())
            return statistics_dict

        def createExcel(self):
            """! Create the excel for doing the analysis
                @param None
                @return None
            """
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
            df['CRYSTALB_M'] = self.m_m.calc_crystalBLEU(re_compute_ngrams=False)
            df['SACREB_M'] = self.m_m.calc_sacreBLEU()
            df['ROUGE_M'] = self.m_m.calc_rouge(self.model_output_path,self.refs_path)
            df['HUMAN_E'] = df['EM_M']
            df.to_excel(self.excel_name,index=False)

        def category_distribution(self,name):
            input_prompt = []
            with open(self.config_p.get("DEFAULT","data_in"), "r") as file:
                # Leggi il file riga per riga
                for linea in file:
                    # Rimuove eventuali spazi bianchi (come newline) alla fine della riga
                    linea = linea.strip()
                    input_prompt.append(linea)
            category_distr = []
            with open(self.config_p.get("DEFAULT","category_distr_Dataset"), "r") as file:
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
            with open(self.config_p.get("DEFAULT","test_in_path"), "r") as file:
                # Leggi il file riga per riga
                for linea in file:
                    # Rimuove eventuali spazi bianchi (come newline) alla fine della riga
                    linea = linea.strip()
                    test_in_data.append(linea)
            category_data_for_test = [0] * len(test_in_data)
            for i in range(0,len(test_in_data)):
                category_data_for_test[i] = df["Category"][df.loc[df["Prompt"] == test_in_data[i]].index.tolist()].to_list()[0]
            df_test_in = pd.DataFrame()
            df_test_in["Prompt"] = test_in_data
            df_test_in["Category"] = category_data_for_test
            df_test_in.to_excel(name+".xlsx",index=False)