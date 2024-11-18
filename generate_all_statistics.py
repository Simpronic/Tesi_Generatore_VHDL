"""! @brief Defines the analysis operation that you can performa for this project."""
##
# @file generate_all_statistics.py
#
# @brief Driver to perform all the statistical analysis on the input file
#
# @section generate_all_statistics.py Description
# Driver to perform all the statistical analysis on the input file and writes them on txt file
#
# @section note_analysis Notes
# - Comments are Doxygen compatible.
#
#
# @section author_sensors Author(s)
# - Created by Marco Di Fiandra on 29/10/2024.
# - Modified by Marco Di Fiandra on 29/10/2024.

from Evaluation_manager import *
import configparser
import os
import csv
import matplotlib.pyplot as plt

evaluation_master = Evaluation_master(None,None,None,None)
current_excel_analysis = None
evaluation_t_file_path = None
f_p = None
xlsx_f_p = None
failure_file_p = "Common_failure.csv"
config = configparser.ConfigParser()
txt_namefile = None
config.read('config.cfg')


def loadStatisticsExcel():
    """! Loads into evaluation master the xlsx file to perform the analysis
        @param None
        @return None
    """
    global current_excel_analysis
    print("Insert excel path")
    excel_path = input()
    if(len(excel_path) == 0):
        current_excel_analysis = None
        evaluation_master.clearExcel_to_analyze()
    else:
        current_excel_analysis = os.path.basename(excel_path)
        try:
            evaluation_master.loadExcel(excel_path)
        except Exception as e:
            print(e)

def evaluationTimeAnalysis():
    """! Driver for Time analysis
        @param None
        @return None
    """
    global evaluation_t_file_path
    rows,max_elab_time_ms,max_elab_time,avg_time_ms,c_i,avg_time,total_evaluation_time = evaluation_master.evaluationTimeAnalysis(evaluation_t_file_path)
    with open(txt_namefile, 'a') as file:
        for row in rows:
            file.write(f"Max Time: {max_elab_time_ms} ms ({max_elab_time}  ore:minuti:secondi:millisecondi) for {row} rows\n")
        
        file.write(f"AVG time for entry: {avg_time_ms} ms C.I 95%:{c_i};({avg_time}  ore:minuti:secondi:millisecondi) \n")
        file.write(f"Total evaluation time for model: {total_evaluation_time} \n")

    
def correlationAnalysis():
    """! Driver for Correlation analysis
        @param None
        @return None
    """
    metrics = config.get("STATISTICS","metrics_name").split(",")
    with open(txt_namefile, 'a') as file:
        for metric in metrics:
            kendall_corr,kendall_p_value,spearman_corr,spearman_p_value,pearson_corr, pearson_p_value = evaluation_master.correlationAnalysis(metric)

            file.write(f"Spearman Correlation: {spearman_corr}\n")
            file.write(f"Spearman P-value: {spearman_p_value}\n")

            file.write(f"Kendall Correlation: {kendall_corr}\n")
            file.write(f"Kendall P-value: {kendall_p_value}\n")

            file.write(f"Pearson Correlation: {pearson_corr} \n")
            file.write(f"Pearson P-value: {pearson_p_value}\n")

            file.write("\n")

def he_impact():
    """! Driver for he impact analysis
        @param None
        @return None
    """
    h_e_number_of_ones,number_of_records,number_one_before = evaluation_master.getHEImpact()
    with open(txt_namefile, 'a') as file:
        file.write(f"Number of records: {number_of_records}\n")
        file.write(f"Human evaluation statistics: ones: {h_e_number_of_ones} zeros: {number_of_records-h_e_number_of_ones}\n")
        file.write(f"Human evaluation impact: ones_before: {number_one_before} ones_after: {h_e_number_of_ones} human evaluation impact: {h_e_number_of_ones-number_one_before}\n")
        metric_statistics = evaluation_master.getMetricsStatistics()
        partial_sum = 0
        metrics = config.get("STATISTICS","metrics_name").split(",")
        for metric in metrics:
            partial_sum+=float(metric_statistics[metric][0])
        avg = partial_sum/len(metrics)
        he_accuracy = evaluation_master.model_accuracy_HE()
        file.write(f" metrics average: {avg} he accuracy: {he_accuracy} residual: {avg-he_accuracy} absolute Residual: {abs(avg-he_accuracy)}\n")

def metrics_statistics():
    """! Driver for metric statistics analysis
        @param None
        @return None
    """
    metric_dict = evaluation_master.getMetricsStatistics()
    with open(txt_namefile, 'a') as file:
        for key in metric_dict.keys():
            file.write(f"For metric {key}: \n")
            file.write(f"mean: {metric_dict[key][0]}\n")
            file.write(f"std: {metric_dict[key][1]}\n")
            file.write(f"median: {metric_dict[key][2]} \n")
       

def model_acc():
    """! Driver for model accuracy (number_of_ones/number_of_records) analysis
        @param None
        @return None
    """
    with open(txt_namefile, 'a') as file:
        file.write(f"pre_HE: {evaluation_master.model_accuracy_pre_HE()} post HE: {evaluation_master.model_accuracy_HE()} \n")

def categ_analysis():
    """! Driver for category analysis
        @param None
        @return None
    """
    score_dict,cat_dict = evaluation_master.categoryAnalysis() 
    with open(txt_namefile, 'a') as file:   
        for score in score_dict.keys():
            file.write(f"{cat_dict[score]} : {score_dict[score]}\n")
        file.write("\n")

def time_categ_analysis():
    """! Driver for category time analysis
        @param None
        @return None
    """
    global evaluation_t_file_path
    max_time_ms,row_categ = evaluation_master.categoryTimeAnalysis(evaluation_t_file_path)
    with open(txt_namefile, 'a') as file:  
        file.write(f"Max time {max_time_ms} for: ")
        for row in row_categ:
            file.write(f"{row[0]} : {row[1]}")
        file.write("\n")

def createglobaldf(f_p):
    """! Driver for creating a big dataframe to perform global correlation analysis
        @param f_p: folder path, the folder where we can find all the xlsx analysis files
        @return gdf: global data frame
    """
    gdf = pd.DataFrame()
    dati = []
    file_xlsx = [file for file in os.listdir(f_p) if file.endswith(".xlsx")]
    file_xlsx = [os.path.join(f_p, file) for file in file_xlsx]
    for file in file_xlsx:
        df = pd.read_excel(file,engine='openpyxl')
        dati.append(df)
    gdf = pd.concat(dati,ignore_index=True)

    return gdf

def globalCorrelation():
    """! Driver for global correlation analysis
        @param None
        @return None
    """
    global f_p
    g_df = createglobaldf(f_p)
    metrics = config.get("STATISTICS","metrics_name").split(",")
    with open(txt_namefile, 'a') as file:  
        for metric in metrics:
            kendall_corr,kendall_p_value,spearman_corr,spearman_p_value,pearson_corr, pearson_p_value = evaluation_master.globalCorrelation(g_df,metric)
            file.write(f"Spearman Correlation: {spearman_corr}\n")
            file.write(f"Spearman P-value: {spearman_p_value}\n")

            file.write(f"Kendall Correlation: {kendall_corr}\n")
            file.write(f"Kendall P-value: {kendall_p_value}\n")

            file.write(f"Pearson Correlation: {pearson_corr}\n")
            file.write(f"Pearson P-value: {pearson_p_value}\n")

            file.write("\n")
        
def commonFailure():
    """! Driver for common failure analysis
        @param None
        @return None
    """
    global xlsx_f_p
    failure_array = evaluation_master.commonFailureAnalysis(xlsx_f_p)
    not_zero_values = [(index, value) for index, value in enumerate(failure_array) if value != 0]
    ordered_not_zero_values =sorted(not_zero_values, key=lambda x: x[1],reverse=True) 
    indexes = [str(index) for index, value in ordered_not_zero_values]
    values = [value for index, value in ordered_not_zero_values]
    print("Writing file csv ....")
    with open("Common_failure.csv",mode=
              'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Index','Failures'])
        writer.writerows(not_zero_values)
    print("Saving plot...")
    print("Plotting top 20 common failure...")
    print("Saving plot")
    plot_common_f(indexes[0:19],values[0:19],"Common_failures","Row","Number of failure","Common Failuers",None)

def commonFailureCateg():
    global failure_file_p
    common_failure_dict,cat_dict = evaluation_master.commonFailureAnalysis_category(failure_file_p)
    plot_common_f(cat_dict.values(),common_failure_dict.values(),"Common_failures_categ","Failures","Category","Common Failuers Category",'h')

def plot_common_f(indices,values,name,xlable_n,y_label_n,h_title,h_type=None):
    """! Utility to plot histograms
        @param indices,values,name
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
    plt.savefig(name+".png")


if __name__ == "__main__":
    loadStatisticsExcel()
    print("Insert evaluation time file path")
    evaluation_t_file_path = input()
    txt_namefile = os.path.basename(current_excel_analysis).split(".")[0]+"_Full_Analysis.txt"
    print("To perform global correlation put all the xlsx file in one folder and then enter the folder path\n")
    print("Folder path: ")
    f_p = input()
    print("Insert the path of the folder where the xlsx file are located")
    xlsx_f_p = input()
    with open(txt_namefile, 'w'):
        pass  # Non esegue alcuna operazione, ma crea il file
    correlationAnalysis()
    he_impact()
    metrics_statistics()
    evaluationTimeAnalysis()
    categ_analysis()
    commonFailure()
    commonFailureCateg()


