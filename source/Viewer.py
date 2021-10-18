from tkinter import *
import time
import os
os.add_dll_directory('C:\\Program Files (x86)\\VideoLAN\\VLC')
import vlc

root = Tk()
root.title('RTSP Viewer')


# read from config.cfg:
try:
    dict_cam = {}
    lst = []
    numbers_cam = sum(1 for line in open('config.cfg', 'r'))-1
    print(f'We have {numbers_cam} cameras in config.cfg')
    with open('config.cfg') as file:
        wh_lst = file.readline().split(' ')
        # read resolution
        root_width, root_height= wh_lst[2], wh_lst[3]
        root_width = int(root_width)
        root_height = int(root_height[:-1])
        # read labels and adresses for cams
        for i in range(numbers_cam):
            name, addr = file.readline().split('   ')
            addr = addr[:-1]
            dict_cam[name] = addr
except:
    print('config.cfg not found!')
    time.sleep(5)
    exit()

   
# load geometry 
print(f'Resolution is {root_width}x{root_height}')
root.geometry(f"{root_width}x{root_height}")
root.resizable(width=False, height=False)

# labels for cams to list
labels = list(dict_cam.keys())
# adresses for cams to list
addrs = list(dict_cam.values())
# print name of loading cams
for i in labels:
    print(f'Loading {i} Web Camera')


# CREATE FRAMES
#       frames for cam
for i in range(1,17):
    globals()[f'frame{i}'] = LabelFrame(root, width=root_width/4, height=root_height/4.52, bd=2)
frame1.grid(row=1, column=0, padx=1)
frame2.grid(row=1, column=1, padx=1)
frame3.grid(row=1, column=2, padx=1)
frame4.grid(row=1, column=3, padx=1)
frame5.grid(row=3, column=0, padx=1)
frame6.grid(row=3, column=1, padx=1)
frame7.grid(row=3, column=2, padx=1)
frame8.grid(row=3, column=3, padx=1)
frame9.grid(row=5, column=0, padx=1)
frame10.grid(row=5, column=1, padx=1)
frame11.grid(row=5, column=2, padx=1)
frame12.grid(row=5, column=3, padx=1)
frame13.grid(row=7, column=0, padx=1)
frame14.grid(row=7, column=1, padx=1)
frame15.grid(row=7, column=2, padx=1)
frame16.grid(row=7, column=3, padx=1)

#       frames for text
for i in range(17, 33):
    globals()[f'frame{i}'] = LabelFrame(root, width=root_width/4, height=root_height/30, bd=0)
frame17.grid(row=0, column=0, padx=1)
frame18.grid(row=0, column=1, padx=1)
frame19.grid(row=0, column=2, padx=1)
frame20.grid(row=0, column=3, padx=1)
frame21.grid(row=2, column=0, padx=1)
frame22.grid(row=2, column=1, padx=1)
frame23.grid(row=2, column=2, padx=1)
frame24.grid(row=2, column=3, padx=1)
frame25.grid(row=4, column=0, padx=1)
frame26.grid(row=4, column=1, padx=1)
frame27.grid(row=4, column=2, padx=1)
frame28.grid(row=4, column=3, padx=1)
frame29.grid(row=6, column=0, padx=1)
frame30.grid(row=6, column=1, padx=1)
frame31.grid(row=6, column=2, padx=1)
frame32.grid(row=6, column=3, padx=1)

# create frames for labels
frames_labels = []
for i in range(17,33):
    frames_labels += [globals()[f'frame{i}']]
# create frames for cameras
frames_cams = []
for i in range(1,17):
    frames_cams += [globals()[f'frame{i}']]
    
i = 17  # number of first frame for labels
for label in labels:
    label = Label(globals()[f'frame{i}'], text=label, fg="#333", bg="#eee")
    label.pack()
    i += 1

def play_video(frame, addr):       # fr - frame(n), addr - rtsp address
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    player.set_hwnd(frame.winfo_id())
    media = Instance.media_new(addr)
    player.set_media(media)
    player.play()
    return player
    
# for check cam(n) status
n = 1
for addr in addrs:
    globals()[f'cam{n}'] = play_video(frames_cams[n-1], addr)
    n += 1
print()

print('Starting...')
print()

# for fullscreen
print('Press 1-9 fjr fullscreen 1-9 channels')
print('Press 0 for fullscreen 10 channel')
print('Press q-y for fullscreen 11-16 channels')

def stop_fullscr(e):
    full_scr.stop()
    print (f'Stop Fullscreen')
def fullscr(e):
    global full_scr
    try:
        if 1 <= int(e.char) <= 9:
            channel = int(e.char)
        elif int(e.char) == 0:
            channel = 10
    except:
        if e.char =='q':
            channel = 11
        elif e.char == 'w':
            channel = 12
        elif e.char == 'e':
            channel = 13
        elif e.char == 'r':
            channel = 14
        elif e.char == 't':
            channel = 15
        elif e.char == 'y':
            channel = 16
    full_scr = vlc.MediaPlayer(addrs[channel-1])
    full_scr.play()
    full_scr.toggle_fullscreen()
    print (f'Start Fullscreen for cam#{channel}')
    time.sleep(40)
    full_scr.stop()
    print (f'Stop Fullscreen')


root.bind("<KeyPress>", fullscr)
root.bind("s", stop_fullscr)
root.focus_set()
root.mainloop()



        

'''
# reset stream if status = Ended (NOT WORKING NOW!)
while True:
    for i in range(1, numbers_cam+1):
        if globals()[f'cam{i}'].get_state() == vlc.State.Ended:
            print(globals()[f'cam{i}'].get_state())
            globals()[f'cam{i}'].stop()
            #print(f"Oooops, reload cam{i}!")
            globals()[f'cam{i}'] = play_video(frames[i-1], addr)
'''

        


