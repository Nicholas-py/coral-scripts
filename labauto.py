import re
import matplotlib.pyplot as plt
from mss import mss
import pyautogui as ag
import pytesseract as pt
import numpy as np
from time import sleep
import os
import glob
import pymupdf
from PIL import Image
from textdistance import levenshtein as stringdist
from unidecode import unidecode

namesensitivity = 2
unitsensitivity = 2
maximumwords = 4
bottomtesttoextras = 26
bottomindex = 78

pt.pytesseract.tesseract_cmd = r'C:\Users\nicho\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
PSM_MODE = '--psm 1'


#THINGS TO SPEED UP
# y Type results in website order, not order of toenter
# y Filter out common non-lines (page #, names, etc)
# y Get other tests (ht, GR nuclees, etc) and enter them automatically in other box
# y Strip < from numbers
# - special case vit d
# - Catch order of magnitude errors

def lineistest(line):
    tokens = line.split()
    firstnumber = 0
    
    for i in range(1,maximumwords+1):
        try:
            tokens[i] = float(tokens[i].replace(',','.'))
            firstnumber = i
            break
        except ValueError:
            pass
        except IndexError:
            return

    if firstnumber == 0:
        return None

    if len(tokens) < 3 or len(tokens) > 14:
        return None
    
    name = clearjunk(' '.join(tokens[0:firstnumber])).lower()

    namematches = None
    mindist = 100
    for i in testindexes:
        if stringdist(name, i) <= min(mindist, len(name)-2,namesensitivity):
            namematches = i
            mindist = stringdist(name, i)
    if namematches is None:
        for i in ignorelist:
            if stringdist(name.strip(),i) < 2:
                return None
        #print(line, end = '      ')
        #print('Rejected for name',name,'not test')
        return None

    print(line, end = '      ')
    testindex = testindexes[namematches]
    value = tokens[firstnumber]
    requiredunits = units[testindex]
    possibleunitsr = [clearjunk(' '.join(tokens[firstnumber+1:firstnumber+2])),
                clearjunk(' '.join(tokens[firstnumber+2:firstnumber+3])),
                clearjunk(' '.join(tokens[firstnumber+3:firstnumber+4])),
                clearjunk(' '.join(tokens[firstnumber+4:firstnumber+5])),
                clearjunk(' '.join(tokens[firstnumber+5:firstnumber+6]))]
    possibleunits = []
    for i in possibleunitsr:
        if i is not None:
            possibleunits.append(i)
    if requiredunits:
        unitline = -1
        for i in possibleunits:
            if i is not None:
                for j in requiredunits:
                    if stringdist(i,j) < unitsensitivity:
                        unitline = possibleunits.index(i)
        if unitline == -1:
            print('Rejected for range + units ('+' '.join(possibleunits)+' not '+' '.join(requiredunits)+') not correct')
            return True
    #all tests passed
    print('Accepted!')
    print('Name:',namematches,'value',value,'range+units:',' '.join(possibleunits))
    return (namematches,testindex, value)

def screenshot(bounds, show = False, french = False):
    shot = mss()
    arr = np.asarray(shot.grab(bounds))
    threshold = 1000

    channel_sum = arr.sum(axis=2)

    mask = channel_sum > threshold

    arr[mask]  = np.array([255, 255, 255, 255])
    arr[~mask] = np.array([0, 0, 0, 255])
    if show:
        plt.imshow(arr)
        plt.show()
    if french:
        text = pt.image_to_string(arr,config=PSM_MODE, lang='fra')
    else:
        text = pt.image_to_string(arr, config=PSM_MODE)
    if show:
        print(text.strip())
    return text

def clearjunk(name):
    if not name:
        return
    strippables = ['.','_',',','<','08 ','. ']
    for i in strippables:
        if name[-len(i):] == i:
            name = name[0:-len(i)]
        if not name:
            return ''
    for i in strippables:
        if name[0:len(i)] in strippables:
            name = name[len(i):]
        if not name:
            return ''
    nouse = '°”{}:'
    for i in nouse:
        name = name.replace(i,'')
    return name.lower()

def moveup():
    global currentline

    if currentline == 0:
        raise ZeroDivisionError('Attempt to move up when at top')
    if not tests[currentline-1]:
        currentline -= 1
        ag.hotkey('shift','tab')
    currentline -= 1
    ag.hotkey('shift','tab')
    ag.hotkey('shift','tab')
def movedown():
    global currentline
    if currentline == bottomindex - 1:
        currentline += 2
        for i in range(bottomtesttoextras):
            ag.hotkey('tab')
            sleep(0.05)
        return
    if currentline > bottomindex:
        ag.write(' ')
        currentline += 1
        return
    if not tests[currentline+1]:
        currentline += 1
        ag.hotkey('tab')
    currentline += 1
    ag.hotkey('tab')
    ag.hotkey('tab')

def enter(toenter):
    global currentline
    currentline = 0

    toenter.sort(key=lambda x:x[1])
    
    for i in toenter:
        print('Entering',i[0]+'...')
        target = i[1]
        tally = 0
        while currentline != target:
            if currentline > target:
                moveup()
            else:
                movedown()
            if tally > len(tests)+10:
                raise ZeroDivisionError("Could not reach target "+str(target))
        if target > bottomindex:
            ag.write(unidecode(i[0])+' ')
        ag.write(str(i[2]))
        print('Entered',i[2])


def gettestsandindexdict():
    file = open('tests.txt',encoding='utf-8')
    tests = file.read().split('\n')
    for i in range(len(tests)):
        if tests[i]:
            tests[i] = tests[i].lower().split(', ')
    testindexes = {}
    extras = False
    for i in range(len(tests)):
        for j in tests[i]:
            testindexes[j] = i
    return tests,testindexes

def getunits():
    file = open('units.txt',encoding='utf-8')
    units = file.read().split('\n')
    for i in range(len(units)):
        if units[i]:
            units[i] = units[i].lower().split(', ')
    return units
    
def gettestsfrominput():
    toenter = []
    while True:
        datas = input().lower().split(' ')
        if datas == ['q']:
            raise SystemExit("Exiting")
        if len(datas) == 1:
            if datas[0] == '':
                return toenter
            print('Enter value as well')
            continue
        try:
            value = float(datas[-1])
        except ValueError:
            print('Rearrange')
            continue
        name = ' '.join(datas[0:-1])
        if name not in testindexes:
            print('Test not found, please try again')
        else:
            j = 0
            for i in range(len(toenter)):
                if toenter[i-j][0] == name:
                    toenter.pop(i-j)
                    j+=1
            toenter.append((name, testindexes[name], value))
            print('Accepted',name+':',value)

def experiments(pix):
            l = []
            plist = list(pix.samples)
            print(len(plist))
            lx = []
            ly = []
            #print(min(plist))
            #exit()
            ratio = (len(plist)/(pix.width * pix.height))
            print(ratio)
            width = int(pix.width * 3)
            height = int(pix.height )
            for i in range(0,len(plist)):
                if plist[i] < 100:
                    lx.append(i%width)
                    ly.append(height-i//width)
                #l.append(suum)
            for i in range(height):
                suum = 0
                for j in range(width):
                    if plist[i*width + j] < 100:
                        suum += 1
                lx.append(width + suum)
                ly.append(height-i)
            plt.scatter(lx,ly)
            plt.show()
    

while True:
    print('Will run through the most recently downloaded PDF and print if it detects a test at each line. Please enter any that it misses')
    #numtests = int(input('How many tests are there on the pdf you downloaded?'))

    inp = input('French or english?').lower()
    french = 'f' in inp
    lang = 'fra' if french else 'eng'
    
    tests, testindexes = gettestsandindexdict()
    units= getunits()
    ignorelist = list(map(lambda x:x.lower(),open('ignorelist.txt',encoding='utf-8').read().split('\n')))
    
    assert len(units) == len(tests)
    assert 'umol/l' in units[testindexes['dheas']]


    pdfbounds = {'top':142,'left':0,'width':1000,'height':988}

    text = ''
    downloads = glob.glob('c:/Users/nicho/Downloads/*.pdf')
    print('reading file',max(downloads, key=os.path.getctime))
    with pymupdf.open(max(downloads, key=os.path.getctime)) as doc:
        for page in doc:
            pix = page.get_pixmap(dpi=305)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += pt.image_to_string(img, lang=lang)

    
    
    print('O.1',text.count('O.1'), '£L', text.count(' £L'))
    text = text.replace('£l','fl').replace('O.1','0.1')

    text = text.replace('<','')

    if 'ptext' in inp:
        print(text)
        continue
    
    lines = text.split('\n')        
    print('len',len(text), 'lines',len(lines))
    #print(text)
    
    #for i in range(len(lines)):
     #   print(lines[i])


    try:
        toenter = []
        names = []
        for i in lines:
            result = lineistest(i)
            if result and result is not True and result[0] not in names:
                toenter.append(result)
                names.append(result[0])
            if result is not None:
                [toenter.append(i) for i in gettestsfrominput()]
    except SystemExit:
        pass
        

        

    

    print('#'*50)
    print()
    print()
    print('Processed',len(toenter),'tests')
    print(', '.join(map(lambda x:x[0], toenter)))
    if 'y' in input('Enter more tests? '):
        [toenter.append(i) for i in gettestsfrominput()]
                
            
        
    if 'y' in input('Are you ready to automatically enter the tests?'):
        print('Okay, please click on the first entry in the coral lab upload page.')
        sleep(3)
        print('About to start...')
        sleep(2)
        enter(toenter)
    
                        
            


