import pyautogui as ag
import pytesseract as pt
import time
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from mss import mss
import numpy as np
import matplotlib.pyplot as plt
import pyperclip

pt.pytesseract.tesseract_cmd = r'C:\Users\nicho\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
ag.PAUSE = 0
def screenshot(bounds, show = False):
    global sleeptally
    scttime = time.time()
    shot = mss()
    arr = np.asarray(shot.grab(bounds))
    if show:
        plt.imshow(arr)
        plt.show()
    text = pt.image_to_string(arr,config='--psm 7')
    if show:
        print(text.strip())
    sleeptally += time.time()-scttime
    return text

times = []
lasttime = 0
def section(name):
    global lasttime, times
    curtime = time.time()
    times.append((name, curtime-lasttime))
    lasttime = curtime

sleeptally = 0
def sleep(s):
    global sleeptally
    sleeptally += s
    time.sleep(s)

lastdate = ''
print('Ensure:\n'+
      'Printer mode is set to "save to PDF"')
print('The first tab is the EMR, logged in.')
print('File explorer defaults to the downloads page')
def run():
    global lasttime, times, sleeptally, lastdate
    if lastdate:
        print('Prev date was', lastdate.strftime("%B"),lastdate.day, lastdate.year)
    startdate = input('Date of form: ')
    formname = input('Form initials: ').upper()
    if not formname:
        formname = 'ST'
    if startdate and startdate in '1234567891011':
        lastdate += relativedelta(days=int(startdate))
        date = lastdate
    elif startdate:
        date = parse(startdate)
        lastdate = date
    elif lastdate:
        date = lastdate
    else:
        raise Exception("No date provided")
    month = date.strftime("%B")
    day = date.day
    year = date.year
    print(day,month,year)
    sleep(1)
    print('Will take over mouse in 2 seconds, please hover over the member link')
    sleep(2)

    linkpos = ag.position()
    
    sleeptally = 0
    starttime = time.time()
    lasttime = starttime
    
    ag.click()

    #Wait for website to load - important!
    sleep(2.5)

    pos = ag.locateCenterOnScreen('copybutton.png')
    ag.moveTo(pos)
    ag.move(0,10)
    ag.click()
    sleep(0.1)
    name = pyperclip.paste().title()
    
    #namebounds = {'top':350,'left':540,'width':500,'height':50}
    #name = screenshot(namebounds).strip().replace('-',' ')

    trashfound = ['oO','[9', '(9','(0','(Q','{Q']
    for i in trashfound:
        name = name.replace(' '+i,'')
    letters = 'QWERTYUIOPASDFGHJKLZXCVBNMÀÁÂÃÄÅĀĂĄǍȀȂȦẠẢẤẦẨẪẬẮẰẲẴẶÆḂḄḆÇĆĈĊČĎĐḊḌḎḐḒÈÉÊËĒĔĖĘĚȄȆẸẺẼẾỀỂỄỆḞĜĞĠĢǦǴĤḢḤḦḨḪÌÍÎÏĨĪĬĮIǏȈȊỊỈĴJ̌ĶḰḲḴĹĻĽĿŁḶḸḺḼḾṀṂÑŃŅŇṄṆṈṊÒÓÔÕÖŌŎŐǑȌȎȮỌỎỐỒỔỖỘỚỜỞỠỢŒṔṖŔŖŘȐȒṘṚṜṞŚŜŞŠṢṠṤṦṨSSŤŦṬṮȚṰÙÚÛÜŨŪŬŮŰŲǓȔȖỤỦỨỪỬỮỰṲṶṸṺẀẂŴẄẆẈẊẌÝŸŶȲẎỴỶY̊ỲŹŻŽẐẒẔ'

    acronym = ''
    maybestake = ''
    for i in name.split(' '):
        if len(i) > 1 and i[0] in letters:
            acronym += i[0]
        else:
            maybestake = i
    print(name, acronym)

    if name in ['Josée St-Onge', 'micheal pucyk', 'Yuan Chu Zi Lao', 'Nancy Da Silva']:
        print('\n MEMBER IS CURSED.\n')
        return
    
    sponsor = screenshot({'top':435,'left':552,'width':400,'height':50})
    if 'ponsored' in sponsor:
        boundschange = 60
        print(sponsor)
    else:
        boundschange = 30

    nurseloc = ag.locateCenterOnScreen('nurse.png',confidence = 0.9)
    nurse = screenshot({'top':nurseloc.y +30,'left':nurseloc.x+20,'width':250,'height':50})

    nurses = ['lefebvre','jessica', 'linda', 'proulx','labrecque','merat','silva','st-onge','truong']
    for i in nurses:
        if i in nurse.lower():
            nurse = i
            break
    else:
        print('Nurse',nurse,'not known (may be none)')
        nurse = None

    precloc = ag.locateCenterOnScreen('prescriber.png',confidence=0.9)
    prescriber = screenshot({'top':precloc.y +30,'left':precloc.x+2,'width':250,'height':50})

    prescribers = ['ariane','vicky','catarina','mcgraw','dionne','anais','duong','latulippe','keller','eisma']
    for i in prescribers:
        if i.lower() in prescriber.lower():
            prescriber = i
            break
    else:
        print('Prescriber',prescriber,'not known (may be none)')
        prescriber = None

    print(nurse, prescriber)

    section('Get info from coral app')
    
    #Navigate to form
    ag.hotkey('ctrl', 'w')
    ag.moveTo(linkpos)
    ag.move(0,27)
    sleep(0.2)
    ag.click()

    #Save
    sleep(1.2)
    ag.hotkey('ctrl','p')
    sleep(0.4)
    ag.write('\n')
    sleep(2.3) #at minimum
    string = acronym + '_'+formname+'_'+month[0:3]+str(day)
    print('Filename:',string)
    ag.write(string)
    sleep(0.79)
    ag.write('\n')
    sleep(0.25)
    ag.write('\n')

    section('Save pdf')
    
    #Open EMR calendar view
    sleep(0.1)
    ag.hotkey('ctrl','w')
    sleep(0.1)
    ag.hotkey('ctrl','1')
    ag.moveTo(115,178)
    sleep(0.2)
    ag.click()
    sleep(0.2)
    
    section('Open MYLE')
    
    #Find the member
    ag.moveTo(126,251)
    ag.click(clicks=3)
    ag.press('backspace')
    acroindex = 0
    for i in range(len(name.split(' '))):
        #Copy paste to allow special characters
        if not name.split(' ')[i] or acroindex >= len(acronym):
            continue
        if acroindex != 0 and acroindex != len(acronym)-1:
            acroindex+= 1
            continue
        if name.split(' ')[i][0].upper() == acronym[acroindex]:
            towrite = name.split(' ')[i]+' '
            if "'" in towrite:
                towrite = towrite.split("'")[0]
                if i > 1 and len(name.split(' ')[i-1]) > 1:
                    towrite = name.split(' ')[i-1]+' '
                    
            acroindex += 1
        else:
            continue
        pyperclip.copy(towrite)
        sleep(0.1)
        ag.hotkey('ctrl','v')
        sleep(0.2)

    ag.moveTo(135,366)
    sleep(0.8)

    paticons = ag.locateAllOnScreen('paticon.png')
    number = 0
    for i in paticons:
        number += 1
        if number > 1:
            raise Exception("Multiple Patients Found")
    if number == 0:
        raise Exception("No patients found")
    ag.click()

    section('Get member info')
    
    #Hide alerts
    sleep(0.9)
    ag.write('\n')
    sleep(0.25)

    #Open form
    ag.moveTo(1881,513)
    ag.click()
    sleep(0.1)
    ag.moveTo(110,452)
    sleep(0.1)
    ag.moveTo(54,452)
    ag.click()

    #Attach document
    sleep(0.1)
    ag.moveTo(911,1047)
    ag.click()
    sleep(2)
    ag.moveTo(321,206)
    ag.click()
    sleep(0.8)
    ag.write('\n')
    sleep(0.5)


    #Add source + description + date
    ag.moveTo(918,798)
    ag.click()
    ag.write('Membre - Coral App')
    ag.press('tab')
    ag.write(formname+' - '+month[0:3]+' '+str(day)+' ' + str(year))
    ag.press('tab')
    ag.write('Sunday, '+str(day)+' '+month+' '+str(year))
    sleep(0.2)

    #Add providers
    ag.moveTo(894,633)
    ag.click()
    if nurse:
        ag.write(nurse)
        sleep(0.7)
        ag.write('\n')
    if prescriber:
        ag.write(prescriber)
        sleep(0.7)
        ag.write('\n')
    ag.moveTo(1610,573)
    ag.click()

    section('Get document')
    sleep(0.2)
    ag.click(1790,1101) #accept
    sleep(0.8)
    ag.click(1700,1101) #cancel
    sleep(0.2)
    ag.click(1308, 399) #refresh
    pyperclip.copy('')
    print('Done in',round(time.time()-starttime,5),'seconds.')
    print()
    #for i in times:
    #    print(i[0],round(i[1],2))
    #times = []
    #print('Total time slept + shotted:',round(sleeptally,2))
    print()
while True:
    run()
