from MenuFunction import *


def statisticsMenu():
    print("Which statistics would you like to perform ? \n\n")
    print("0. Go back")
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
    print("12. Model evaluation on difficult category")
    print("13. Correlation on category")
    print("Other. Exit")
    choice = int(input())
    switch_statistics.get(choice,default)()

def plotMenu():
    print("Which plot would you like to draw ? \n\n")
    print("0. Go back")
    print("1. Resisual plot (metric_avg - accuracy_he)")
    print("2. Category distribution")
    print("3. Models evaluation on difficult categories")
    print("4. Category Token Plot")
    choice = int(input())
    switch_plot.get(choice,default)()

def menu():
    while(1):
        print("Which operation would you like to do ? \n\n")
        print("1. Create excel for analysis")
        print("2. Get Excel Statistics")
        print("3. TestSet distribution")
        print("4. Plots")
        print("Other. Exit")
        choice = int(input())
        switch_main_menu.get(choice,default)()

switch_statistics = {
    0: menu,
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
    11: commonFailureCategPlt,
    12: ModelEvalDiffiCateg,
    13: correlationForCategoryToken
}

switch_plot = {
    0: menu,
    1: res_plot,
    2: cat_plot,
    3: modelEvalDiffCateg_plot,
    4: CategTokenPlt,
    5: plotCategoryDifficulty
}


switch_main_menu = {
    1: excelCreation,
    2: statisticsMenu,
    3: TestSetDistribution,
    4: plotMenu
}


def default():
    exit()


if __name__ == "__main__":
   menu()