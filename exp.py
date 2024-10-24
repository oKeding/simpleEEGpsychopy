from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'sounddevice'
prefs.hardware['audioLatencyMode'] = '3'

from psychopy import core, visual, event, sound
from pylsl import StreamInfo, StreamOutlet
import numpy as np

# Save folder.
save_dir = "results/"

# Load audiofile. [choose yourself, a podcast]
filename = "stimuli/beachBlock.wav"

# Set up trigger LSL.
info = StreamInfo(name='trigger_stream', type='trigger', channel_count=1,
                      channel_format='int32', source_id='trigger_stream_001')
outlet = StreamOutlet(info)  # Broadcast the stream.
markers = {
        'start': [1],
        'stop': [2],
    }

# Set up AudioCapture LSL stream. ??? how ??? (only can do before outside)

# Set up monitor.
win = visual.Window()#fullscr=True)
win.flip()
t_box = visual.TextStim(win, "Start recording EEG (including proper LSL).",bold=True,color=(1, 1, 1))
t_box.draw()

win.flip()
event.waitKeys(keyList="1") # When setup stream pause to start the experiment capture.
win.flip()
# In chunks of 3 mins:
length_of_trial = 2 # in seconds
for i in range(10):
    # Set up Sound.
    Left = sound.Sound('A', secs=-1, stereo=True, hamming=True, name='Front', sampleRate=44100, startTime = i*length_of_trial, stopTime = (i+1)*length_of_trial)
    
    # Load audio
    Left.setSound(filename)
    nextFlip = win.getFutureFlipTime(clock='ptb')
    core.wait(5)
    Left.play(when=nextFlip)  # sync    with screen refresh
    
    # Change color of the fixation cross for this trial.
    t_plus = visual.TextStim(win, "+",bold=True,color=(1, 1, np.random.rand()))
    t_plus.draw()
    
    #LSL trigger start of audio.
    outlet.push_sample(markers['start'])
    # Podcast start.
    win.flip()
    core.wait(length_of_trial)
    Left.stop()
    # LSL trigger ending of audio.
    outlet.push_sample(markers['stop'])
    # Tell participant of break.
    trial_break_text = visual.TextStim(win, "Break until next trial",bold=True,color=(1,1,1))
    trial_break_text.draw()
    win.flip()
    
    # Save data to trial audio. (LSL for now, and manual cropping of stimuli)

