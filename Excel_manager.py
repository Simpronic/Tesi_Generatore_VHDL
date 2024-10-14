import pandas as pd
from Metrics_manager import *

REQUEST_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.in"
REFS_PATH = r"C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Dataset\splitted_files\vhdl-test.out"

class Excel_creator:

        def __init__(self,requests,hyps,refs,excel_name):
            self.req_path = requests
            self.refs_path = refs
            self.model_output_path = hyps
            self.excel_name = excel_name+".xlsx"
            self.m_m = Metrics_manager()

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
        

if __name__ == "__main__":
    print("Insert model output path")
    model_out_path = input()
    print("Insert excel name")
    excel_name = input()
    excel_m = Excel_creator(REQUEST_PATH,model_out_path,REFS_PATH,excel_name)
    excel_m.createExcel()


    #C:\Users\marcd\Desktop\Tesi\Dati\OneDrive_1_04-10-2024\Results\Open-source-models\Open-source-models\Open-source-models\CodeGen\finetuned\test-2024-07-06-23-49\hyps.txt
    #AnalisiCodeGen