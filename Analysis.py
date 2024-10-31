
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

evaluation_master = Evaluation_master(None,None,None,None)
current_excel_analysis = None


def excelCreation():
    global evaluation_master
    print("Insert model output path")
    model_out_path = input()
    print("Insert excel name")
    excel_name = input()
    evaluation_master.setAllParameters(REQUEST_PATH,model_out_path,REFS_PATH,excel_name)
    evaluation_master.createExcel()

def loadStatisticsExcel():
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
    print("Insert evaluation time file path")
    evaluation_t_file_path = input()
    rows,max_elab_time_ms,max_elab_time,avg_time_ms,c_i,avg_time = evaluation_master.evaluationTimeAnalysis(evaluation_t_file_path)
    for row in rows:
        print(f"Max Time: {max_elab_time_ms} ms ({max_elab_time}  minuti:secondi:millisecondi) for {row} rows")
        
    print(f"AVG time for entry: {avg_time_ms} ms C.I 95%:{c_i};({avg_time}  minuti:secondi:millisecondi)")

    
def correlationAnalysis():
    evaluation_master.correlationAnalysis()

def he_impact():
   evaluation_master.getHEImpact()

def metrics_statistics():
   evaluation_master.getMetricsStatistics()

def rom_phenomena():
    evaluation_master.rom_phenomenaAnalisis()

def model_acc():
    print(f"pre_HE: {evaluation_master.model_accuracy_pre_HE()} post HE: {evaluation_master.model_accuracy_HE()}")

def categ_analysis():
    print("Insert Test in category distribution file path")
    categ_distr_path = input()
    print("Insert Category legend file path")
    categ_legend_path = input()
    score_dict,cat_dict = evaluation_master.categoryAnalysis(categ_distr_path,categ_legend_path)    
    for score in score_dict.keys():
        print(f"{cat_dict[score]} : {score_dict[score]} ")

def time_categ_analysis():
    print("Insert Test in category distribution file path")
    categ_distr_path = input()
    print("Insert Category legend file path")
    categ_legend_path = input()
    print("Insert Time file")
    time_file_path = input()
    max_time_ms,row_categ = evaluation_master.categoryTimeAnalysis(categ_distr_path,categ_legend_path,time_file_path)
    print(f"Max time {max_time_ms} for: ")
    for row in row_categ:
        print(f"{row[0]} : {row[1]}")

    
def default():
    exit()

def statisticsMenu():
    print("Which statistics would you like to perform ? \n\n")
    print(f"1. Change excel to analyze actually: {current_excel_analysis}")
    print("2. Correlation analysis analysis with Human evaluation")
    print("3. Get human evaluation impact")
    print("4. Get metrics statistics")
    print("5. Get rom fenomena count")
    print("6. Get evaluation time statistics")
    print("7. Model accuracy pre and post HE")
    print("8. Category Analysis")
    print("9. Time analysis for category")
    print("Other. Exit")
    choice = int(input())
    switch_statistics.get(choice,default)()


switch_statistics = {
    1: loadStatisticsExcel,
    2: correlationAnalysis,
    3: he_impact,
    4: metrics_statistics,
    5: rom_phenomena,
    6: evaluationTimeAnalysis,
    7: model_acc,
    8: categ_analysis,
    9: time_categ_analysis
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