from time import sleep
import pyautogui as ag

auto = False
survey = None

def longanswer(lines, i, checkauto = True):
    global auto, isfrench
    noanswer = ['No answer', 'Pas de réponse'][int(isfrench)]
    savedauto = auto
    auto = auto and checkauto
    if lines[i] == 'A: '+noanswer:
        return False
    while i < len(lines) and not (lines[i][0:3] == 'Q: ' or (lines[i][0:3] == '' and lines[i+1] == lines[i+1].upper())):
        if lines[i][0:3] == 'A: ':
            setbodytext(lines[i][3:])
        else:
            setbodytext(lines[i])
        i+=1
    auto = savedauto
    return i-1

def answered(lines, i):
    noanswer = ['No answer', 'Pas de réponse'][int(isfrench)]
    return lines[i][3:] != noanswer 
def settitletext(line):
    print(line)
    if auto:
        sleep(0.35)
        ag.click(893,558)
        ag.sleep(0.25)
        ag.write(line)
        ag.sleep(0.25)
        ag.press('tab')
        ag.press('tab')
        sleep(0.25)
           

def setbodytext(line, end='\n'):
    print(line, end=end)
    if auto:
        ag.write(line)
        if end == '\n':
            ag.press('enter')
        else:
            ag.write(end)

def endsection():
    print()
    print()
    if auto:
        ag.sleep(0.4)
        ag.click(1805,1099)

def whsq(lines):
    global auto, isfrench
    noanswer = ['No answer', 'Pas de réponse'][int(isfrench)]
    auto = 'y' in input("Would you like to automate this survey? ") 

    
    if not auto:
        print('\nCopy each of the following into "Active problems", with the category as the title\n\n')

    if auto:
        sleep(1)
        print('Okay. Please open kardex, and create a new "Active Problem". You have 2 seconds')
        sleep(1)
        print('1 second')
        sleep(1)

        
    headings = ['VASOMOTOR SYMPTOMS',
                'CARDIOVASCULAR SYMPTOMS',
                'NEUROLOGICAL SYMPTOMS',
                'SLEEP DISTURBANCES',
                'GYNECOLOGICAL AND SEXUAL HEALTH SYMPTOMS',
                'URINARY SYMPTOMS',
                'GASTROINTESTINAL SYMPTOMS',
                'MUSCULOSKELETAL SYMPTOMS',
                'SKIN AND HAIR SYMPTOMS',
                'EMOTIONAL AND PSYCHOLOGICAL SYMPTOMS']
    settitletext('''Menopause symptoms scale''')
    setbodytext('''1) not at all
2) a little
3) moderately
4) often
5) extremely''')
    endsection()
    scale = ['','Not at all','A little', 'Moderately','Often','Extremely']

    for heading in headings:
        hind = lines.index(heading)
        currentq = hind+1
        hastitled = False
        while lines[currentq]:
            if lines[currentq+1] != 'A: Not at all':
                if lines[currentq+1] =='butterflies in my chest or stomach':
                    lines[currentq+1] = 'Q: Heart palpitations or a sensation of butterflies in my chest or stomach'
                    currentq+=1
                    continue

                if not hastitled:
                    hastitled = True
                    settitletext(heading.title())
                text = lines[currentq][3:] +' '
                if lines[currentq+1] =='butterflies in my chest or stomach':
                    text += lines[currentq+1]
                    currentq+=1
                if lines[currentq+1][3:] in scale:
                    text += str(scale.index(lines[currentq+1][3:]))+'/5'
                setbodytext(text)
            currentq += 2
        if hastitled:
            endsection()
                    

    iol = lines.index('IMPACT ON LIFE')
    settitletext('\nImpact on Life')
    setbodytext('How would you rate the impact of your menopause symptoms on your daily activities and quality of life? ' \
    +str(['','Minimal','Minor','Moderate','Significant','Severe'].index(lines[iol+2][3:]))+'/5')
    setbodytext('''1)Minimal
2)Minor
3)Moderate
4)Significant
5)Severe''')
    endsection()

def mhq(lines):
    global auto, isfrench
    noanswer = ['No answer', 'Pas de réponse'][int(isfrench)]
    auto = 'y' in input("Would you like to automate this survey? ") 

    print('\nFile under Medical History, with condition as the title')
    if auto:
        sleep(1)
        print('Okay. Please open kardex, and create a new "Medical history". You have 2 seconds')
        sleep(1)
        print('1 second')
        sleep(1)
    headings = ['CARDIOVASCULAR HISTORY',
                'HEMATOLOGICAL MEDICAL HISTORY',
                'NEUROLOGICAL MEDICAL HISTORY',
                'GASTROINTESTINAL MEDICAL HISTORY',
                'MUSCULOSKELETAL MEDICAL HISTORY',
                'UROGYNECOLOGICAL MEDICAL HISTORY',
                'METABOLIC MEDICAL HISTORY',
                'RESPIRATORY MEDICAL HISTORY',
                'INTEGUMENTARY MEDICAL HISTORY',
                'MENTAL HEALTH MEDICAL HISTORY',
                'OTHER MEDICAL DIAGNOSES',
                'SURGICAL HISTORY',
                'LAB TEST HISTORY'
                ]
    notes = {'MENTAL HEALTH MEDICAL HISTORY':'file under "Psychiatric History"'}
    clicks = {'MENTAL HEALTH MEDICAL HISTORY':lambda :ag.click(666,948)}

    for heading in headings:
        hind = lines.index(heading)
        currentq = hind+1
        hastitled = False
        finished = []
        true = ['True','Vrai'][int(isfrench)]
        false = ['False','Faux'][int(isfrench)]
        noanswer = ['No answer', 'Pas de réponse'][int(isfrench)]
        while lines[currentq]:
            if lines[currentq+1][3:] not in [false, noanswer] and currentq not in finished:
                if not hastitled:
                    hastitled= True
                    print('\n\n')
                    if heading in notes:
                        print('Note- '+notes[heading])
                    if auto and heading == 'SURGICAL HISTORY':
                        print('Please enter manually:')
                    print(heading.title()+':')
                if lines[currentq+1][3:] == true:
                    print(lines[currentq][3:])
                    if auto and heading != 'SURGICAL HISTORY':
                        if heading in clicks:
                            clicks[heading]()
                        ag.click(837,557)
                        sleep(0.1)
                        ag.write(lines[currentq][3:])
                        sleep(0.3)
                        ag.click(1800, 1103)
                        sleep(0.4)
                    

                else:
                    if auto:
                        print("Please enter the following manually. (enter to continue)")
                    longanswer(lines, currentq+1, False)
                    if auto:
                        input()
                    break
            currentq += 2
            if currentq >= len(lines):
                break
    try:
        cncr = lines.index('Q: Do you currently have an active cancer diagnosis, or have you previously been diagnosed with cancer? ')
        if lines[cncr+1][3:] not in [noanswer,'I have never been diagnosed with cancer']:
            print('\n\nCancer')
            print(lines[cncr+1][3:])
    except:
        pass
    auto = False
    famindex = lines.index('FAMILY MEDICAL HISTORY')
    print('\n\nFamily history:')
    cfm = lines.index('Q: Please list any close family members (mother, father, brother, or sister) who have been diagnosed by a doctor with any of the conditions mentioned previously, including those that occurred during pregnancy, and include past or present diagnoses.')
    longanswer(lines, cfm+1)
    mexp = lines.index('Q: How would you describe your mother\'s experience with menopause?')
    print('\nHow would you describe your mother\'s experience with menopause?')
    print(lines[mexp+1][3:])
    if lines[mexp+3][3:] != noanswer:
        longanswer(lines,mexp+3)

    repindex = lines.index('REPRODUCTIVE HISTORY')
    print('\n\nReproductive History:')
    if answered(lines, repindex+2):
        try:
            print(int(lines[repindex+2][3:]),'pregnancies')
        except:
            repindex = longanswer(lines,repindex+2)-2
        print(['Has no children\n','Has '][int('True' == (lines[repindex+4][3:]))],end='')
    if 'True' == (lines[repindex+4][3:]):
        try:
            print(int(lines[repindex+6][3:]),' children')
        except:
            print('children:',lines[repindex+6][3:])
    elif answered(lines,repindex+6):
        print('children:',lines[repindex+6][3:])
    print('\n'+lines[repindex+7][3:])
    print(lines[repindex+8][3:])
    longanswer(lines, repindex+10)

    
def ghq(lines):
    global isfrench
    noanswer = ['No answer', 'Pas de réponse'][int(isfrench)]

    print('\nFile under Obstetrical History')
    print('\nGynecologic History')
    status = lines[5].split(': ')[1]
    statdict = {'Pre-menopause':'still experiencing regular menstrual cycles, no changes noticed',
                'Perimenopause':'noticed irregular menstrual cycles characterized by changes in flow, frequency, or duration',
                'Menopause':'has not had a menstrual period for at least 12 consecutive months, signifying the end of your reproductive years',
                'Post-menopause':'have not had a menstrual period for MORE than 12 consecutive months',
                'I\'m not sure':'I have either an intrauterine device (IUD) with hormones or I\'m taking continuous hormonal contraception, both of which prevent me from having a period'}
    print('Current menstrual status: '+status+': '+statdict[status])
    if lines[7][3:] not in ['Not applicable','Other']:
        print('Onset of menopause:',end=' ')
        print(lines[7][3:])
    elif lines[7][3:]  == 'Other':
        print('Onset of menopause: Other:')
        print(lines[9][3:])
    print('Age at menarche:',lines[11][3:])
    if lines[13][3:] == 'True':
        print('Periods usually regular')
    else:
        print('Periods usually irregular')
    presdict = {'Yes':' ','No':' not ','Not sure':' not known if '}
    print('Uterus'+presdict[lines[15][3:]]+'present') 
    print('Both ovaries'+presdict[lines[17][3:]]+'present') 
    print('Cervix'+presdict[lines[19][3:]]+'present')
    if lines[21][3:] != noanswer:
        try:
            print('Last period at age:',int(lines[21][3:]))
        except:
            print('Notes on last period age:',lines[21][3:])
    print('Breast self-examinations:',lines[23][3:])
    desdict = {'No, my mother did not take DES during her pregnancy with me':'No',
'Yes, my mother took DES during her pregnancy with me':'Yes',
'I am not sure':'Not sure',
'My mother was not pregnant with me during the that time':'No'}
    if answered(lines, 25):
        print('DES exposure in utero:',desdict[lines[25][3:]])
    if lines[27][3:] =='No, I do not use douching':
        print('Douching: no')
    else:
        print('Douching:',lines[27][3:])
    if lines[29][3:] != noanswer:
        print(lines[29][3:])


        
    cmi = lines.index('CURRENT MENSTRUAL INFORMATION')
    print('\n\nCurrent Menstrual Status')
    print('Cycle frequency: '+lines[cmi+2][3:])
    print('Painful periods: ',end='')
    if lines[cmi+4][3:] == 'I am unsure/It’s variable each month':
        print('variable')
    else:
        print(lines[cmi+4][3:])
    print('Spotting/bleeding between periods:',end=' ')
    spotdict = {'No, I do not have any spotting or bleeding between periods':'no',
                'Yes, occasionally I have light spotting':'light spotting',
                'Yes, I have frequent spotting between periods':'frequent spotting',
                'Yes, I have heavy bleeding between periods':'heavy bleeding',
                'I am unsure or it varies each month':'varies',
                noanswer:noanswer}
    print(spotdict[lines[cmi+6][3:]])
    print('Cycle regularity: ',end='')
    changedict = {'No, my periods have remained regular':'no recent changes',
'Yes, they have become more frequent':'they have become more frequent',
'Yes, they have become less frequent':'they have become less frequent',
'Yes, I’ve missed a period recently':'missed a period recently',
'I am unsure about the changes in my cycle':'unsure about the changes in cycle',
                  noanswer:noanswer}
    print(changedict[lines[cmi+8][3:]])
    print('Menstrual heaviness: ',end='')
    heavydict = {'No, my periods have not changed in heaviness':'no change',
'Yes, they have become slightly heavier':'they have become slightly heavier',
'Yes, they have become noticeably heavier':'they have become noticeably heavier',
'Yes, they are now very heavy and concerning':'they are now very heavy and concerning',
'I’m unsure about the change in heaviness':'unsure about the change in heaviness',
noanswer:noanswer}
    print(heavydict[lines[cmi+10][3:]])
    print('Concerns about cycle:',end=' ')
    cdict = {'No, I have no concerns about my menstrual cycle':'none',
'Yes, I have minor concerns but nothing serious':'minor',
'Yes, I have some significant issues I’d like to discuss':'significant',
"Yes, I’m experiencing severe problems affecting my daily life I’d like to discuss":'severe',
'I am unsure if what I’m experiencing is a problem':'unsure',
             noanswer:noanswer}
    print(cdict[lines[cmi+12][3:]])
        
    longanswer(lines,cmi+14)
    pms = lines.index('Q: Do you experience any issues related to premenstrual syndrome (PMS), such as mood swings, bloating, or headaches, in the days leading up to your period?')

    if lines[pms+1] != 'No, I do not experience any PMS symptoms':
        print('PMS: ',end='')
        if lines[pms+1][3:][0:3] == 'Yes':
            print(lines[pms+1][3:][5:])
        else:
            print(lines[pms+1][3:])
    if answered(lines,pms+3):
        print('Typical PMS symptoms: ',end='')
        longanswer(lines,pms+3)
    eff = lines.index('Q: How would you rate the effectiveness of the medications, supplements, or remedies you use in alleviating your PMS symptoms?')
    if lines[eff+1][3:] != "Not applicable":
        print('Management effectiveness:',lines[eff+1][3:])
    

def msmq(lines):
    global isfrench
    noanswer = ['No answer', 'Pas de réponse'][int(isfrench)]
    cmns = 3
    if lines[cmns+2][3:] == 'True':
        print('Currently taking HRT for menopause')
    if 'True' ==(lines[cmns+4][3:]) or answered(lines, cmns+6):
        print('Currently taking prescribed medication (related or non-related to menopause)')
    a = longanswer(lines,cmns+6)
    if a:
        cmns = a-6
    if 'True' == (lines[cmns+8][3:]) or answered(lines, cmns+10):
        print('Currently taking supplements (related or non-related to menopause)')
    a = longanswer(lines,cmns+10)#supplements
    if a:
        cmns = a-10
    if lines[cmns+12][3:] != 'No side effects experienced' and lines[cmns+12][3:] != noanswer:
        if lines[cmns+12][3:] == 'Unsure/need to discuss with a healthcare provider':
            print('Side effects:',end=' ')
        print(lines[cmns+12][3:])
    a = longanswer(lines,cmns+14)#side effects
    if a:
        cmns = a-14
    if lines[cmns+16][3:] != noanswer and lines[cmns+16][3:] != 'No, I have not discontinued anything recently' :
        print(lines[cmns+16][3:])
    print(lines[cmns+17][3:])#healthcare provider
    print(lines[cmns+18][3:])
    try:
        bcp = lines.index('Q: I am currently on a birth control pill.')
        if answered(lines,bcp+3):
            print("Birth control:", end = ' ')
            longanswer(lines,bcp+3)
        elif lines[bcp+1][3:] == 'True':
            print('Takes birth control')
            
        iud = lines.index('Q: I currently have an IUD (intra-uterine device).')
        if answered(lines,iud+3):
            print("IUD:", end = ' ')
            longanswer(lines,iud+3)
        elif lines[bcp+1][3:] == 'True':
            print('Has an IUD')
    except ValueError:
        print('\n\nForm filled out before Nov 2025\n\n')
    
    hrt = lines.index('CURRENT HORMONE THERAPY REVIEW')
    if lines[hrt+2][3:] != noanswer or answered(lines,hrt+4):
        print("\n\nHRT Review:")
        critical = [hrt+1,hrt+5,hrt+7,hrt+9,hrt+17,hrt+19,hrt+21]
        index = hrt+1
        while lines[index] != '':
            if lines[index+1][3:] != noanswer or index in critical:
                if index == hrt + 1 and lines[index+1][3:] != 'Other':
                    lines[index+1] = ':'.join(lines[index+1].split(':')[:-1])
                print(lines[index][3:])
                print(lines[index+1][3:])
            index += 2
    else:
        index = hrt+1
        while lines[index] != '':
            if answered(lines,index+1) and lines[index+1][3:] != 'Poor':
                print(lines[index][3:])
                print(lines[index+1][3:])
            index += 2
    alt = lines.index('ALTERNATIVE TREATMENTS TO SYMPTOM MANAGEMENT')

    print('\n\nAlternative treatments to symptom management')
    if answered(lines,alt+2):
        print('Has tried:',end=' ')
        print(lines[alt+2][3:])
        a = longanswer(lines,alt+4)
        if a:
            alt = a-4
    if answered(lines,alt+6):
        print('Primary symptoms relief sought for:',end=' ')
        a = longanswer(lines,alt+6)
        if a:
            alt = a-6
        else:
            print('xxxxx')
    if answered(lines, alt+8):
        print('Treatments found effective:',end=' ')
        a = longanswer(lines,alt+8)
        if a:
            alt = a-8
        else:
            print('')
    if answered(lines,alt+2) or lines[alt+10][3:] != 'Poor':
        print('Effectiveness: ',lines[alt+10][3:])
    
    newapp = lines.index('INTEREST IN NEW APPROACHES')
    print('\n\nNew approaches')
    print('Open to exploring alternative treatments:',lines[newapp+2][3:])
    text = lines[newapp+4][3:].replace(': strength training, cardiovascular training, etc','').replace('Other','').replace(noanswer,'')
    if not answered(lines, newapp+4):
        text = 'Nothing'
    print('Interested in:',text,end='')
    if answered(lines, newapp+6):
        newapp = longanswer(lines,newapp+6)-6
    else:
        print()
    sciback = lines[newapp+8][3:]
    if lines[newapp+10][3:] != noanswer:
        newapp = longanswer(lines,newapp+10)-10
    if sciback != noanswer:
        print('Importance of scientific research backing:',sciback)
    if lines[newapp+12][3:] != noanswer:
        print('Additional support or resources would you find helpful:',end=' ')
        longanswer(lines, newapp+12)

def lhq(lines):
    global auto
    noanswer = ['No answer', 'Pas de réponse'][int(isfrench)]
    auto = 'y' in input("Would you like to automate this survey? ") 

    
    if not auto:
        print('\nCopy each of the following into "Social Habits", with the category as the title\n\n')

    if auto:
        sleep(1)
        print('Okay. Please open kardex, and create a new "Social Habit". You have 2 seconds')
        sleep(1)
        print('1 second')
        sleep(1)

    
    sah = 3
    settitletext('Self-Assessment of Health')
    l1 = ['Very poor','Poor','Fair','Good','Excellent'].index(lines[sah+2][3:])
    l2 = ['Never','Rarely','Sometimes','Often','Always'].index(lines[sah+4][3:])
    setbodytext(f'''How would you rate your health? {l1+1}/5
1)Very poor
2)Poor
3)Fair
4)Good
5)Excellent

How often do you feel fatigued or low on energy? {l2+1}/5
1)Never
2)Rarely
3)Sometimes
4)Often
5)Always''')
    endsection()
    slp = lines.index('SLEEP')
    settitletext('Sleep')
    setbodytext(lines[slp+2][3:]+' hours of sleep per night')
    setbodytext(lines[slp+4][3:]+' when wake up')
    cons = lines[slp+8][3:].split('(')
    setbodytext(cons[0] + 'sleep schedule ('+cons[1])
    l3 = ['Very poor','Poor','Average','Good','Excellent'].index(lines[slp+6][3:])
    setbodytext(f'''How would you rate the overall quality of your sleep on a scale from 1 to 5? {l3+1}/5
1)Very poor
2)Poor
3)Average
4)Good
5)Excellent''')
    endsection()

    mwb = lines.index('MENTAL WELLBEING')
    settitletext('Mental Wellbeing')
    setbodytext('Mental health: '+lines[mwb+2][3:])
    setbodytext('Mood swings: '+lines[mwb+4][3:])
    if lines[mwb+6][3:] == 'True':
        setbodytext("I have noticed shifts in my self-confidence or sense of self-worth")
    setbodytext('Stress: '+lines[mwb+8][3:])
    setbodytext('Stress management: '+lines[mwb+10][3:])
    setbodytext('Concentration: '+lines[mwb+12][3:].replace('same','same as before').replace('before','a few months ago'))
    setbodytext('Emotional support: '+lines[mwb+14][3:])
    endsection()
    
    pa = lines.index('PHYSICAL ACTIVITY')
    settitletext('Physical Activity')
    setbodytext('Frequency: '+lines[pa+2][3:])
    setbodytext('Duration: '+lines[pa+4][3:])
    setbodytext('Types: '+lines[pa+6][3:].replace('Other',''),end='')
    if answered(lines, pa+8):
        setbodytext(' ',end='')
        longanswer(lines, pa+8)
    else:
        setbodytext('')
    if answered(lines,pa+14):
        setbodytext('Limitation: ',end='')
        longanswer(lines,pa+14)
    elif lines[pa+12][3:] == 'True':
        setbodytext('Has a limitation')

    l4 = ['Not at all','Slightly','Somewhat','Mostly','Very'].index(lines[pa+10][3:])
    setbodytext(f'''How satisfied are you with the amount of physical activity you currently engage in? {l4+1}/5
1)Not at all
2)Slightly
3)Somewhat
4)Mostly
5)Very''')

    endsection()
    
    nutr = lines.index('NUTRITION')
    
    settitletext('Nutrition')
    setbodytext('Diet: '+lines[nutr+2][3:].replace('I don\t follow a specific diet','No specific'))
    setbodytext('Meals: '+lines[nutr+4][3:])
    setbodytext('Fruits/vegetables: '+lines[nutr+6][3:])
    setbodytext('Water: '+lines[nutr+8][3:]+'/day')
    setbodytext('Hunger cues: '+lines[nutr+10][3:])
    setbodytext('Satisfaction with eating habits: '+lines[nutr+12][3:])
    endsection()
    
    such = lines.index('SUBSTANCE USE AND CONSUMPTION HABITS')
    settitletext('Caffeine ('+lines[such+2][3:].replace(' a day','')+'/day)')
    endsection()
    
    settitletext('Alcohol - '+lines[such+4][3:])
    endsection()
    smokes = {'No, never':'Non-Smoker','I quit':'Non-smoker - quit',
              'Yes, regularly':'Tobacco (regular)','Yes, occasionally':'Tobacco (Occasionally)',
              'Prefer not to say':'', noanswer:''}[lines[such+6][3:]]
    if smokes:
        settitletext(smokes)
        endsection()
        
print('Copy paste a form here, then type xxx for english or fff for french and hit enter to see copy-pasteable version')
while True:
    lines = []
    while True:
        isfrench = False
        lines.append(input())
        if len(lines) == 1 and not lines[-1]:
            lines.pop()
            continue
        if lines[-1][0:2] == 'xx':
            lines.pop()
            isfrench = False
            break
        elif lines[-1][0:2] == 'ff':
            lines.pop()
            isfrench = True
            break
    #print(lines)
    auto=False
    if not lines:
        print('IMPROPER COPY PASTE')
        continue
    elif lines[0] == 'WOMEN’S HEALTH SYMPTOMS QUESTIONNAIRE':
        print('Decoding WHSQ...')
        survey = 'whsq'
        whsq(lines)
    elif lines[0] == 'MEDICAL HISTORY QUESTIONNAIRE':
        print('Decoding MHQ...')
        survey = 'mhq'
        mhq(lines)
    elif lines[0] == 'GYNECOLOGICAL HISTORY QUESTIONNAIRE':
        print('Decoding GHQ...')
        survet = 'ghq'
        ghq(lines)
    elif lines[0] == 'MEDICATION AND SYMPTOM MANAGEMENT QUESTIONNAIRE':
        print('Decoding MSMQ...')
        survey = 'msmq'
        msmq(lines)
    elif lines[0] == 'LIFESTYLE AND HABITS QUESTIONNAIRE':
        print('Decoding LHQ...')
        survey = 'lhq'
        lhq(lines)
    else:
        print('IMPROPER COPY PASTE')







