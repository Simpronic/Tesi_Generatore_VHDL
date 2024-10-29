import sys
import evaluate
import subprocess
import pylcs

def editDistance(s1, s2):                
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_temp = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_temp.append(distances[i1])
            else:
                distances_temp.append(1 + min((distances[i1], distances[i1 + 1], distances_temp[-1])))
        distances = distances_temp
        MED = 1-(distances[-1]/max(len(s1),len(s2)))
    return MED #,distances[-1]
   
#LCS for input Sequences “AGGTAB” and “GXTXAYB” is “GTAB” of length 4.

def lcs(s1, s2):
    matrix = [["" for x in range(len(s2))] for x in range(len(s1))]
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                if i == 0 or j == 0:
                    matrix[i][j] = s1[i]
                else:
                    matrix[i][j] = matrix[i-1][j-1] + s1[i]
            else:
                matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1], key=len)

    cs = matrix[-1][-1]
    MLCS = len(cs)/max(len(s1),len(s2))

    return MLCS #,len(cs), cs   
    
    
###########################################################################################
    
def calc_lcs(hyps, refs, out_file_name):
	print("##### LCS #####\n")
	scores = []
	for hyp, ref in zip(hyps, refs):
		tmp = pylcs.lcs_sequence_length(hyp, ref)
		res_norm = tmp/max(len(hyp),len(ref))
		#print(res_norm)
		scores.append(str(res_norm))
		
	with open(out_file_name, 'w') as out_file:
		[out_file.write(sc + "\n") for sc in scores]
	out_file.close()
	
def calc_ed(hyps, refs, out_file_name):
	print("##### ED #####\n")
	scores = []
	for hyp, ref in zip(hyps, refs):
		tmp = pylcs.edit_distance(hyp, ref)
		res_norm = 1-(tmp/max(len(hyp),len(ref)))
		#print(res_norm)
		scores.append(str(res_norm))
		
	with open(out_file_name, 'w') as out_file:
		[out_file.write(sc + "\n") for sc in scores]
	out_file.close()
	
def calc_meteor(hyps, refs, out_file_name):
	print("##### METEOR #####\n")
	meteor = evaluate.load('meteor')
	scores = []
	for hyp, ref in zip(hyps, refs): 
		res_meteor = meteor.compute(predictions=[hyp], references=[ref])
		print(res_meteor['meteor'])
		scores.append(str(res_meteor['meteor']))
		
	with open(out_file_name, 'w') as out_file:
		[out_file.write(sc + "\n") for sc in scores]
	out_file.close()
	
def calc_rouge(hyps_name, refs_name, out_file_name):
	import ast
	print("##### ROUGE #####\n")
	
	metrics = ['1', '2', '3', '4', '5', 'L']
	metrics_name = ["rouge-1", "rouge-2", "rouge-3", "rouge-4", "rouge-5", "rouge-l"]
	
	for i, m in enumerate(metrics):
		cmd = "rouge -f " + hyps_name + " " + refs_name + " --metrics " + m
		result = subprocess.getoutput(cmd)
		res = ast.literal_eval(result)
			
		scores_p = []
		scores_r = []
		scores_f = []
			
		#print(metrics_name[i] + " Precision")
		#print([line[metrics_name[i]]["p"] for line in res])	
		[scores_p.append(str(line[metrics_name[i]]["p"])) for line in res]	
		#print(metrics_name[i] + " Recall")
		#print([line[metrics_name[i]]["r"] for line in res])
		[scores_r.append(str(line[metrics_name[i]]["r"])) for line in res]
		#print(metrics_name[i] + " F1-Score")
		#print([line[metrics_name[i]]["f"] for line in res])
		[scores_f.append(str(line[metrics_name[i]]["f"])) for line in res]	
			
		with open(out_file_name + metrics_name[i] + ".txt", 'w') as out_file:
			
			out_file.write(metrics_name[i] + " Precision\n")
			[out_file.write(str(sc) + "\n") for sc in scores_p]
			out_file.write(metrics_name[i] + " Recall\n")
			[out_file.write(str(sc) + "\n") for sc in scores_r]
			out_file.write(metrics_name[i] + " F1-Score\n")
			[out_file.write(str(sc) + "\n") for sc in scores_f]
			out_file.write("\n\n")
			
		out_file.close()
		
		
def calc_bleu(hyps, refs, out_file_name):
	print("##### BLEU #####\n")
	from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
	metrics = [(1,0,0,0), (0.5, 0.5, 0, 0), (0.33, 0.33, 0.33, 0), (0.25, 0.25, 0.25, 0.25)]
	metric_name = ["\nBLEU-1\n", "\nBLEU-2\n", "\nBLEU-3\n", "\nBLEU-4\n"]
	scores = []
	for i, metric in enumerate(metrics):
		#print(metric_name[i])
		scores.append(metric_name[i])
		for hyp, ref in zip(hyps, refs):
			ref = ref.split()
			hyp = hyp.split()
			#print(sentence_bleu([ref], hyp, weights=metric, smoothing_function=SmoothingFunction().method3))		#smoothing method 3
			scores.append(str(sentence_bleu([ref], hyp, weights=metric, smoothing_function=SmoothingFunction().method3)))	#smoothing method 3
			
		with open(out_file_name, 'w') as out_file:
			[out_file.write(sc + "\n") for sc in scores]
		out_file.close()
		
def calc_sacreBLEU(hyps, refs, out_file_name):
	print("##### SacreBLEU #####\n")
	import sacrebleu
	scores = []
	for i in range(len(hyps)):
		result = sacrebleu.sentence_bleu(hyps[i],refs)
		str_result=str(result)
		scores.append(str_result[7:13])
	with open(out_file_name, 'w') as out_file:
		[out_file.write(sc + "\n") for sc in scores]
	out_file.close()
		
def calc_bleu_corpus(hyps, refs, out_file_name):
	print("##### BLEU #####\n")
	from nltk.translate.bleu_score import corpus_bleu
	metrics = [(1,0,0,0), (0.5, 0.5, 0, 0), (0.33, 0.33, 0.33, 0), (0.25, 0.25, 0.25, 0.25)]
	metric_name = ["\nBLEU-1\n", "\nBLEU-2\n", "\nBLEU-3\n", "\nBLEU-4\n"]
	scores = []
	for i, metric in enumerate(metrics):
		scores.append(metric_name[i])
		scores.append(str(corpus_bleu(refs, hyps, weights=metric)))
			
		with open(out_file_name, 'w') as out_file:
			[out_file.write(sc + "\n") for sc in scores]
		out_file.close()
			
def calc_EM(hyps, refs, out_file_name):
	print("##### EXACT MATCH #####\n")
	scores = []
	for hyp, ref in zip(hyps, refs):
		if hyp == ref:
			#print(1)
			scores.append(str(1))
		else:
			#print(0) 
			scores.append(str(0))
			
	with open(out_file_name, 'w') as out_file:
		[out_file.write(sc + "\n") for sc in scores]
	out_file.close()
			

def read_files(hyps_name, refs_name):
	refs = []
	hyps = []
	
	with open(refs_name, 'r') as refs_file:
		refs_temp = refs_file.readlines()
		refs += [ref.strip('\n') for ref in refs_temp]
		refs_file.close()
	with open(hyps_name, 'r') as hyps_file:
		hyps_temp = hyps_file.readlines()
		hyps += [hyp.strip('\n') for hyp in hyps_temp]
		hyps_file.close()
	return hyps, refs
	
		

if __name__ == '__main__':

	refs = []
	hyps = []
	
	# Modificare nomi files
			
	files_hyps = ["Extended_shellcodeIA32_hyps_ChatGPT.txt"]
	files_refs = ["Extended_shellcodeIA32_refs.txt"]
	
	dir_name = "scores/"
	
	for fh, fr in zip(files_hyps, files_refs):
		print('\n', fh, fr, '\n')
		hyps, refs = read_files(fh, fr)
		
		#calc_rouge(fh, fr, dir_name + fr)
		calc_ed(hyps, refs, dir_name + fr + "_edit_distance.txt")
		#calc_lcs(hyps, refs, dir_name + fr + "_lcs.txt")
		#calc_meteor(hyps, refs, dir_name + fr + "s")
		#calc_bleu_corpus(hyps, refs, dir_name + fr + "_bleu_corpus.txt")
		calc_bleu(hyps, refs, dir_name + fr + "_bleu_line.txt")
		calc_sacreBLEU(hyps, refs, dir_name + fr + "_sacrebleu_line.txt")
		calc_EM(hyps,refs, dir_name + fr + "_exact.txt")

