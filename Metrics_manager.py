import sys
import evaluate
import subprocess
import pylcs
from bleu_score2 import compute_bleu
import os
import numpy as np
from crystal_bleu import *
from rouge import Rouge
from typing import List, Tuple
import pylcs


class Metrics_manager:

    def __init__(self):
        self.hyps = None
        self.refs = None
        self.meteor = evaluate.load('meteor')
        self.bleu = evaluate.load('bleu')
        
    def load_hyps(self,hyps):
        self.hyps = hyps

    def load_refs(self,refs):
        self.refs = refs

    def calc_lcs(self):
        scores = []
        for hyp, ref in zip(self.hyps, self.refs):
            tmp = pylcs.lcs_sequence_length(hyp, ref)
            res_norm = tmp/max(len(hyp),len(ref))
            scores.append(str(res_norm))
            return scores
    
    def __edit_dist(self,hyp, ref):
        tmp = pylcs.edit_distance(hyp, ref)
        res_norm = 1-(tmp/max(len(hyp), len(ref)))
        return res_norm
    
    def calc_ed(self):
        scores = [self.__edit_dist(h, r) for h, r in zip(self.hyps, self.refs)]
        mean_ed = np.mean(scores)
        min_ed = np.min(scores)
        max_ed = np.max(scores)
        median_ed = np.median(scores)
        q1_ed = np.percentile(scores, 25)
        q3_ed = np.percentile(scores, 75)
        return scores
    
    def calc_meteor(self):
        scores = [self.meteor.compute(predictions=[h], references=[r])[
            'meteor'] for h, r in zip(self.hyps, self.refs)]
        mean_meteor = np.mean(scores)
        min_meteor = np.min(scores)
        max_meteor = np.max(scores)
        median_meteor = np.median(scores)
        q1_meteor = np.percentile(scores, 25)
        q3_meteor = np.percentile(scores, 75)
        return scores

    def calc_EM(self):
        scores = [1 if hyp.split() == ref.split() else 0 for hyp,
                ref in zip(self.hyps, self.refs)]
        mean_em = np.mean(scores)
        return scores

def calc_rouge(self):
    metrics = ["rouge-1", "rouge-2", "rouge-3", "rouge-4", "rouge-l"]
    all_f1_scores = {metric: [] for metric in metrics}
    formatted_score = []
    for i, metric in enumerate(metrics):
        rouge = Rouge(metrics=[metric])
        scores = rouge.get_scores(self.hyps, self.refs, avg=False)
        f1_scores = [score[metric]['f'] for score in scores]
        all_f1_scores[metric].extend(f1_scores)
        scores = np.array(all_f1_scores[metric])
        mean_rouge = np.mean(scores)
        min_rouge = np.min(scores)
        max_rouge = np.max(scores)
        median_rouge = np.median(scores)
        q1_rouge = np.percentile(scores, 25)
        q3_rouge = np.percentile(scores, 75)
        formatted_score.append(
            f'{metrics[i].upper()}: {mean_rouge * 100:.2f}% (min: {min_rouge:.3f}, max: {max_rouge:.3f}, median: {median_rouge:.3f}, Q1: {q1_rouge:.3f}, Q3: {q3_rouge:.3f})')
    for score in formatted_score:
        print(f"{score}")
    return formatted_score,all_f1_scores





def calc_corpus_BLEU(self):
    formatted_score = []
    scores = []
    for i in range(1, 5):
        bleu_tup = compute_bleu([[x] for x in self.refs],
                                self.hyps, smooth=False, max_order=i)
        bleu = bleu_tup[0]
        scores.append(bleu)
        formatted_score.append(
            'BLEU-' + str(i) + ':{0:.2f}%'.format(bleu * 100))
    for score in formatted_score:
        print(f"{score}")
    return formatted_score,scores


def calc_sentence_BLEU(self):
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    metrics = [(1, 0, 0, 0), (0.5, 0.5, 0, 0),
               (0.33, 0.33, 0.33, 0), (0.25, 0.25, 0.25, 0.25)]
    metric_name = ["BLEU-1", "BLEU-2", "BLEU-3", "BLEU-4"]
    formatted_score = []
    all_scores = []
    for i, metric in enumerate(metrics):
        scores = []
        for hyp, ref in zip(self.hyps, self.refs):
            ref = ref.split()
            hyp = hyp.split()
            scores.append(sentence_bleu(
                [ref], hyp, weights=metric, smoothing_function=SmoothingFunction().method1))
        mean_bleu = np.mean(scores)
        min_bleu = np.min(scores)
        max_bleu = np.max(scores)
        median_bleu = np.median(scores)
        q1_bleu = np.percentile(scores, 25)
        q3_bleu = np.percentile(scores, 75)
        formatted_score.append(
            f'{metric_name[i]}: {mean_bleu * 100:.2f}% (min: {min_bleu:.3f}, max: {max_bleu:.3f}, median: {median_bleu:.3f}, Q1: {q1_bleu:.3f}, Q3: {q3_bleu:.3f})')
        all_scores.append(scores)
    for score in formatted_score:
        print(f"{score}")
    return formatted_score, all_scores

def calc_crystalBLEU(self, re_compute_ngrams: bool):

    cache_folder = "crystal_cache"
    # os.makedirs(cache_folder, exist_ok=True)
    # if re_compute_ngrams:
    #     pass

    # else:
    #     print("Loading trivially shared ngrams")

    trivial_ngrams = compute_trivially_shared_ngrams(
        self.hyps, "vhdl", cache_folder)
    scores = compute_crystal_bleu(self.refs, self.hyps, trivial_ngrams, "vhdl")
    mean_crystal = np.mean(scores)
    min_crystal = np.min(scores)
    max_crystal = np.max(scores)
    median_crystal = np.median(scores)
    q1_crystal = np.percentile(scores, 25)
    q3_crystal = np.percentile(scores, 75)
    formatted_score = (
        f'\nCrystalBLEU: {mean_crystal * 100:.2f}% (min: {min_crystal:.3f}, max: {max_crystal:.3f}, median: {median_crystal:.3f}, Q1: {q1_crystal:.3f}, Q3: {q3_crystal:.3f})')
    print(formatted_score)
    return formatted_score,scores

