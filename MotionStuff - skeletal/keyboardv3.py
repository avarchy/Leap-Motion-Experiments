# Adithya Venkatesan
#
# keyboard
# need to get keyboard swipes and updates to work
#

from Tkinter import *
from sys import exit
import math
import time
lastswipe=time.time()
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import pyperclip #allows me to copy text to clipboard

w,h= 975,400
x,y,dx,dy=100,100,199,199
fingdisplist = []
scaling = 3.0
root = None
canvas = None
typed = None
key_width = 70#width of each key displayed on the canvas
key_height = 60#height of each key displayed on the canvas
circlediameter = 20#diamater of each finger circle
keyspacing = 4#space bewteen each key
changekeyb=False
btn_list = [
    ['`','1','2','3','4','5','6','7','8','9','0','-','='],
     ['*20','q','w','e','r','t','y','u','i','o','p','Backspace'],
        ['*40','a','s','d','f','g','h','j','k','l',';','\'','Enter'],
        ['Shift','z','x','c','v','b','n','m',',','.','/','Shift'],
        ['*200','space']]
kyb_list = [
    #regular keyboards
    [['`','1','2','3','4','5','6','7','8','9','0','-','='],
     ['*20','q','w','e','r','t','y','u','i','o','p','Backspace'],
        ['*40','a','s','d','f','g','h','j','k','l',';','\'','Enter'],
        ['Shift','z','x','c','v','b','n','m',',','.','/','Shift'],
        ['*200','space']],
    [['`','1','2','3','4','5','6','7','8','9','0','-','='],
     ['*20','\'',',','.','p','y','f','g','c','r','l','Backspace'],
        ['*40','a','o','e','u','i','d','h','t','n','s','-','Enter'],
        ['Shift',';','q','j','k','x','b','m','w','v','z','Shift'],
        ['*200','space']],
    #capitalized keyboards
    [['~','!','@','#','$','%','^','&','*','(',')','_','+'],
     ['*20','Q','W','E','R','T','Y','U','I','O','P','Backspace'],
        ['*40','A','S','D','F','G','H','J','K','L',':','\'','Enter'],
        ['Shift','Z','X','C','V','B','N','M','<','>','?','Shift'],
        ['*200','space']],
    [['~','!','@','#','$','%','^','&','*','(',')','_','+'],
     ['*20','\'','<','>','P','Y','F','G','C','R','L','Backspace'],
        ['*40','A','O','E','U','I','D','H','T','N','S','_','Enter'],
        ['Shift',':','Q','J','K','X','B','M','W','V','Z','Shift'],
        ['*200','space']],
]
curkeyb = 0#current keyboard being used
numkeybs=2#total number of keyboards, can tell if it is a caps keyboard if

#global w,h,x,y,dx,dy,fingdisplist,scaling,root,canvas,typed,key_width,key_height,circlediameter,keyspacing,btn_list,kyb_list,curkeyb,numkeybs
def quit(event):
    global root
    root.destroy()
    
def copytext():
    global root
    pyperclip.copy(typed.get())
##    root.withdraw()
##    root.clipboard_clear()
##    root.clipboard_append(typed.get())

def updatekeyboard():
    global w,h,x,y,dx,dy,fingdisplist,scaling,root,canvas,typed,key_width,key_height,circlediameter,keyspacing,btn_list,kyb_list,curkeyb,numkeybs,changekeyb
    canvas.delete("all")
    changekeyb=False
    btnlist = kyb_list[curkeyb]
    ycorner=10
    for r in kyb_list[curkeyb]:
        xcorner=10
        for c in r:
            print c
            if c[0]=='*' and not len(c)==1:
                xcorner+= int(''.join(map(str,c[1:])))#one liner to convert list to num
                #specifies spacing used
            #elif c[0]=='+' and not len[c]==1:
                
            elif c == 'space':
                rect=canvas.create_rectangle(xcorner,ycorner,xcorner+7*key_width,ycorner+key_height,fill='gray',outline='black',tags="space")
                objt=canvas.create_text((7*key_width+2*xcorner)/2,(key_height+2*ycorner)/2,text=c,fill='white')
                xcorner+=keyspacing+key_width
            else:
                rect=canvas.create_rectangle(xcorner,ycorner,xcorner+key_width,ycorner+key_height,fill='gray',outline='black',tags=c)
                objt=canvas.create_text((key_width+2*xcorner)/2,(key_height+2*ycorner)/2,text=c,fill='white')
                xcorner+=keyspacing+key_width
        ycorner+=keyspacing+key_height

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        global w,h,x,y,dx,dy,fingdisplist,scaling,root,canvas,typed,key_width,key_height,circlediameter,keyspacing,btn_list,kyb_list,curkeyb,numkeybs,changekeyb,lastswipe
        for finger in fingdisplist:
                canvas.delete(finger)
                fingdisplist = []
        frame = controller.frame()

        ##print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        ##      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if not frame.hands.is_empty:
            # Get the first hand
            for hand in frame.hands:
                # Check if the hand has any fingers
                fingers = hand.fingers
                if not fingers.is_empty:
                    # Calculate the hand's average finger tip position
                    avg_pos = Leap.Vector()
                    for finger in fingers:
                        fingdisplist.append(canvas.create_oval( w/2+scaling*(finger.tip_position[0]), h/2+scaling*(finger.tip_position[2]) , w/2+scaling*(finger.tip_position[0])+circlediameter , h/2+scaling*(finger.tip_position[2])+circlediameter,fill='blue',outline=''))
                        #fingdisplist.append(a)
                        ##avg_pos += finger.tip_position
                        ##avg_pos /= len(fingers)
                        #canvas.delete(a)
                        #print "Hand has %d fingers, finger drawn: %s" % (len(fingers), finger.tip_position)
                        
        #use find_overlapping(x1,y1,x2,y2) to find rectangle that it is inside
        #use a bounding box that is tall enough that it goes a little past the height of a key
        #then check each of the tuples for left <= x <= right, top <= y <= bottom
        #if any satisfy, it is hitting that key => set the key a different shade for a sec and register the letters
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                #print "Key Tap Position: %s, direction %s" % (keytap.position, keytap.direction)
                xtap=int(w/2+scaling*(keytap.position[0]))
                ytap=int(h/2+scaling*(keytap.position[2]))
                overlapkeys = canvas.find_overlapping(xtap-1,ytap-(key_height/2+1),xtap+1,ytap+(key_height/2+1))
                #print len(overlapkeys)

                for posskey in overlapkeys:
                    tempcoords = canvas.coords(posskey)
                    if len(tempcoords)<4:
                        print tempcoords
                        continue#some error that occurs randomly when I type due to temp coords not containing 4 entries specifying 2 coordinates
                    if tempcoords[0] < xtap and xtap < tempcoords[2] and tempcoords[1] < ytap and ytap < tempcoords[3]:
                        if canvas.type(posskey)=="rectangle":
                            pressedkey = canvas.gettags(posskey)[0]
                            print pressedkey
                            copytext()
                            #various key functions
                            if pressedkey=='Backspace':
                                typed.delete(len(typed.get())-1,END)
                            elif pressedkey=='space':
                                typed.insert(END,' ')
                            elif pressedkey=='Enter':
                                typed.insert(END,'\n')
                            elif pressedkey=='Shift':
                                curkeyb=(curkeyb+2)%(2*numkeybs)
                                updatekeyboard()
                            else:
                                typed.insert(END,canvas.gettags(posskey)[0])
            elif gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                #determines which direction you are circling
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"
            elif gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                if(controller.config.set("Gesture.Swipe.MinLength", 150.0) and controller.config.set("Gesture.Swipe.MinVelocity", 1500)):
                    controller.config.save()
                ishoriz = abs(swipe.direction[0]) > abs(swipe.direction[1])
                if lastswipe+1 > time.time():
                    return()
                lastswipe=time.time()
                if ishoriz:
                    if swipe.direction[0] > 0:
                        swipeDirection='right'
                        curkeyb=(curkeyb+1)%numkeybs
                        changekeyb=True
                    else:
                        swipeDirection='left'
                        curkeyb=(curkeyb+1)%numkeybs
                        changekeyb=True
                else:
                    if swipe.direction[1] > 0:
                        swipeDirection='up'
                        curkeyb=(curkeyb+numkeybs)%(2*numkeybs)
                        changekeyb=True
                    else:
                        swipeDirection='down'
                        curkeyb=(curkeyb-numkeybs)%(2*numkeybs)
                        changekeyb=True
                updatekeyboard()
                print swipe.direction, swipeDirection
            
                
                        
#
#Start of stuff
#

def main():
    global w,h,x,y,dx,dy,fingdisplist,scaling,root,canvas,typed,key_width,key_height,circlediameter,keyspacing,btn_list,kyb_list,curkeyb,numkeybs,changekeyb
    root=Tk()
    canvas=Canvas(root,width=w,height=h,bg='white')
    canvas.pack()
    #
    # Graphics objects. 
    #

    updatekeyboard()

    typed = Entry(root, bd =5, width=30)
    typed.pack()
    typed.place(relx=.45,rely=.9)
    #option to copy text in the program
    #just add button to get this to work, probably need a click event
    #root.withdraw()
    #root.clipboard_clear()
    #root.clipboard_append(typed.get())
    #root.destroy()
    


    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Gestures
    #
    # Callbacks.
    #
    ##root.bind('<Down>',down)
    ##root.bind('<Up>',up)
    ##root.bind('<Right>',right)
    ##root.bind('<Left>',left)
    root.bind('<q>',quit)


    #
    # Here we go.
    #
    root.mainloop()
if __name__ == '__main__': main()
