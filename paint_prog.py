from pygame import *
from random import *
import time
init()

def pentool():
    layer.set_clip((20,20,836,653))
    if mb[0] == 1:
        draw.line(layer,drawC1,(omx,omy),(mx,my),thick)
    elif mb[2] == 1:
        draw.line(layer,drawC2,(omx,omy),(mx,my),thick)

def linetool():
    screen.set_clip((20,20,836,653))
    if mb[0] == 1:
        screen.blit(newscreen,(0,0))
        draw.line(screen,drawC1,(x,y),(mx,my),thick)
    elif mb[2] == 1:
        screen.blit(newscreen,(0,0))
        draw.line(screen,drawC2,(x,y),(mx,my),thick)  
            
def brushtool():
    layer.set_clip((20,20,836,653))
    dx,dy = omx-mx,omy-my
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(mx+i/distance*dx)
        y = int(my+i/distance*dy)
        if mb[0] == 1:
            draw.circle(layer,drawC1,(x,y),thick*7)
        elif mb[2] == 1:
            draw.circle(layer,drawC2,(x,y),thick*7)

#FIX ERASERTOOL            
def erasetool():
    layer.set_clip((20,20,836,653))
    if mb[0] == 1 and Rect(20,20,836,653).collidepoint((mx-20,my-20)):
        eraseRect = Rect(mx-20,my-20,40,40)
        if layer == canvas1:
            layer.blit(background.subsurface(eraseRect),(mx-20,my-20))
        else:
            layer.blit(canvases[canvases.index(layer)-1].subsurface(eraseRect),(mx-20,my-20))
        
def recttool():
    screen.set_clip((20,20,836,653))
    if mb[0] == 1:
        screen.blit(newscreen,(0,0))
        draw.rect(screen,drawC1,(x,y,mx-x,my-y),thick)
    if mb[2] == 1:
        screen.blit(newscreen,(0,0))
        draw.rect(screen,drawC2,(x,y,mx-x,my-y),thick)
    elif ev.type == MOUSEBUTTONUP:
        if ev.button == 1:
            draw.rect(layer,drawC1,(x,y,mx-x,my-y),thick)
        elif ev.button == 3:
            draw.rect(layer,drawC2,(x,y,mx-x,my-y),thick)

def ellipsetool():
    screen.set_clip((20,20,836,653))
    if abs(mx-x)>thick*2+1:
        if mb[0] == 1:
            screen.blit(newscreen,(0,0))
            draw.ellipse(screen,drawC1,(min(mx,x),min(my,y),abs(mx-x),abs(my-y)),thick)
        elif mb[2] == 1:
            screen.blit(newscreen,(0,0))
            draw.ellipse(screen,drawC2,(min(mx,x),min(my,y),abs(mx-x),abs(my-y)),thick)
        elif ev.type == MOUSEBUTTONUP:
            if ev.button == 1:
                draw.ellipse(layer,drawC1,(min(mx,x),min(my,y),abs(mx-x),abs(my-y)),thick)
            if ev.button == 3:
                draw.ellipse(layer,drawC2,(min(mx,x),min(my,y),abs(mx-x),abs(my-y)),thick)
            
            
def spraytool():
    layer.set_clip((20,20,836,653))
    for i in range(thick*30):
        x = randint(mx-thick*10,mx+thick*10)
        y = randint(my-thick*10,my+thick*10)
        d = ((mx-x)**2 + (my-y)**2)**0.5
        if d <= thick*10:
            if mb[0] == 1:
                draw.circle(layer,drawC1,(x,y),0)
            if mb[2] == 1:
                draw.circle(layer,drawC2,(x,y),0)

def stamptool():
    global grow, turn, stampw, stamph, changedstamp
    screen.set_clip((20,20,836,653))    
    if currentstamp in stamppics:
        if mb[0] == 1:
            if keypress[K_LEFT] == True:
                turn += 20
            elif keypress[K_RIGHT] == True:
                turn -= 20
            if keypress[K_UP] == True:
                grow += 0.1   
            elif keypress[K_DOWN] == True:
                if grow>0.1:
                    grow -= 0.1
            changedstamp = transform.rotozoom(currentstamp, turn, grow)
            stampw, stamph = changedstamp.get_width(), changedstamp.get_height()
            screen.blit(newscreen,(0,0))
            screen.blit(changedstamp,(mx-stampw//2,my-stamph//2))
        elif ev.type == MOUSEBUTTONUP:
            layer.blit(changedstamp,(mx-stampw//2,my-stamph//2))
            
    
#FIX SELECTTOOL
def selecttool():
    global selectRect, selected, sx, sy
    layer.set_clip((20,20,836,653))
    if mb[0] == 1:
        screen.blit(newscreen,(0,0))      
        selectRect = draw.rect(screen,(0,0,0),(x,y,mx-x,my-y),1)
        selected = layer.subsurface(selectRect).copy()
        sx,sy = selected.get_size()
    elif mb[2] == 1 and selectRect.collidepoint((x,y)):
        screen.blit(newscreen,(0,0))
        screen.blit(selected,(mx-sx//2,my-sy//2))
        layer.blit(background.subsurface(selectRect).copy(),selectRect)
        if len(canvases)>1:
            for i in range(len(toplayer)-1):
                layer.blit(toplayer[i].subsurface(selectRect).copy(),selectRect)
    elif ev.type == MOUSEBUTTONUP:
        if ev.button == 3:
            layer.blit(selected,(mx-sx//2,my-sy//2))

                    
def eyedroptool():
    global drawC1, drawC2
    if mb[0] == 1:
        drawC1 = layer.get_at((mx,my))
    elif mb[2] == 1:
        drawC2 = layer.get_at((mx,my))

#FIX FILLTOOL
def filltool(mx,my):
    layer.set_clip((20,20,836,653))
    if mb[0] == 1:
        col = layer.get_at((mx,my))
        if col == drawC1:
            return
        edge=[(mx,my)]
        layer.set_at((mx, my), (0,0,0))
        for (mx, my) in edge:
            for (x, y) in ((mx+1, my), (mx-1, my), (mx, my+1), (mx, my-1)):
                if canvasRect.collidepoint((x,y)) == False: break
                if layer.get_at((x, y)) == col:
                    layer.set_at((x, y),drawC1)
                    edge.append((x, y))
    if mb[2] == 1:
        col = layer.get_at((mx,my))
        if col == drawC2:
            return
        edge=[(mx,my)]
        layer.set_at((mx, my), (0,0,0))
        for (mx, my) in edge:
            for (x, y) in ((mx+1, my), (mx-1, my), (mx, my+1), (mx, my-1)):
                if canvasRect.collidepoint((x,y)) == False: break
                if layer.get_at((x, y)) == col:
                    layer.set_at((x, y),drawC2)
                    edge.append((x, y))
#FIX BLANKTOOL
def blanktool(current):
    global tool
    layer.set_clip((20,20,836,653))
    screen.blit(background.subsurface(canvasRect),(0,0))
    draw.rect(layer,(0,0,0,0),canvasRect)
    if current == "blank":
        tool = ''

def invertLayer():
    if layer in canvases:
        layer.set_clip((20,20,836,653))
        for i in range(20,856):
            for j in range(20,673):
                a,b,c,d = layer.get_at((i,j))
                layer.set_at((i,j),(255-a,255-b,255-c,d))

def rainbowmode():
    global rpos, drawC1, drawC2
    layer.set_clip((20,20,836,653))
    if mb[0] == 1:
        rpos += 1
        drawC1 = screen.get_at((rpos,764))
    elif mb[2] == 1:
        rpos += 1
        drawC2 = screen.get_at((rpos,764))
    if rpos>1133:
        rpos = 881

def getTheme():
    global theme, background, layer, allTools, toolcopy
    theme += 1
    if theme >3:
        theme = 1
    if theme == 1:
        background = cathat
    elif theme == 2:
        background = lorax
    elif theme == 3:
        background = horton

    screen.blit(background,(0,0))
    allTools = background.subsurface(toolArea).copy()
    toolcopy = screen.subsurface(toolArea).copy()
    selectTool()
    
def playMusic():
    global musicOn
    if musicOn == True:
        musicOn = False
    else:
        musicOn = True
        
    if musicOn == False:
        mixer.music.pause()
    elif musicOn == True:
        mixer.music.unpause()

def loadPics():
    for i in range(len(stamps)):
        stamp = image.load(stamps[i]+".png")
        icon = image.load(stamps[i]+"icon.png")
        stamppics.append(stamp)
        stampicons.append(icon)

def blit_stamps():
    global scrolling
    stampSurf.blit(stampSurfcopy,(0,0))
    for i in range(len(stamps)):
        if i<4:
            rect_stamp = Rect(873+65*i,421,62,60)
            stamprect.append(rect_stamp)
            stampSurf.blit(stampicons[i],(2+65*i,0+scrolling))
        else:
            stampSurf.blit(stampicons[i],(2+65*(i-4),65+scrolling))
        
def selectStamp():
    global currentstamp, stampw, stamph, grow, turn, scrolling, stampOn
    if stampOn == False:
        blit_stamps()
    if stampOn == False:
        stampOn = True
    else:
        stampOn = False
    for i in range(4):
        if stamprect[i].collidepoint((mx,my)) and mb[0] == 1:
            if scrolling == 0:
                draw.rect(screen,(0,0,0),stamprect[i],3)
                currentstamp = stamppics[i]
            if scrolling == -65:
                if i==0 or i==1:
                    draw.rect(screen,(0,0,0),stamprect[i],3)
                    currentstamp = stamppics[i+4]
            if currentstamp in stamppics:
                stampw,stamph = currentstamp.get_size()
            grow = 1.0
            turn = 0
            
def blit_tools():
    for i in range(len(toolbelt)):
        if i<7:
            rect_i = Rect(105+i*65,710,45,45)
        else:
            rect_i = Rect(105+(i-7)*65,780,45,45)
        toolrect.append(rect_i)

def highlightTool():
    global toolcopy
    if toolArea.collidepoint((mx,my)):
        for i in range(len(toolrect)):
            if toolrect[i].collidepoint((mx,my)):
                screen.blit(toolcopy,toolArea)
                draw.rect(screen,(255,0,0),toolrect[i],3)
                if tool == toolbelt[i]:
                    draw.rect(screen,(255,255,255),toolrect[i],3)
    else:
        screen.blit(toolcopy,toolArea)
        
    if layerArea.collidepoint((mx,my)):
        for i in range(len(layerRect)):
            if layerRect[i].collidepoint((mx,my)):
                if layerclick == 2:
                    screen.blit(layer2,layerRect[0])
                elif layerclick >= 3:
                    screen.blit(layer3,layerRect[0])
                draw.rect(screen,(0,0,0),layerRect[i],3)
            if layer in canvases:
                draw.rect(screen,(255,255,255),layerRect[canvases.index(layer)],3)
    else:
        if layerclick == 2:
            screen.blit(layer2,layerRect[0])
        elif layerclick >= 3:
            screen.blit(layer3,layerRect[0])
        else:
            screen.blit(layercopy,layerArea)
        if layer in canvases:
            draw.rect(screen,(255,255,255),layerRect[canvases.index(layer)],3)

    if addArea.collidepoint((mx,my)):
        for i in range(len(addlist)):
            if addlist[i].collidepoint((mx,my)):
                screen.blit(background.subsurface(addArea),addArea)
                draw.rect(screen,(4,149,186),addlist[i],3)
                if ev.type == MOUSEBUTTONDOWN:
                    draw.rect(screen,(255,0,0),addlist[i],3)
    else:
        screen.blit(background.subsurface(addArea),addArea)
def selectTool():
    global tool, toolcopy
    screen.blit(allTools,toolArea)
    for i in range(len(toolbelt)):
        if toolrect[i].collidepoint((mx,my)) and mb[0] == 1:
            #screen.blit(allTools,toolArea)
            draw.rect(screen,(4,149,186),toolrect[i],3)  
            tool = toolbelt[i]
            toolcopy = screen.subsurface(toolArea).copy()
               
        
def addLayer():
    global canvases
    if layerclick == 2:
        layerRect.append(Rect(875,313,262,46))
        canvases = [canvas1,canvas2]
        screen.blit(layer2,layerRect[0])
    elif layerclick == 3:
        layerRect.append(Rect(875,364,263,46))
        canvases = [canvas1,canvas2,canvas3]
        screen.blit(layer3,layerRect[0])
        
    if layer in canvases:
        draw.rect(screen,(255,255,255),layerRect[canvases.index(layer)],2)
        
#def deleteLayer():
 #   global layer
  #  if layer in canvases[1::]:
   #     if layer == canvas2:
    #        screen.blit(layer1_3,layerRect[0])
     #       layer.fill((255,255,255))
      #  elif layer == 3:
       #     screen.blit(layer2,layerRect[0])
        #    layer.fill((255,255,255))
        #toplayer.insert(0,toplayer.pop(toplayer.index(layer)))
        #layer = ''
            
def duplicateLayer():
    global canvas2, canvas3, canvases
    if layer in canvases:
        double = layer.copy()
        if layerclick == 2:
            layerRect.append(Rect(875,313,261,45))
            canvas2 = double
            canvases = [canvas1,canvas2]
            screen.blit(layer2,layerRect[0])
        elif layerclick == 3:
            layerRect.append(Rect(875,364,261,45))
            canvas3 = double
            canvases = [canvas1,canvas2,canvas3]
            screen.blit(layer3,layerRect[0])
        if layer in canvases:
            draw.rect(screen,(255,255,255),layerRect[canvases.index(layer)],2)
    
def selectLayer():
    global layer, toplayer,layercopy
    for i in range(len(layerRect)):
        if layerRect[i].collidepoint((mx,my)) and ev.type == MOUSEBUTTONDOWN:
            layer = canvases[i]
            del toplayer[0]
            toplayer.append(layer)
            showLayer()
    
def showLayer():
    if layer in canvases:
        if layerclick == 2:
            screen.blit(layer2,layerRect[0])
        elif layerclick >= 3:
            screen.blit(layer3,layerRect[0])
        draw.rect(screen,(255,255,255),layerRect[canvases.index(layer)],2)

def makeThick():
    global thick, scrollmy
    if my in range(708,821):
        scrollmy = my
        screen.blit(thickSlide,thickArea)
        screen.blit(knob,(557,scrollmy-8))
        thick = 5-(my-708)//19
        if tool != "ellipse" or tool != "rect":
            if thick == 0:
                thick = 1
        
def makeFade():
    global drawC1,drawC2
    if my in range(708,820):
        screen.blit(fadeSlide,fadeArea)
        screen.blit(knob,(598,my-8))
        drawC1.a = int(225-(my-708)//0.43921568627450980392156862745098) 
      
running = True
screen = display.set_mode((1152,864))
canvasRect = Rect(0,0,856,673)

#THEME STUFF#######################################################
cathat = image.load("catinthehat.png")
lorax = image.load("lorax.png")
horton = image.load("horton.png")

bgpic = [cathat,lorax,horton]
for i in range(len(bgpic)):
    bgpic[i] = bgpic[i].convert_alpha()
    
theme = 1
changeTheme = Rect(18,700,62,63)
background = cathat

screen.blit(cathat,(0,0))

#MUSIC STUFF#######################################################
music = Rect(18,773,62,63)
musicOn = True

song = mixer.music.load("Music/Up Soundtrack-Up With Tiles.mp3")
mixer.music.pause()

#DRAWING STUFF#####################################################
canvas1 = Surface((856,673),SRCALPHA)
canvas2 = Surface((856,673),SRCALPHA)
canvas3 = Surface((856,673),SRCALPHA)
canvases = [canvas1]

spectrum = Rect(881,688,253,152)
drawC1 = Color(0,0,0)
drawC2 = Color(255,255,255)
rpos = 881
thick = 1

mx,my = 0,0
rainOn = False
#STAMP STUFF########################################################
stamps = ["cat","thing1","thing2","fish","boy","girl"]
stamppics = []
stampicons = []
stamprect = []

stampArea = Rect(871,421,261,125)
stampSurf = screen.subsurface(stampArea)
stampSurfcopy = screen.subsurface(stampArea).copy()
currentstamp = ''

stampOn = False
scrolling = 0

stampw,stamph = 0,0
stampSurf.set_clip(0,0,261,63)
loadPics()
#TOOLS STUFF##################################################
toolbelt = ["pen","line","brush","erase","ellipse","rect","spray",
            "polygon","stamp","select","text","eyedrop","fill","blank"]
toolrect = []
toolArea = Rect(100,705,445,125)
allTools = background.subsurface(toolArea).copy()
toolcopy = allTools.copy()
tool = ''

blit_tools()
#LAYER STUFF##################################################
layerArea = Rect(870,260,267,152)
layercopy = background.subsurface(layerArea)

layerRect = [Rect(875,264,261,45)]

layer = ''
toplayer = [canvas3,canvas2,canvas1]

#ADD AND DELETE LAYERS STUFF##################################
add = Rect(972,207,48,48)
delete = Rect(1029,207,48,48)
duplicate = Rect(1087,207,48,48)
addlist = [add,delete,duplicate]
addArea = Rect(962,202,178,54)
layerclick = 1

layer1 = image.load("layer1.png")
layer2 = image.load("layer2.png")
layer3 = image.load("layer3.png")
layer1_3 = image.load("layer1-3.png")


#UNDO AND REDO STUFF##########################################
undopos = 0
undolist = [canvas1.copy()]
undobut = Rect(783,690,79,74)
redobut = Rect(783,771,79,74)

#SLIDER STUFF#################################################
thickArea = Rect(542,700,42,138)
thickSlide = background.subsurface(thickArea).copy()
fadeArea = Rect(584,700,42,138)
fadeSlide = background.subsurface(fadeArea).copy()

knob = transform.scale(image.load("knob.png"),(16,16))
screen.blit(knob,(557,812))
screen.blit(knob,(598,700))
scrollmy = 820
selectRect = Rect(0,0,0,0)

use = True
while running:
    omx,omy = mx,my
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()
    keypress = key.get_pressed()
    for ev in event.get():
        if ev.type == QUIT:
            running = False
            
        if ev.type == MOUSEBUTTONUP:
            print(undolist)
            if layer in canvases and canvasRect.collidepoint((mx,my)):
                if tool == "line":
                    if ev.button == 1:
                        draw.line(layer,drawC1,(x,y),(mx,my),thick)
                    elif ev.button == 3:
                        draw.line(layer,drawC2,(x,y),(mx,my),thick)
                    
                if undopos<len(undolist)-1:
                    del undolist[undopos+1::]
                undolist += [layer.copy()]
                undopos+=1
                    
        if ev.type == MOUSEBUTTONDOWN:
            if ev.button == 1 or ev.button == 3:
                x,y = mx,my  
                newscreen = screen.copy()
                
            if ev.button == 4:
                if scrolling<0:
                    scrolling += 5    
            elif ev.button == 5:
                if scrolling>-65:
                    scrolling -= 5
        
            if undobut.collidepoint((mx,my)) and undopos>0:
                undopos-=1
                blanktool(tool)
                layer.blit(undolist[undopos],(0,0))
            if redobut.collidepoint((mx,my)) and undopos<len(undolist)-1:
                undopos+=1
                layer.blit(undolist[undopos],(0,0))
                
        if ev.type == KEYDOWN:
            if ev.key == K_w:
                drawC1 = (255,255,255)
            elif ev.key == K_b:
                drawC1 = (0,0,0)
            if ev.key == K_i:
                invertLayer()
            if ev.key == K_r:
                if rainOn == False:
                    rainOn = True
                else:
                    rainOn = False
    
    if changeTheme.collidepoint((mx,my)) and ev.type == MOUSEBUTTONDOWN:
        getTheme()

    if music.collidepoint((mx,my)) and ev.type == MOUSEBUTTONDOWN:
        playMusic()

    if spectrum.collidepoint((mx,my)):
        if mb[0] == 1:
            drawC1 = screen.get_at((mx,my))
        if mb[2] == 1:
            drawC2 = screen.get_at((mx,my))

    screen.set_clip(None)
    
    if add.collidepoint((mx,my)) and ev.type == MOUSEBUTTONDOWN:
        layerclick += 1
        addLayer()
    elif delete.collidepoint((mx,my)) and ev.type == MOUSEBUTTONDOWN:
        pass
        #deleteLayer()
    elif duplicate.collidepoint((mx,my)) and ev.type == MOUSEBUTTONDOWN:
        layerclick += 1
        duplicateLayer()

        
    if layerArea.collidepoint((mx,my)):
        selectLayer()

    if thickArea.collidepoint((mx,my)) and mb[0] == 1:
        makeThick()

    if fadeArea.collidepoint((mx,my)) and mb[0] == 1:
        makeFade()
       
    if toolArea.collidepoint((mx,my)):
        if mb[0] == 1:
            selectTool()
    elif toolArea.collidepoint((mx,my)) == False:
        screen.blit(toolcopy,toolArea)
     
    if tool == "stamp":
        selectStamp()
    else:
        screen.blit(stampSurfcopy,stampArea)
    highlightTool()
    if layer in canvases:
        if canvasRect.collidepoint((mx,my)):
            if rainOn == True:
                rainbowmode()
            if tool == "pen":
                pentool()
            elif tool == "line":
                linetool()
            elif tool == "brush":
                brushtool()
            elif tool == "erase":
                erasetool()
            elif tool == "rect":
                recttool()
            elif tool == "ellipse":
                ellipsetool()
            elif tool == "spray":
                spraytool()
            elif tool == "stamp":
                stamptool()
            elif tool == "select":
                selecttool()
            elif tool == "eyedrop":
                eyedroptool()
            elif tool == "fill":
                if canvasRect.collidepoint((x,y)):
                    filltool(x,y)
    if tool == "blank":
        draw.rect(screen,(255,0,0),toolrect[toolbelt.index("blank")],3)
        if layer in canvases:
            blanktool(tool)
        elif toolrect[toolbelt.index("blank")].collidepoint((mx,my)) and ev.type == MOUSEBUTTONUP:
            tool = ''
    elif tool not in toolbelt:
        highlightTool()
            
    if mb[0] == 1:
        print(mx,my)
    
    if layer in canvases:
        for i in toplayer:
            screen.blit(i,(0,0))
    
    draw.rect(screen,drawC1,(635,710,45,45),0)
    draw.rect(screen,drawC2,(635,780,45,45),0)
    display.update()
    display.flip()
quit()
