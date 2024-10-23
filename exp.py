from psychopy import core, visual, event
from pylsl import StreamInfo, StreamOutlet
import librosa
import numpy as np

# Save folder.
save_dir = "results/"

# Load audiofile. [choose yourself, a podcast]
filename = r"C:\Users\oskar\Documents\GitHub\MobEEGConv\speech_material\single\cut_audio\AnneVibekeIsaksen_0.mp3"
samplerate, sounddata = librosa.load(filename)

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
win = visual.Window()
win.flip()
t_box = visual.TextBox(win, "+",bold=True,font_size=100,font_color=(0, 0, np.random.rand(), 1),)
t_box.draw

# In chunks of 3 mins: 
for i in range(3):
    # Make fixation cross.
    
    # Load audio
    mySound = sound.Sound(sounddata[i*180:(i+1)*180:],secs=180)
    nextFlip = win.getFutureFlipTime(clock='ptb')
    mySound.play(when=nextFlip)  # sync with screen refresh

    #LSL trigger start of audio.
    outlet.push_sample(markers['start'])
    # Podcast start.
    win.flip()    
    # LSL trigger ending of audio.
    outlet.push_sample(markers['stop'])
    # Save data to trial audio.
    # Tell participant of break.
    t_box = visual.TextBox(win, "+",bold=True,font_size=100,font_color=(0, 0, np.random.rand(), 1),)
    t_box.draw