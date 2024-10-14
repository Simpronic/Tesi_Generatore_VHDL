import pandas as pd
from Metrics_manager import *

REQUEST_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.in"
REFS_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.out"
COLUMS = {"IN","REFS","HYPS","EM_M","ED_M","METEOR_M","HUMAN_E"}



class Excel_creator:

        def __init__(self,requests,hyps,refs,excel_name):
            self.req_path = requests
            self.refs_path = refs
            self.model_output_path = hyps
            self.excel_name = excel_name+".xlsx"
            self.m_m = Metrics_manager()
            self.excel_to_analyze = None


        def load_excel(self,excel_path): #Sincera che l'excel a cui faccio riferimento ha il giusto formato (riporta le colonne che mi aspetto da un excel generato da questo manager)
            df = pd.read_excel(excel_path,engine='openpyxl')
            all_colums_in_file = all(item in df.columns for item in COLUMS)
            if(all_colums_in_file):
                self.excel_to_analyze = df
            else:
                raise Exception("[ERROR]: wrong excel format")
            
        def getExcelStatistics(self): #Estrapola le statistiche dell'excel a cui facciamo riferimento (numero di EM, media ED e Meteor etc)
            print("Work in progress")

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
        

def excelCreation():
    print("Insert model output path")
    model_out_path = input()
    print("Insert excel name")
    excel_name = input()
    excel_m = Excel_creator(REQUEST_PATH,model_out_path,REFS_PATH,excel_name)
    excel_m.createExcel()

def getStatistics():
    print("Insert excel path")
    excel_path = input()
    e_g = Excel_creator(None,None,None,None)
    try:
        e_g.load_excel(excel_path)
        e_g.getExcelStatistics()
    except Exception as e:
        print(e)
       
def default():
    exit()

switch = {
    1: excelCreation,
    2: getStatistics
}

def menu():
    print("Which operation would you like to do ? \n\n")
    print("1. Create excel for analysis")
    print("2. Get Excel Statistics")
    print("Other. Exit")
    choice = int(input())
    switch.get(choice,default)()


if __name__ == "__main__":
   menu()

    #C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Results\Open-source-models\Open-source-models\Open-source-models\CodeGen\finetuned\test-2024-07-06-23-49\hyps.txt
    #AnalisiCodeGen