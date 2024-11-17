
"""! @brief Defines the analysis operation that you can performa for this project."""
##
# @file Analysis.py
#
# @brief Defines the analysis operation that you can performa for this project.
#
# @section analysis.py Description
# Defines the analysis that you can do with the framework.
# - Create excel for analysis: help you create an excel for human evaluation analysis
# - Get Excel Statistics: Perform analysis on the outputs, in the documentation you can find functions for analysis
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
config = configparser.ConfigParser()
config.read('config.cfg')

def excelCreation():
    """! Driver for excel creation
        @param None
        @return None
    """
    global evaluation_master
    print("Insert model output path")
    model_out_path = input()
    print("Insert excel name")
    excel_name = input()
    evaluation_master.setAllParameters(config['DEFAULT']['test_in_path'],model_out_path,config['DEFAULT']['refs_path'],excel_name)
    evaluation_master.createExcel()

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
    print("Insert evaluation time file path")
    evaluation_t_file_path = input()
    rows,max_elab_time_ms,max_elab_time,avg_time_ms,c_i,avg_time,total_evaluation_time = evaluation_master.evaluationTimeAnalysis(evaluation_t_file_path)
    for row in rows:
        print(f"Max Time: {max_elab_time_ms} ms ({max_elab_time}  ore:minuti:secondi:millisecondi) for {row} rows")
        
    print(f"AVG time for entry: {avg_time_ms} ms C.I 95%:{c_i};({avg_time}  ore:minuti:secondi:millisecondi)")
    print(f"Total evaluation time for model: {total_evaluation_time}")

    
def correlationAnalysis():
    """! Driver for Correlation analysis
        @param None
        @return None
    """
    metrics = config.get("STATISTICS","metrics_name").split(",")
    for metric in metrics:
        kendall_corr,kendall_p_value,spearman_corr,spearman_p_value,pearson_corr, pearson_p_value = evaluation_master.correlationAnalysis(metric)

        print("Spearman Correlation:", spearman_corr)
        print("Spearman P-value:", spearman_p_value)

        print("Kendall Correlation:", kendall_corr)
        print("Kendall P-value:", kendall_p_value)

        print("Pearson Correlation:", pearson_corr)
        print("Pearson P-value:", pearson_p_value)

    print("\n\n")

def he_impact():
    """! Driver for he impact analysis
        @param None
        @return None
    """
    h_e_number_of_ones,number_of_records,number_one_before = evaluation_master.getHEImpact()
    print(f"Number of records: {number_of_records}")
    print(f"Human evaluation statistics: ones: {h_e_number_of_ones} zeros: {number_of_records-h_e_number_of_ones}")
    print(f"Human evaluation impact: ones_before: {number_one_before} ones_after: {h_e_number_of_ones} human evaluation impact: {h_e_number_of_ones-number_one_before}")

def metrics_statistics():
    """! Driver for metric statistics analysis
        @param None
        @return None
    """
    metric_dict = evaluation_master.getMetricsStatistics()
    for key in metric_dict.keys():
       print(f"For metric {key}: \n")
       print(f"mean: {metric_dict[key][0]}")
       print(f"std: {metric_dict[key][1]}")
       print(f"median: {metric_dict[key][2]} \n")
       

def model_acc():
    """! Driver for model accuracy (number_of_ones/number_of_records) analysis
        @param None
        @return None
    """
    print(f"pre_HE: {evaluation_master.model_accuracy_pre_HE()} post HE: {evaluation_master.model_accuracy_HE()}")

def categ_analysis():
    """! Driver for category analysis
        @param None
        @return None
    """
    score_dict,cat_dict = evaluation_master.categoryAnalysis()    
    for score in score_dict.keys():
        print(f"{cat_dict[score]} : {score_dict[score]} ")

def time_categ_analysis():
    """! Driver for category time analysis
        @param None
        @return None
    """
    time_file_path = input()
    max_time_ms,row_categ = evaluation_master.categoryTimeAnalysis(time_file_path)
    print(f"Max time {max_time_ms} for: ")
    for row in row_categ:
        print(f"{row[0]} : {row[1]}")

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
    print("To perform global correlation put all the xlsx file in one folder and then enter the folder path\n\n")
    print("Folder path: ")
    f_p = input()
    g_df = createglobaldf(f_p)
    metrics = config.get("STATISTICS","metrics_name").split(",")
    for metric in metrics:
        kendall_corr,kendall_p_value,spearman_corr,spearman_p_value,pearson_corr, pearson_p_value = evaluation_master.globalCorrelation(g_df,metric)
        print("Spearman Correlation:", spearman_corr)
        print("Spearman P-value:", spearman_p_value)

        print("Kendall Correlation:", kendall_corr)
        print("Kendall P-value:", kendall_p_value)

        print("Pearson Correlation:", pearson_corr)
        print("Pearson P-value:", pearson_p_value)

        print("\n\n")
    
def commonFailure():
    """! Driver for common failure analysis
        @param None
        @return None
    """
    print("To perform common failure analysis put all the xlsx file in one folder and then enter the folder path\n\n")
    print("Folder path: ")
    f_p = input()
    failure_array = evaluation_master.commonFailureAnalysis(f_p)
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
    print("Insert th path to common failure csv file")
    fp = input()
    common_failure_dict,cat_dict = evaluation_master.commonFailureAnalysis_category(fp)
    plot_common_f(cat_dict.values(),common_failure_dict.values(),"Common_failures_categ","Failures","Category","Common Failuers Category",'h')

def plot_common_f(indices,values,name,xlable_n,y_label_n,h_title,h_type=None):
    """! Utility to plot histograms
        @param indices,values,name
        @param h_type: histogram type h for horizontal otherwise is standard
        @return None
    """
    plt.figure(figsize=(30, 15))
    if(h_type == 'h'):
        plt.barh(indices, values, color='skyblue', edgecolor='black',color='salmon')
    else:
        plt.bar(indices, values, color='skyblue', edgecolor='black',color='salmon')
    plt.xticks(rotation=45)
    plt.title(h_title)
    plt.xlabel(xlable_n)
    plt.ylabel(y_label_n)
    plt.savefig(name+".png")

def default():
    exit()


def statisticsMenu():
    print("Which statistics would you like to perform ? \n\n")
    print(f"1. Change excel to analyze actually: {current_excel_analysis}")
    print("2. Correlation analysis analysis with Human evaluation")
    print("3. Get human evaluation impact")
    print("4. Get metrics statistics")
    print("5. Get evaluation time statistics")
    print("6. Model accuracy pre and post HE")
    print("7. Category Analysis")
    print("8. Time analysis for category")
    print("9. Global correlation analysis")
    print("10. Common Failure analysis")
    print("11. Common Failure analysis (Category)")
    print("Other. Exit")
    choice = int(input())
    switch_statistics.get(choice,default)()


switch_statistics = {
    1: loadStatisticsExcel,
    2: correlationAnalysis,
    3: he_impact,
    4: metrics_statistics,
    5: evaluationTimeAnalysis,
    6: model_acc,
    7: categ_analysis,
    8: time_categ_analysis,
    9: globalCorrelation,
    10: commonFailure,
    11: commonFailureCateg
}



switch_main_menu = {
    1: excelCreation,
    2: statisticsMenu
}


def menu():
    while(1):
        print("Which operation would you like to do ? \n\n")
        print("1. Create excel for analysis")
        print("2. Get Excel Statistics")
        print("Other. Exit")
        choice = int(input())
        switch_main_menu.get(choice,default)()


if __name__ == "__main__":
   menu()