# Adithya Venkatesan
#
# keyboard
# need to work on getting key presses to work
#

from Tkinter import *
from sys import exit
import math

import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

w,h= 975,400
x,y,dx,dy=100,100,199,199
fingdisplist = []
scaling = 3.0

def quit(evnt):
	exit(0)

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
        global fingdisplist
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
                    if tempcoords[0] < xtap and xtap < tempcoords[2] and tempcoords[1] < ytap and ytap < tempcoords[3]:
                        if canvas.type(posskey)=="rectangle":
                            pressedkey = canvas.gettags(posskey)[0]
                            print pressedkey
                            #various key functions
                            if pressedkey=='Backspace':
                                typed.delete(len(typed.get())-1,END)
                            elif pressedkey=='space':
                                typed.insert(END,' ')
                            elif pressedkey=='Enter':
                                typed.insert(END,'\n')
                            elif pressedkey=='Shift':
                                shiftnextkey=True
                            else:
                                typed.insert(END,canvas.gettags(posskey)[0])
            elif gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                #determines which direction you are circling
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"
                #circle
                previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI
                if swept_angle > 3:
                    print 'circles!'
                        
                        

#
#Start of stuff
#

root=Tk()
canvas=Canvas(root,width=w,height=h,bg='white')
canvas.pack()
#
# Graphics objects. 
#

key_width = 70
key_height = 60
circlediameter = 20
keyspacing = 4
btn_list = [
['`','1','2','3','4','5','6','7','8','9','0','-','='],
 ['*20','q','w','e','r','t','y','u','i','o','p','Backspace'],
    ['*40','a','s','d','f','g','h','j','k','l',';','\'','Enter'],
    ['Shift','z','x','c','v','b','n','m',',','.','/','Shift'],
    ['*200','space']]

typed = Entry(root, bd =5, width=30)
typed.pack()
typed.place(relx=.45,rely=.9)
#option to copy text in the program
#just add button to get this to work, probably need a click event
#root.withdraw()
#root.clipboard_clear()
#root.clipboard_append(typed.get())
#root.destroy()

ycorner=10
for r in btn_list:
    xcorner=10
    for c in r:
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
