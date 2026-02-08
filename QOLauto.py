import pyautogui as ag
import pytesseract as pt
from time import time, sleep
from dateutil.parser import parserinfo
from mss import mss
import numpy as np
import matplotlib.pyplot as plt
import pyperclip

pt.pytesseract.tesseract_cmd = r'C:\Users\nicho\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
ag.PAUSE = 0.01
def screenshot(bounds, show = False):
    shot = mss()
    arr = np.asarray(shot.grab(bounds))
    if show:
        plt.imshow(arr)
        plt.show()
    text = pt.image_to_string(arr,config='--psm 7')
    if show:
        print(text.strip())
    return text
    

print('Ensure:\n'+
      'Printer mode is set to "save to PDF"')
print('The first tab is the EMR, logged in, and airtable is the second')
print('File explorer defaults to the downloads page')
print('You\'re on airtable, with the full screen open, and show hidden fields off')
def run():
    print("\n\nWill take over immediately.")
    input('Ready? ')
    print('Will take over computer in 2 seconds, please make sure Airtable entry is open')

    starttime = time()

    
    namebounds = {'top':580,'left':540,'width':500,'height':50}
    name = screenshot(namebounds).strip().replace('-',' ')
    letters = 'QWERTYUIOPASDFGHJKLZXCVBNMÀÁÂÃÄÅĀĂĄǍȀȂȦẠẢẤẦẨẪẬẮẰẲẴẶÆḂḄḆÇĆĈĊČĎĐḊḌḎḐḒÈÉÊËĒĔĖĘĚȄȆẸẺẼẾỀỂỄỆḞĜĞĠĢǦǴĤḢḤḦḨḪÌÍÎÏĨĪĬĮIǏȈȊỊỈĴJ̌ĶḰḲḴĹĻĽĿŁḶḸḺḼḾṀṂÑŃŅŇṄṆṈṊÒÓÔÕÖŌŎŐǑȌȎȮỌỎỐỒỔỖỘỚỜỞỠỢŒṔṖŔŖŘȐȒṘṚṜṞŚŜŞŠṢṠṤṦṨSSŤŦṬṮȚṰÙÚÛÜŨŪŬŮŰŲǓȔȖỤỦỨỪỬỮỰṲṶṸṺẀẂŴẄẆẈẊẌÝŸŶȲẎỴỶY̊ỲŹŻŽẐẒẔ'

    acronym = ''
    maybestake = ''
    for i in name.split(' '):
        if len(i) > 0 and i[0] in letters:
            if i == name.split(' ')[-1]:
                if not ((len(i) == 2 and 'aeiou' not in i) or (len(i) == 1)):
                    acronym += i[0]
            else:
                acronym += i[0]
        else:
            maybestake = i
    print(name, acronym)

    
    namebounds = {'top':410,'left':340,'width':500,'height':50}
    filename = screenshot(namebounds).strip().replace('-',' ')
    allowedchars = 'QOL #1234567890'
    newname = ''
    for i in filename:
        if i in allowedchars:
            newname += i
    print(filename,'->',newname)

    ag.moveTo(500,500)
    
    #Scroll to bottom
    for i in range(5):
        ag.scroll(-2000)
    
    datebounds = {'top':383,'left':572,'width':150,'height':50}
    sleep(0.2)
    datestring = screenshot(datebounds).strip()
    hasdate = True
    if len(datestring.split('-')) == 3:
        year,month,day = map(int,datestring.split('-'))
        month = parserinfo.MONTHS[month-1][-1]
        print(year, month, day)
    else:
        hasdate = False
        print('---NO DATE FOUND---')

    #Show hidden fields + open member link
    ag.moveTo(797,1009)
    sleep(0.1)
    ag.click()
    sleep(0.1)
    ag.scroll(-2000)
    ag.moveTo(780,864)
    sleep(0.2)
    ag.click()

    sleep(1.8)
    #Get nurse + prescriber

    sponsor = screenshot({'top':435,'left':552,'width':400,'height':50})
    if "sponsored" in sponsor.lower():
        boundschange = 30
        print("Is sponsored!")
    else:
        boundschange = 0
    
    nurse = screenshot({'top':710+boundschange,'left':835,'width':250,'height':50})

    nurses = ['lefebvre','jessica', 'linda', 'proulx']
    for i in nurses:
        if i in nurse.lower():
            nurse = i
            break
    else:
        print('Nurse',nurse,'not known (may be none)')
        nurse = None

    prescriber = screenshot({'top':710+boundschange,'left':1323,'width':300,'height':50})

    prescribers = ['ariane','vicky','catarina','mcgraw']
    for i in prescribers:
        if i in prescriber.lower():
            prescriber = i
            break
    else:
        print('Prescriber',prescriber,'not known (may be none)')
        prescriber = None

    print(nurse, prescriber)
    ag.hotkey('ctrl','w')
    
    #Open document
    ag.moveTo(738,647)
    sleep(0.2)
    ag.click()
    sleep(0.5)
    ag.click()
    ag.hotkey('ctrl','p')

    #Save
    sleep(1.6)
    ag.hotkey('ctrl','p')
    sleep(1)
    ag.write('\n')
    sleep(0.75)
    ag.write('\n')
    sleep(0.25)
    ag.write('\n')
    sleep(0.5)
    ag.hotkey('ctrl','w')
    sleep(0.25)
    ag.press('esc')
    
    #Open EMR calendar view
    sleep(0.25)
    ag.hotkey('ctrl','1')
    ag.moveTo(115,178)
    sleep(1)
    ag.click()
    sleep(0.5)

    #Find the member
    ag.moveTo(126,251)
    ag.click(clicks=3)
    ag.press('backspace')
    acroindex = 0
    for i in range(len(name.split(' '))):
        #Copy paste to allow special characters
        if not name.split(' ')[i] or acroindex >= len(acronym):
            continue
        if name.split(' ')[i][0].upper() == acronym[acroindex]:
            towrite = name.split(' ')[i]+' '
            if "'" in towrite:
                towrite = towrite.split("'")[0]
            acroindex += 1
        else:
            continue
        pyperclip.copy(towrite)
        ag.hotkey('ctrl','v')
        sleep(0.05)

    if 'Nathalie Gagnon' in name:
        print("WARNING: There are two members with this name. Please enter manually.")
        return

    
    ag.moveTo(135,366)
    sleep(0.9)
    ag.click()
    sleep(1.1)

    #Open form
    ag.write('\n')
    sleep(0.25)
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
    sleep(0.75)
    ag.moveTo(321,206)
    ag.click()
    sleep(0.4)
    ag.write('\n')
    sleep(0.5)


    #Add source + description + date
    ag.moveTo(918,798)
    ag.click()
    ag.hotkey('shift','tab')
    ag.write('ooo')
    ag.press('tab')
    ag.write('Membre - Coral App')
    ag.press('tab')
    ag.write(newname)
    ag.press('tab')
    if hasdate:
        ag.write('Sunday, '+str(day)+' '+month+' '+str(year))
    sleep(0.25)

    
    #Add providers
    ag.moveTo(894,633)
    ag.click()
    if nurse:
        ag.write(nurse)
        sleep(0.5)
        ag.write('\n')
    if prescriber:
        ag.write(prescriber)
        sleep(0.5)
        ag.write('\n')
    ag.moveTo(1610,573)
    ag.click()

    print('Done in',round(time()-starttime,5),'seconds.')
while True:
    run()
