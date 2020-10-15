# author: s-Kline
# dot probe task with interleaved affect induction trials
# to do: jittered pause between dot probe trials?
#        images are stretched in fullscreen because monitor specs are needed to fix that

import os
import numpy
from psychopy import gui, visual, core, event, monitors

def read_order(st_file_path):
    """ function for reading presentation order from st_files
        input: path to textfile
        output: list of trial specs"""
    st_file = open(st_file_path)
    order_list = [t.rstrip() for t in st_file.readlines()]
    order_list = [t.split('\t') for t in order_list]
    st_file.close()
    return order_list

def shutdown():
    win.close()
    core.quit()

##################################################################################################################

key = 'q'
event.globalKeys.add(key=key, func=shutdown)

# stimuli prep
stim_path = 'stimuli\\'
iaps_path = stim_path + 'picpercept_stimuli\\'

# display GUI for subject ID
info = {'vp-nummer': '001'}
dictDlg = gui.DlgFromDict(dictionary=info,
                          title='dotprobe',
                          fixed=['ExpVersion'])
if dictDlg.OK:
    print(info)
else:
    core.quit()
    print('User Cancelled')
vp_nummer = info['vp-nummer']

# prepare logfile
logdir = 'logfiles\\'
datei = logdir + str(vp_nummer) + '_emo_cue_dotprobe_log' + '.txt'
datei = open(datei, 'w')
datei.write('trial\tleft stim'
            '\tright stim'
            '\tdot_onset'
            '\tbutton_onset'
            '\treacttime'
            '\tbutton_press'
            '\tdot position'
            '\tdot replaced'
            '\tanswer')
trial_list = []


# read trial order from file
steuerfile = 'st_files\\' + str(vp_nummer) + '_emo_cue_dotprobe_st.txt'
trial_order = read_order(steuerfile)
print(trial_order)

# initialize window
mon = monitors.Monitor('Acer_Sanja')
win = visual.Window(fullscr=True,
                    mon=mon,
                    screen=0,
                    size=(1000, 800),
                    color='black')
# fixationskreuz
fix_kreuz = visual.TextStim(win, text='+', color='white', pos=(0, 0))  # stimulus spezifizieren, mitte

############################################################################################################
# main experiment loop starts here
i = 1
aff = 0
for trial in trial_order:
    trial_events = []
    clock = core.Clock()

    # affect induction trial
    if trial[0] == 'affect':
        
        for frameN in range(120):  # present fix. cross for 120 frames(2 s)
            fix_kreuz.draw()
            win.flip()
            
        pics = trial[1:]
        print(pics)
        trial_events.append(i)  # trial number
        trial_events.append('\t'.join(trial))  # pic names
        # present iaps pics specified in trial_order
        for p in range(3):
            aff_stim = visual.ImageStim(win,
                                    image=iaps_path + pics[p],
                                    units='pix',
                                    size=(1440/2, 1080/2),
                                    pos=(0, 0))
            for frameN in range(120):
                aff_stim.draw()
                win.flip()
        # rating
        ratingScale = visual.RatingScale(win,
                                         labels=('sehr negativ', 'sehr positiv'),
                                         scale=None,
                                         low=1,
                                         high=9,
                                         marker='slider',
                                         markerStart=5,
                                         leftKeys='left',
                                         rightKeys='right',
                                         pos=(0, 0),
                                         showValue=False,
                                         showAccept=False,
                                         markerColor='white'
                                         )
        item = visual.TextStim(win,
                               text='Wie fuehlen Sie\nsich gerade?',
                               pos=(0, 0.5),
                               alignHoriz='center',
                               color='white'
                               )
        while ratingScale.noResponse:
            item.draw()
            ratingScale.draw()
            win.flip()
        rating = ratingScale.getRating()
        decisionTime = ratingScale.getRT()
        choiceHistory = ratingScale.getHistory()
        trial_events.append('\t'.join([str(rating), str(decisionTime)]))
        
        
        for frameN in range(120):  # present fix. cross for 120 frames (2 s)
            fix_kreuz.draw()
            win.flip()

    # dot probe trial
    else:
        trial_events.append(i)  # wievielter trial?
        # images
        stim_left = visual.ImageStim(win,
                                     image=stim_path + trial[0],
                                     #units='pix',
                                     #size=(1024*0.8, 768*0.8),
                                     size=0.8,
                                     pos=(-0.5, 0))

        stim_right = visual.ImageStim(win,
                                      image=stim_path + trial[1],
                                      #units='pix',
                                      #size=(1024*0.8, 768*0.8),
                                      size=0.8,
                                      pos=(0.5, 0))
        # dot
        if trial[2] == 'left':
            dot_pos = (-0.5, 0)
        elif trial[2] == 'right':
            dot_pos = (0.5, 0)

        dot = visual.Circle(win,
                            radius=0.02,
                            edges=32,
                            lineColor='white',
                            fillColor='white',
                            pos=dot_pos)

        # which cue presented where
        trial_events.extend([trial[0][:-4], trial[1][:-4]])

        for frameN in range(30):  # present fix. cross for 30 frames(500 ms)
            fix_kreuz.draw()
            win.flip()
        for frameN in range(60):  # present cues for 60 frames(1000 ms)
            #fix_kreuz.draw()
            stim_left.draw()
            stim_right.draw()
            win.flip()
        dot.draw()  # present dot for 1 frame (16 ms)
        win.flip()

        # get reaction time
        button_press = []
        dot_onset = float(clock.getTime())
        button_press = event.waitKeys(maxWait=1.5, keyList=['right', 'left'])
        button_onset = float(clock.getTime())

        # log times if a reaction ocurred
        if button_press:
            reacttime = button_onset - dot_onset
            print(dot_onset, button_onset, reacttime, button_press[0])
            trial_events.extend([dot_onset, button_onset, reacttime, button_press[0]])
        else: trial_events.extend([dot_onset, 'no response', 'no reacttime', 'no response'])

        # log position, which stim was replaced and if response was correct
        if dot_pos == (-0.5, 0):  # dot on the left
            trial_events.append('left')  # dot position
            trial_events.append(trial[0][:-4].split('_')[0])  # dot replaced what
            if button_press == ['left']: trial_events.append('correct')
            elif button_press == ['right']: trial_events.append('incorrect')
            else: trial_events.append('no response')
        if dot_pos == (0.5, 0):  # dot on the right
            trial_events.append('right')  # dot position
            trial_events.append(trial[1][:-4].split('_')[0])   # dot replaced what
            if button_press == ['right']: trial_events.append('correct')
            elif button_press ==['left']: trial_events.append('incorrect')
            else: trial_events.append('no response')
    # write contents of trial_events in tab sep. line
    datei.write('\n' + '\t'.join([str(j) for j in trial_events]))
    datei.flush()
    i += 1
datei.close()
core.quit()
win.close()
