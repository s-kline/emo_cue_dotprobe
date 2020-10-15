# author: s-Kline
# create controlfiles for emotional dotprobe paradigm
# 4 affect induction blocks each of 3 emotion categories (positive, negative, neutral) with 4 pics each
# after each affect block, 9 dot probe trials of 3 different stimuli types (porn, gambling, neutral)

import random
import os
import copy
from itertools import chain
from collections import Counter
# from sys import exit

stimdir = 'C:\\Users\\klein\\PycharmProjects\\emo_cue_dotprobe\\stimuli\\'
st_dir = 'C:\\Users\\klein\\PycharmProjects\\emo_cue_dotprobe\\st_files\\'

# get picpercept stimuli
affect_pics = os.listdir(stimdir + 'picpercept_stimuli\\')
affect_neu = [i for i in affect_pics if i.startswith('neu')]
affect_pos = [i for i in affect_pics if i.startswith('pos')]
affect_neg = [i for i in affect_pics if i.startswith('neg')]
affect_cat = [affect_pos, affect_neg, affect_neu]

# get cue stimuli for dot probe
allstim = os.listdir(stimdir)
ga_pics = [i for i in allstim if i.startswith('ga_')]  # 47 pics
po_pics = [i for i in allstim if i.startswith('po_')]  # 49 pics
neu_pics = [i for i in allstim if i.startswith('neu_')]  # 57 pics

# sort gaming stimuli into categories
ga_desk = [i for i in ga_pics if 'desk' in i]
ga_smar = [i for i in ga_pics if 'smar' in i]
ga_lap = [i for i in ga_pics if 'lap' in i]
ga_tab = [i for i in ga_pics if 'tab' in i]
ga_logo = [i for i in ga_pics if 'logo' in i]

# sort porn stimuli into categories
po_desk = [i for i in po_pics if 'desk' in i]
po_smar = [i for i in po_pics if 'smar' in i]
po_lap = [i for i in po_pics if 'lap' in i]
po_tab = [i for i in po_pics if 'tab' in i]
po_logo = [i for i in po_pics if 'logo' in i]

gaming_stim = [ga_desk, ga_smar, ga_lap, ga_tab]  # , ga_logo]
porn_stim = [po_desk, po_smar, po_lap, po_tab]  # , po_logo]
neu_stim = neu_pics

# dotprobe stimuli have to be chosen according to this dummy block (6 stimuli of each category per block)
dummy_dotprobe_trials = [['po', 'neu'],
                         ['neu', 'po'],
                         ['ga', 'neu'],
                         ['neu', 'ga'],
                         ['ga', 'po'],
                         ['po', 'ga'],
                         ['ga', 'ga'],
                         ['po', 'po'],
                         ['neu', 'neu']]

dot_list = ['left', 'right']  # possible dot positions

################################################################

subjects = 80  # how many st_files do we need
n_iaps_cat = 3  # how many emotional picture categories are there
n_reps = 5  # how many times should affect trials be repeated
n_blocks = n_iaps_cat * n_reps  # how many dotprobe blocks should be created

iaps_reps = 1  # how many times are iaps pics allowed to be used?

################################################################
for n in range(1, subjects + 1):
    filename = st_dir + str(n).zfill(3) + '_emo_cue_dotprobe_st.txt'
    st_file = open(filename, 'w')
    experiment = []

    for i in range(2): # do the following 2 times per subject
        trial_list = []
        probe_blocks = []
        # while affect block violations remain, create n_blocks affect blocks
        violations = 1  # starting point for creation
        while violations > 0:
            trial_list = []
            tmp_affect_cat = [i*iaps_reps for i in affect_cat]  # tmp list where used pics are deleted (every pic exists iaps_reps times)
            # make trials
            all_affect_trials = []
            for cat in tmp_affect_cat:  # for every category containing 60 pics
                for i in range(n_reps):  # chose from each affect n_reps times
                    affect_block = random.sample(cat, 4)  # take 4 pictures from one category
                    trial_list.append(affect_block)  # add as affect block
                    for p in affect_block: cat.remove(p) # take out so nothing can be reused
            random.shuffle(trial_list)  # shuffle blocks

            # check for violations (exit while loop if none remain)
            violations = 0
            for b in trial_list:
                if len(list(set(b))) != len(b): # only unique pics in one block
                    violations += 1
                    continue
            for i in range(len(trial_list)-1):
                block = trial_list[i]
                next_block = trial_list[i+1]
                if block[0][:3] == next_block[0][:3]:  # no two same blocks after another
                    violations += 1
                    continue  # stop here and try again (no need to check the rest)

        # while dot probe violations remain, create 12 dot probe blocks
        violations = 1  # starting point for creation
        while violations > 0:
            probe_blocks = []
            for i in range(n_blocks):  # number of dot probe blocks to be created
                violations = 1  # starting point
                # while block violations remain, create new block of trials
                while violations > 0:
                    probe_trials = []
                    # refill stimuli lists with originals
                    tmp_porn_stim = copy.deepcopy(porn_stim)
                    tmp_gaming_stim = copy.deepcopy(gaming_stim)
                    tmp_neu_stim = copy.deepcopy(neu_stim)
                    tmp_all = [tmp_neu_stim, tmp_gaming_stim, tmp_porn_stim]

                    # makes 9 trials (or however many specified in the dummy list)
                    for trial in dummy_dotprobe_trials:
                        new_trial = ['', '']
                        stimtype = random.randint(0, 3)  # one of the 4 stimuli types in porn_stim/game_stim
                        while any(stimlist[stimtype] == [] for stimlist in tmp_all):  # cant choose from empty ones
                            stimtype = random.randint(0, 3)
                        # constructs one trial:
                        for p in range(0, 2):
                            if trial[p] == 'po':
                                new_trial[p] = random.choice(tmp_porn_stim[stimtype])  # randomly choose from type list
                                tmp_porn_stim[stimtype].remove(new_trial[p])  # delete
                            if trial[p] == 'ga':
                                new_trial[p] = random.choice(tmp_gaming_stim[stimtype])  # randomly choose from type list
                                tmp_gaming_stim[stimtype].remove(new_trial[p])  # delete
                            if trial[p] == 'neu':
                                new_trial[p] = random.choice(tmp_neu_stim)  # randomly choose from neutral
                                tmp_neu_stim.remove(new_trial[p])  # delete

                        new_trial.append(random.choice(dot_list))  # add left or right dot position randomly
                        probe_trials.append(new_trial)
                    random.shuffle(probe_trials)  # shuffle the block

                    violations = 0
                    # check for block violations here (left & right equality, replacements)
                    ga_replaced = 0
                    po_replaced = 0
                    neu_replaced = 0
                    rightpos = 0
                    leftpos = 0
                    repl = 0
                    positions = []
                    for trial in probe_trials:
                        positions.append(trial[2])
                        if trial[2] == 'left':
                            repl = trial[0]
                            leftpos += 1
                        elif trial[2] == 'right':
                            repl = trial[1]
                            rightpos += 1
                        if not trial[0][:3] == trial[1][:3]:  # ignore the trials with same cues
                            if repl.startswith('ga_'): ga_replaced += 1
                            elif repl.startswith('po_'): po_replaced += 1
                            elif repl.startswith('neu_'): neu_replaced += 1

                   # print(positions)
                    size = 3  # positions are not allowed to repeat 3 times
                    result = [sublist for sublist in
                              (positions[x:x + size] for x in range(len(positions) - size + 1))]  # get sublists of specif. size
                    if any([sublist.count(sublist[0]) == len(sublist) for sublist in result]):  # if any are identical
                        violations += 1
                        continue

                    replacements = [ga_replaced, po_replaced, neu_replaced]
                    if any(not 3 >= r >= 1 for r in replacements):  # each should be replaced 2-3 times
                        violations += 1
                        continue

                    if any(not 5 >= pos >= 3 for pos in [leftpos, rightpos]):  # left and right should be 3-5 times each
                        violations += 1
                        continue

                    probe_blocks.append(probe_trials)  # add to list of blocks if no violations remain

            # check for experiment violations here
            all_dot_trials = list(chain.from_iterable((list(chain.from_iterable(probe_blocks)))))
            used_pics = [i for i in all_dot_trials if i != 'right' and i != 'left']
            c = Counter(used_pics)
            if any(pic > 5 for pic in c.values()):  # pics should not be used more than 5 times
                violations += 1
                continue

        experiment.extend([trial_list, probe_blocks])  # st_file content ready to write

    # write the whole thing to the txt file
    for h in range(0, 4, 2): # experiment contains 4 lists to create two big blocks
        trials = experiment[h]
        probes = experiment[h+1]
        for i in range(n_blocks):
            st_file.write('affect\t')
            st_file.write('\t'.join(trials[i]) + '\n')
            for trial in probes[i]:
                st_file.writelines('\t'.join(trial) + '\n')
        st_file.write('pause\n')
    st_file.close()
    print(filename, ' done!')

