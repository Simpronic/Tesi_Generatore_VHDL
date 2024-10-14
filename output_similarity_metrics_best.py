import sys
import evaluate
import subprocess
import pylcs
from bleu_score2 import compute_bleu
import os
import numpy as np
from crystal_bleu import *
# from file_parser import *
from rouge import Rouge
from typing import List, Tuple

meteor = evaluate.load('meteor')
bleu = evaluate.load('bleu')


def edit_dist(hyp, ref):
    tmp = pylcs.edit_distance(hyp, ref)
    res_norm = 1-(tmp/max(len(hyp), len(ref)))
    return res_norm


def calc_ed(hyps, refs, aggregate: bool = True):
    scores = [edit_dist(h, r) for h, r in zip(hyps, refs)]
    mean_ed = np.mean(scores)
    min_ed = np.min(scores)
    max_ed = np.max(scores)
    median_ed = np.median(scores)
    q1_ed = np.percentile(scores, 25)
    q3_ed = np.percentile(scores, 75)
    formatted_score = (
        f'ED: {mean_ed * 100:.2f}% (min: {min_ed:.3f}, max: {max_ed:.3f}, median: {median_ed:.3f}, Q1: {q1_ed:.3f}, Q3: {q3_ed:.3f})')
    print(formatted_score)
    if not aggregate:
        return formatted_score, scores
    else:
        return formatted_score


def calc_meteor(hyps, refs, aggregate: bool = True):
    scores = [meteor.compute(predictions=[h], references=[r])[
        'meteor'] for h, r in zip(hyps, refs)]
    mean_meteor = np.mean(scores)
    min_meteor = np.min(scores)
    max_meteor = np.max(scores)
    median_meteor = np.median(scores)
    q1_meteor = np.percentile(scores, 25)
    q3_meteor = np.percentile(scores, 75)
    formatted_score = (
        f'METEOR: {mean_meteor * 100:.2f}% (min: {min_meteor:.3f}, max: {max_meteor:.3f}, median: {median_meteor:.3f}, Q1: {q1_meteor:.3f}, Q3: {q3_meteor:.3f})')
    print(formatted_score)
    if not aggregate:
        return formatted_score, scores
    else:
        return formatted_score


def calc_rouge(hyps, refs):
    metrics = ["rouge-1", "rouge-2", "rouge-3", "rouge-4", "rouge-l"]
    all_f1_scores = {metric: [] for metric in metrics}
    formatted_score = []
    for i, metric in enumerate(metrics):
        rouge = Rouge(metrics=[metric])
        scores = rouge.get_scores(hyps, refs, avg=False)
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
    return formatted_score


def calc_EM(hyps, refs, aggregate: bool = True):
    scores = [1 if hyp.split() == ref.split() else 0 for hyp,
              ref in zip(hyps, refs)]
    mean_em = np.mean(scores)
    formatted_score = 'EM: {0:.2f}%'.format(mean_em * 100)
    print(formatted_score)
    if not aggregate:
        return formatted_score, scores
    else:
        return formatted_score


def calc_corpus_BLEU(hyps, refs):
    formatted_score = []
    for i in range(1, 5):
        bleu_tup = compute_bleu([[x] for x in refs],
                                hyps, smooth=False, max_order=i)
        bleu = bleu_tup[0]
        formatted_score.append(
            'BLEU-' + str(i) + ':{0:.2f}%'.format(bleu * 100))
    for score in formatted_score:
        print(f"{score}")
    return formatted_score


def calc_sentence_BLEU(hyps, refs, aggregate: bool = True):
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    metrics = [(1, 0, 0, 0), (0.5, 0.5, 0, 0),
               (0.33, 0.33, 0.33, 0), (0.25, 0.25, 0.25, 0.25)]
    metric_name = ["BLEU-1", "BLEU-2", "BLEU-3", "BLEU-4"]
    formatted_score = []
    all_scores = []
    for i, metric in enumerate(metrics):
        scores = []
        for hyp, ref in zip(hyps, refs):
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
    if not aggregate:
        return formatted_score, all_scores
    else:
        return formatted_score


def calc_crystalBLEU(hyps, refs, re_compute_ngrams: bool):

    cache_folder = "crystal_cache"
    # os.makedirs(cache_folder, exist_ok=True)
    # if re_compute_ngrams:
    #     pass

    # else:
    #     print("Loading trivially shared ngrams")

    trivial_ngrams = compute_trivially_shared_ngrams(
        hyps, "vhdl", cache_folder)
    scores = compute_crystal_bleu(refs, hyps, trivial_ngrams, "vhdl")
    mean_crystal = np.mean(scores)
    min_crystal = np.min(scores)
    max_crystal = np.max(scores)
    median_crystal = np.median(scores)
    q1_crystal = np.percentile(scores, 25)
    q3_crystal = np.percentile(scores, 75)
    formatted_score = (
        f'\nCrystalBLEU: {mean_crystal * 100:.2f}% (min: {min_crystal:.3f}, max: {max_crystal:.3f}, median: {median_crystal:.3f}, Q1: {q1_crystal:.3f}, Q3: {q3_crystal:.3f})')
    print(formatted_score)
    return formatted_score

def get_leaf_paths(root_dir: str) -> List[Tuple[str, str]]:
    result = []
    
    for model in os.listdir(root_dir):
        model_path = os.path.join(root_dir, model)
        if not os.path.isdir(model_path):
            continue
        
        for operation in os.listdir(model_path):
            operation_path = os.path.join(model_path, operation)
            if not os.path.isdir(operation_path):
                continue
            
            for test_timestamp in os.listdir(operation_path):
                test_path = os.path.join(operation_path, test_timestamp)
                if not os.path.isdir(test_path):
                    continue
                
                hyps_path = os.path.join(test_path, 'hyps.txt')
                refs_path = os.path.join(test_path, 'refs.txt')
                
                if os.path.isfile(hyps_path) and os.path.isfile(refs_path):
                    result.append((hyps_path, refs_path))
    
    return result

def save_scores_to_file(scores, metric_name, directory):
    filename = os.path.join(directory, f'sentence_results_{metric_name}.txt')
    with open(filename, 'w') as f:
        for score in scores:
            f.write(f"{score}\n")

def get_scores(aggregate: bool = True):
    root_directory = "/Users/carloportosalvo/Desktop/Università/TesiMagistrale/Data/result2/Anna_report"
    paths = get_leaf_paths(root_directory)

    for hyps_filename, refs_filename in paths:
        # Read files
        with open(hyps_filename, 'r') as f:
            hyps = f.readlines()

        with open(refs_filename, 'r') as f:
            refs = f.readlines()

        # Remove newlines and strip spaces
        hyps = [hyp.strip() for hyp in hyps]
        refs = [ref.strip() for ref in refs]

        print(f"Number of predictions: {len(hyps)}")
        print(f"Number of references: {len(refs)}")

        directory = os.path.dirname(hyps_filename)

        if aggregate:
            calc_crystalBLEU(hyps, refs, re_compute_ngrams=True)
            calc_corpus_BLEU(hyps, refs)
            calc_EM(hyps, refs)
            calc_ed(hyps, refs)
            calc_meteor(hyps, refs)
            calc_rouge(hyps, refs)
        else:
            res, em_scores = calc_EM(hyps, refs, aggregate)
            save_scores_to_file(em_scores, 'em', directory)

            res, ed_scores = calc_ed(hyps, refs, aggregate)
            save_scores_to_file(ed_scores, 'ed', directory)

            res, meteor_scores = calc_meteor(hyps, refs, aggregate)
            save_scores_to_file(meteor_scores, 'meteor', directory)

            res, bleu_scores = calc_sentence_BLEU(hyps, refs, aggregate)
            for i, scores in enumerate(bleu_scores):
                save_scores_to_file(scores, f'bleu-{i+1}', directory)


if __name__ == "__main__":
    get_scores(aggregate=True)