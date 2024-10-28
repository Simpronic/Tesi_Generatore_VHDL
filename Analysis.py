from Excel_manager import *

excel_creator = Excel_creator(None,None,None,None)
current_excel_analysis = None

def excelCreation():
    global excel_creator
    print("Insert model output path")
    model_out_path = input()
    print("Insert excel name")
    excel_name = input()
    excel_creator.setAllParameters(REQUEST_PATH,model_out_path,REFS_PATH,excel_name)
    excel_creator.createExcel()

def loadStatisticsExcel():
    global current_excel_analysis
    print("Insert excel path")
    excel_path = input()
    if(len(excel_path) == 0):
        current_excel_analysis = None
        excel_creator.clearExcel_to_analyze()
    else:
        current_excel_analysis = os.path.basename(excel_path)
        try:
            excel_creator.loadExcel(excel_path)
        except Exception as e:
            print(e)

def evaluationTimeAnalysis():
    print("Insert evaluation time file path")
    evaluation_t_file_path = input()
    excel_creator.evaluationTimeAnalysis(evaluation_t_file_path)
    
def correlationAnalysis():
    excel_creator.correlationAnalysis()

def he_impact():
   excel_creator.getHEImpact()

def metrics_statistics():
   excel_creator.getMetricsStatistics()

def rom_phenomena():
    excel_creator.rom_phenomenaAnalisis()

def model_acc():
    print(f"pre_HE: {excel_creator.model_accuracy_pre_HE()} post HE: {excel_creator.model_accuracy_HE()}")

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
    7: model_acc
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