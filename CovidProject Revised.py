import MySQLdb as MS
import pickle
import csv
import decimal
import matplotlib.pyplot as plt
import numpy as np
import random as rd
from datetime import datetime

def installer():
     global ans
     while True:
          try:
               print('Welcome to Installation Wizard')
               dbname=input('Enter Database Name in which you would like to install the database : ')
               while dbname.isalnum()==False:
                    dbname=input('Please Enter a Database Name which contains only Alphanumeric Values :')
               p=input('Enter the Password used to login into MySQL : ')
               db=MS.connect(host='localhost',user='root',passwd=p)
               c=db.cursor()
               dbname=dbname.lower() 
               c.execute('show databases')
               dblist=c.fetchall()
               if (dbname,) in dblist:
                    while True:
                         ans=1
                         x=input('Database exists would you like to reinstall over it. Doing so will erase all data in that database[Y/N] : ')
                         if x in ['Y','y']:
                              c.execute('Use '+dbname)
                              c.execute('drop database '+dbname)
                              c.execute('create database '+dbname)
                              c.execute('Use '+dbname)
                              db.commit()
                              break
                         elif x in ['N','n']:
                              print('Process Terminated')
                              c.execute('use '+dbname)
                              ans=0
                              break
                         else:
                              print('invalid input')
                    break
               else:
                    c.execute('create database '+dbname)
                    c.execute('Use '+dbname)
                    break
          except MS._exceptions.OperationalError:
               print('WRONG/INVALID PASSWORD !')
     print('Connection Success')
     return c,db,dbname

def tablereset():
     print('\nPlease wait while we are adding the tables...')
     c.execute('Use '+dbname)
     try:
          c.execute('create table hosp_rec (HOSP_ID DECIMAL(5) PRIMARY KEY,DISTRICT VARCHAR(25),HOSPITAL_NAME VARCHAR(30) UNIQUE,TOTAL_BEDS DECIMAL(4),AVAILABLE_BEDS DECIMAL(4),PINCODE DECIMAL(6))')
     except:
          c.execute('drop table hosp_rec')
          c.execute('create table hosp_rec (HOSP_ID DECIMAL(5) PRIMARY KEY,DISTRICT VARCHAR(25),HOSPITAL_NAME VARCHAR(30) UNIQUE,TOTAL_BEDS DECIMAL(4),AVAILABLE_BEDS DECIMAL(4),PINCODE DECIMAL(6))')
     hospids,hnames=[],['MAX SUPER SPECIALITY','LOK NAYAK','AIIMS','GTB HOSPITAL','SARDAR PATEL ARMY','RAJIV GANDHI SUPER SPECIALITY','BASE DELHI CANTT.','SAFDURJUNG HOSPITAL','H.A.H.C','BURARI HOSPITAL','ST.STEPHENS TIS HAZARI','RAM MANOHAR LOHIA','INDRAPRASTHA APOLLO','BLKSSH PUSA ROAD','SATYAWATI HARISHCHANDRA','AMBEDAKAR NAGAR','DEEN DAYAL UPADHYAY','HOLY FAMILY OKHLA','MAHARAJA AGRASEN PUNJABI BAGH','FORTIS VASANT KUNJ']
     districts={1:'NEW DELHI',2:'CENTRAL DELHI',3:'EAST DELHI',4:'NORTH DELHI',5:'NORTH-EAST DELHI',6:'NORTH-WEST DELHI',7:'SHAHDARA',8:'SOUTH DELHI',9:'SOUTH-EAST DELHI',10:'SOUTH-WEST DELHI',11:'WEST DELHI'}
     l=[]
     l.append(['0','NOT APPLICABLE','NO HOSPITALIZATION','0','0','0'])
     for i in range(20):
          hosp_id=rd.randint(10000,99999)
          while hosp_id in hospids:
               hosp_id=rd.randint(10000,99999)
          dist=districts[rd.randint(1,11)]
          hname=hnames.pop(rd.randrange(0,len(hnames),1))
          abeds=tbeds=rd.randint(50,80)
          pincode=rd.randint(110001,110099)
          j=[hosp_id,dist,hname,tbeds,abeds,pincode]
          for i in range(len(j)):
               j[i]=str(j[i]).upper()
          l.append(j)
     listtosql(l,'hosp_rec')
     l=record(300)
     try:
          c.execute('create table patient_rec (AADHAR_NO decimal(12) primary key, PATIENT_NAME char(25)not null, AGE decimal(3) not null,GENDER char(1) not null,HOSP_ID decimal(5) not null,GUA\
RANTOR_NAME char(25) not null,G_REL char(15) not null,TESTED_ON date not null, STATUS char(8) not null,DECEASED_ON date)')
     except:
          c.execute('drop table patient_rec')
          c.execute('create table patient_rec (AADHAR_NO decimal(12) primary key, PATIENT_NAME char(25)not null, AGE decimal(3) not null,GENDER char(1) not null,HOSP_ID decimal(5) not null,GUA\
RANTOR_NAME char(25) not null,G_REL char(15) not null,TESTED_ON date not null, STATUS char(8) not null,DECEASED_ON date)')
     for L in l:
          sql='insert into patient_rec values ("'+L[0]+'","'+L[1]+'","'+L[2]+'","'+L[3]+'","'+L[4]+'","'+L[5]+'","'+L[6]+'","'+L[7]+'","'+L[8]+'",'+('"'+L[9]+'"',L[9])[L[9].upper()=='NULL']+')'     
          c.execute(sql)
     db.commit()
     print('Tables Added')

def record(n):
     REC=[]
     def read(f,j=0):
          F=open(f,'r')
          r=csv.reader(F)
          R=[]
          for i in r:
               R.append(i[j])
          F.close()
          return R
     def name():
          rfn=rd.randrange(0,len(FN),1)
          rsn=rd.randrange(0,len(SN),1)
          rgen=GEN[rfn]
          name=FN[rfn]+' '+SN[rsn]
          return name,rgen
     def randdate(my=Dates):
           x=rd.randrange(0,len(my),1)
           dd=str(rd.randint(1,28))
           date=my[x]+'-'+dd
           return date,x
     FN=read('PFN.csv')
     GEN=read('PFN.csv',1)
     SN=read('PSN.csv')
     for i in range(n):
          usedadr=[]
          adrno=rd.randint(200000000000,999999999999)
          while adrno in usedadr:
               adrno=rd.randint(200000000000,999999999999)
          usedadr.append(adrno)
          pname,gender=name()
          r=c.execute('select hosp_id from hosp_rec')
          r1=c.fetchall()
          r2=[]
          for i in range(len(r1)):
               r2.append(r1[i][0])
               
          hosp_id=r2[rd.randrange(0,len(r2),1)]
          tpo,x=randdate()
          rec,infected,dead=['REC_HQUA','REC_HOSP','REC_HOSP'],['HQUA','HOSP'],['DEC_HQUA','DEC_HOSP']
          r=rd.randint(1,10)
          ddate=Dates[x:]
          if r>=1 and r<=4:
               rs=(rd.randint(1,2),0)[hosp_id==0]
               status=rec[rs]
               dco='NULL'
          elif r>=5 and r<=8:
               rs=(1,0)[hosp_id==0]
               status=infected[rs]
               dco='NULL'
          elif r>=8 and r<=10:
               rs=(1,0)[hosp_id==0]
               status=dead[rs]
               dco,x=randdate(ddate)
          if status in ['HQUA','REC_HQUA','DEC_HQUA']:
               gname=grel='Not Applicable'
               age=rd.randint(15,90)
          else:
               r=rd.randint(1,4)
               if r==1:
                    grel='PATIENT'
                    age=rd.randint(18,60)
                    gname=pname
               elif r==2:
                    grel='PRIMARY'
                    age=rd.randint(5,17)
                    gname=name()[0]
               elif r==3 or r==4:
                    grel='SECONDARY'
                    age=rd.randint(50,90)
                    gname=name()[0]
          j=[adrno,pname,age,gender,hosp_id,gname,grel,tpo,status,dco]
          for i in range(len(j)):
               j[i]=str(j[i])
          REC.append(j)
     return REC

def listtosql(l,t):
     for i in l:
          sql='insert into '+t+' values('
          for j in range(len(i)):
               if j!=len(i)-1:
                    sql+="'"+str(i[j])+"',"
               else:
                    sql+="'"+str(i[j])+"')"
          c.execute(sql)
     return c

def sfinder(h,r):
     s=[]
     for i in h:
          s.append(len(i))
     for i in r:
          for j in range(len(i)):
               k=len(str(i[j]))
               if k>s[j]:
                   s[j]=k
     return s
                                       
def unique_confirm(t,f,e):
     sql=c.execute('select '+f+' from '+t+' where '+f+'='+e)
     if sql:
          unique=False
     else:
          unique=True
     return unique  
               
def headextract(t):
     t=str(t)
     c.execute('desc '+t)
     h=c.fetchall()
     hl=[]
     for i in h:
          hl.append(i[0].upper())
     return hl

def l_printer(t):
     l=len(t)-3
     print()
     print('This table has',l//2,'records\n')
     i_no=3
     q=''
     if l==0:
          q='e'
     else:
          q=input('-Press "enter" to print records in batches of 20\n-"e" to show all records\n-Anything else to cancel printing of records\n')
     if q=='':
          for i in range(3):
               print(t[i])         
          for i in range(l):
               if i%40==0 and i!=0 and q=='':
                    print('\n20 records printed\n')
                    q=input('-Press "enter" to continue printing records in batches of 20\n-"e" to show all remaining records\n-Anything else to stop printing further Records\n')
                    if q=='':
                         for i in range(3):
                              print(t[i])
                         print(t[i_no]);i_no+=1
                    else:
                         break 
               else:
                    print(t[i_no]);i_no+=1
          else:
               print((l%40,40)[l%40==0]//2,'records printed',end='\n')
     if q in ['E','e']:
          for j in range(3):
               print(t[j])
          count=0
          for j in range(i_no,len(t)):
               print(t[i_no]);i_no+=1
               count+=1
          print(count//2,'records printed',end='\n')
     print('Total of',(i_no-2)//2,'records were printed')
                              
def tableprinter(l,s,h):
     line=''
     for j in range(len(h)):
          pluses='+%'+str(s[j]+2)+'s'
          line+=pluses%('-'*(s[j]+2))
     line+='+'
     t=[]
     if len(h)!=0:
          thead=''
          for i in range(len(h)):
               temp='| %'+str(s[i])+'s '
               thead+=temp%(str(h[i]).ljust(int(s[i])))
          thead+='|'
          t.append(line)
          t.append(thead)
     rec=''
     for i in l:
          rec=''
          for j in range(len(i)):
               temp='| %'+str(s[j])+'s '
               rec+=temp%(str(i[j]).ljust(int(s[j])))
          rec+='|'
          t.append(line)
          t.append(rec)
     t.append(line)
     return t

def searchintable(T,H,commonkey='',pH='*'):
                    print('*'*27)
                    print('INSTRUCTIONS')
                    print('*'*27)
                    print('1.To search your record enter a few starting keywords and this will search for all records starting with that keyword')
                    print("2.This program will ask for keyword for Each attribute in the Table")
                    print("3.If you dont want to give any keyword then, dont type anything and press 'enter' key to proceed on other attributes")
                    print("4.In case value is NULL then enter NULL not N or NU or NUL")
                    print("5. You can add multiple keywords by seperating keywords with ','")
                    print("Example: to get patients starting with letter 'a' or 'b', ")
                    print("         enter a,b in the prompt asking you to enter patient name keyword")
                    print('*'*27)
                    t=''
                    col='order by '
                    for i in T:
                         t+=i+','
                    t=t[:len(t)-1]
                    SQL='select '+pH+' from '+t+' where '
                    if len(T)>1:
                         for i in T:
                              SQL+=i+'.'+commonkey+'='
                         SQL=SQL[:len(SQL)-1]+' AND '
                    ckeyname=T[0]+'.'+commonkey
                    while True:
                         try:
                              for i in H:
                                   k=input('Enter few keywords for '+i+' :')
                                   if k=='':continue
                                   i=(i,ckeyname)[i==commonkey]
                                   col+=i+','
                                   s=k.split(',')
                                   sq='(%s) AND '
                                   sql=''
                                   for x in s:
                                        x=x.strip()
                                        sql+=(i+' LIKE '+"'"+x+"%'"+' or ',i+' IS NULL or ')[x=='NULL']
                                   sql=sql[:len(sql)-4]
                                   sql=sq%sql
                                   SQL+=sql
                              SQL=SQL.upper()
                              if SQL[len(SQL)-4:]=='AND ':
                                   SQL=SQL[:len(SQL)-4]
                                   col=col[:len(col)-1]
                                   SQL+=col
                              else:
                                   SQL=SQL[:len(SQL)-7]
                              c.execute(SQL)
                              records=c.fetchall()
                              break
                         except :
                              print('Invalid Input. Read instructions again')

                    return records
  
def v_rec(t):
          c.execute('select * from '+t)
          l=c.fetchall()
          h=headextract(t)
          col=''
          for i in h:
               col+=i.upper()+','
          col=col[:len(col)-1]
          while True:
               q=input('Want to show whole table(Y) or start a search in your table(N)? ')
               if q in ['N','n']:
                    l=searchintable([t],h)
                    break
               elif q in ['Y','y']:
                    r=c.execute('select * from '+t+' order by '+col)
                    l=c.fetchall()
                    break
               else:
                    print('invalid input')                    
          s=sfinder(h,l)

          t=tableprinter(l,s,h)
          l_printer(t)

def v_custom():
          t=['patient_rec','hosp_rec']
          H=[]
          for i in t:
               H+=headextract(i)
          commonkey='HOSP_ID'
          if commonkey!='':
               H.remove(commonkey)
          D={}
          for i in range(len(H)):
               D['C'+str(i+1)]=H[i]
          D_list=list(D.items())
          h=['KEY','COLUMN NAME']
          s=[4,25]
          t=tableprinter(D_list,s,h)
          for i in t:
               print(i)
          search_column=[]
          print('\n'+'*'*27)
          print('INSTRUCTIONS :-')
          print('*'*27)
          print("Enter the columns which are to be Printed by entering their column seperated by ','(comma)")
          print("Enter '@all' to print all columns and it can be proceeded with other other column seperated by ','(comma)")
          print("NOTE:Case sensitivity is not important")
          print("Example: To print AADHAR_NO and PATIENT_NAME, enter c1,c2 or C1,C2")
          print('Enter "Q" or "q" to quit')
          while True:
               try:
                    op=input('')
                    if op in ['Q','q']: break
                    opsplit=op.split(',')
                    SQL=''
                    h=[]
                    eopsplit=[]          
                    for i in range(len(opsplit)):
                         j=opsplit[i].upper()
                         if '@ALL' in j:
                                   for k in range(len(D)):
                                        eopsplit.append('C'+str(k+1))
                                        eopsplit.append(',')                             
                         else:
                              eopsplit.append(j)
                              eopsplit.append(',')  
                    eopsplit.pop()
                    for i in range(len(eopsplit)): 
                         j=eopsplit[i].upper()
                         if j in D:
                              if D[j].upper()=='HOSP_ID':
                                   SQL+='hosp_rec.'+D[j]
                              else:
                                   SQL+=D[j]
                         else:
                              SQL+=j
                    SQL=SQL.upper()
                    c.execute('Select '+SQL+' from patient_rec,hosp_rec where patient_rec.HOSP_ID=hosp_rec.HOSP_ID order by '+SQL)
                    l=c.fetchall()                    
                    while True:
                         q=input('Want to show whole table(Y) or start a search in your table(N)? ')
                         if q in ['N','n']:
                              l=searchintable(['patient_rec','hosp_rec'],H,'HOSP_ID',SQL)
                              break
                         elif q in ['Y','y']:  
                              break
                         else:
                              print('invalid input')     
                    shead=c.description
                    for i in shead:
                         h.append(i[0].upper())
                    s=sfinder(h,l)
                    for i in range(len(h)):
                         if len(h[i])>s[i]:
                              s[i]=len(h[i])
                         else:
                              continue
                    t=tableprinter(l,s,h)
                    l_printer(t)
                    break
               except:
                    print('Invalid input!!!    Read instructions again if there is confusion')     

def ViewRec():
     while True:
          print('\n'+'*'*27)
          print       ('1 - Search in Patient Table    ')
          print       ('2 - Search in Hospitals Table   ')
          print       ('3 - Search in Custom created Table')
          print       ('4 - Return to Previous Menu ')
          print('*'*27)
          ch=input('\nEnter Your Choice : ')
          if ch=='1':   v_rec('patient_rec')
          elif ch=='2': v_rec('hosp_rec')     
          elif ch=='3':v_custom()
          elif ch=='4':
               print('Thank You !')
               break
          else:
               print('INVALID INPUT !')

def addhosphosp_id():
    global L
    while True:
            hosp_id=input('Enter Hospital ID No. : ')
            if hosp_id.isdigit() is True:
                 unique=unique_confirm('hosp_rec','hosp_id',hosp_id)
            else:
                 print('INVALID HOSPITAL ID. !\nHOSPITAL ID IS A UNIQUE NUMBER MAXIMUM 5 DIGTS LONG!')
                 continue
            if len(hosp_id)<=5 and hosp_id>'00000' and unique:
                 L.append(hosp_id)
                 break
            elif unique==0:
                 print('Duplicate HOSPITAL ID\n Please enter correct Value')
            else:
                 print('INVALID HOSPITAL ID. !\nHOSPITAL ID IS A UNIQUE NUMBER MAXIMUM 5 DIGTS LONG!')
                 continue
               
def adddistrict():
    global L
    while True:
        try:
            print('Choose District  :-')
            D={1:'NEW DELHI',2:'CENTRAL DELHI',3:'EAST DELHI',4:'NORTH DELHI',5:'NORTH-EAST DELHI',6:'NORTH-WEST DELHI',7:'SHAHDARA',8:'SOUTH DELHI',9:'SOUTH-EAST DELHI',10:'SOUTH-WEST DELHI',11:'WEST DELHI'}
            for i,j in D.items():
                print(i,'-',j)
            dist=int(input("Enter District No  : "))
            dis=D[dist]
            L.append(dis)
            break
        except:
                print('INVALID CHOICE !')
                
def addhname():
    global L
    while True:
            hname=input("Enter Hospital Name(max 30 chars) : ")
            if len(hname)!=0 and len(hname)<=30:
                if all(x.isalpha() or x.isspace() for x in hname):
                    L.append(hname)
                    break
                else:
                    print('INVALID NAME !')          
            else:
                print('INVALID NAME !')
                
def addtbeds():
    global L
    while True:
            tbeds=input("Enter total beds available in hospital : ")
            if tbeds.isdigit() is True and int(tbeds)>0 and int(tbeds)<10000:
                L.append(tbeds)
                break
            else:
                print('Bed numbers should be a "+ve integer" !')

def addpincode():
    global L
    while True:
            pincode=input('Enter Pincode : ')
            if pincode.isdigit() is True and len(pincode)==6:
                L.append(pincode)
                break
            else:
                print('INVALID PINCODE. !\nPINCODE IS A UNIQUE 6 DIGIT NUMBER AND DOESN\'T CONTAIN ALPHABETS OR SPECIAL CHARACTERS !')

def AddHospRec():
    global L
    h=headextract('patient_rec')
    p=1
    while p==1:
        addhosphosp_id()
        adddistrict()
        addhname()
        addtbeds()
        L.insert(4,L[3])
        addpincode()
        sql='insert into hosp_rec values ("'+L[0]+'","'+L[1]+'","'+L[2]+'","'+L[3]+'","'+L[4]+'","'+L[5]+'")'
        c.execute(sql)
        db.commit()
        L.clear()
        print()
        print('HOSPITAL ADDED TO RECORDS SUCCESSFULLY\n')
        while True:
            x=input('Want to add more records? (y/n) : ')
            if x in ['n','N']:
                p=0
                break
            elif x in ['y','Y']:
                print()
                p=1
                break
            else:
                print('INVALID CHOICE !')

                
def addadr():
    global L
    while True:
            adrno=input('Enter Aadhar Card No : ')
            if adrno.isdigit() is True:
                 unique=unique_confirm('patient_rec','AADHAR_NO',adrno)
            else:
                 print('Invalid AADHAR NO.\nAADHAR NO. IS A UNIQUE 12 DIGIT NUMBER !')
                 continue
            if len(adrno)==12 and unique:
                L.append(adrno)
                break
            elif unique==0:
                 print('Patient already registered with this Aadhar No.!')
            else:
                print('Invalid AADHAR NO.\nAADHAR NO. IS A UNIQUE 12 DIGIT NUMBER !')
                
def addpname():
    global L
    while True:
            pname=input("Enter Patient's Full Name (max 25 chars) : ")
            if len(pname)!=0 and len(pname)<=25:
                if all(x.isalpha() or x.isspace() for x in pname):
                    L.append(pname)
                    break
                else:
                    print('INVALID NAME !')          
            else:
                print('INVALID NAME !')
                
def addpathosp_id():
    global L
    while True:
            c.execute('select HOSP_ID , HOSPITAL_NAME from hosp_rec order by HOSP_ID')
            for i,j in c.fetchall():
                print(i,'-',j)
            print('\nEnter 0 if patient is in Home-Quarantine or has NO Hospitalization record during Covid treatment in past.')
            hosp_id=input('Enter Hospital ID No. : ')
            
            if hosp_id.isdigit() is True:
                 unique=unique_confirm('hosp_rec','hosp_id',hosp_id)
            else:
                print('INVALID HOSPITAL ID.\nHOSPITAL ID IS A UNIQUE NUMBER MAXIMUM 5 DIGTS LONG!')
                continue
            avail=(True,c.execute('select AVAILABLE_BEDS from hosp_rec where hosp_id="'+hosp_id+'" and AVAILABLE_BEDS>0'))[hosp_id>'00000']
            hosp_id=hosp_id.rjust(5,'0')
            if len(hosp_id)<=5 and hosp_id>='00000' and not unique:
                if avail==0:
                      print('NOT ENOUGH BEDS !')
                      continue                
                L.append(hosp_id)
                break
            elif unique==1:
                 print('HOSPITAL ID does not exist in hospital table\nPlease register hospital in hospital table first then add here')
            else:
                print('INVALID HOSPITAL ID.\nHOSPITAL ID IS A UNIQUE NUMBER MAXIMUM 5 DIGTS LONG!')
            
def addage():
    global L
    while True:
            print("Enter Patient's age as of",now,end='')
            age=input(" : ")
            if age.isdigit() is True and int(age)>0 and int(age)<1000:
                L.append(age)
                break
            else:
                print('INVALID AGE !')
def addgen():
    global L
    while True:
            print("Enter Patient's gender(M/F)",end='')
            gen=input(" : ")
            gen=gen.upper()
            if gen in ['M','F']:
                L.append(gen)
                break
            else:
                print('INVALID INPUT !')
gname=0   
def addguaname():
    global gname,L
    while True:
            gname=input("Enter Guarantor's Name (max 25 chars) : ")
            if len(gname)!=0 and len(gname)<=25:
                if all(x.isalpha() or x.isspace() for x in gname):
                    break
                else:
                    print('INVALID NAME !')
            else:
                print('INVALID NAME !')
                
def addgrel():
    global gname,L
    while True:
            if L[4]!='00000':
                if int(L[2])>=18:
                    m=input('Is patient able to cover Medical Expenses himself/herself? (y/n) : ')
                    if m in ('y','Y'):
                        grel='PATIENT'
                        L.extend([L[1],grel])
                        break
                    elif m in ('n','N'):
                        while True:
                            addguaname()
                            print('Enter Guarantor age as of',now,end='')
                            age=input(" : ")
                            if age.isdigit() is True:
                                if int(age)>=18 and int(age)<=999:
                                    print('Guarantor Approved !')
                                    grel='SECONDARY'
                                    break
                                else:
                                    print('Guarantor must be an ADULT capable of covering Medical Expenses during treatment in Hospital ')
                            else:
                                print('INVALID AGE !')
                        L.extend([gname,grel])
                        break
                    else:
                        print('INVALID CHOICE !')
                else:
                    print('Minor Patient')
                    print('Guarantor is Parent or Legal Guardian ')
                    while True:
                        addguaname()
                        print('Enter Guarantor age as of',now,end='')
                        age=input(" : ")
                        if age.isdigit() is True:
                            if int(age)>=18 and int(age)<=999:
                                grel='PRIMARY'
                                print('Guarantor Approved !')
                                break
                            else:
                                print('Guarantor is Parent or Legal Guardian ')
                        else:
                            print('INVALID AGE !')
                    L.extend([gname,grel])
                    break
            else:
                gname=grel='Not Applicable'
                L.extend([gname,grel])
                break
                
def addtpo():
    global L
    while True:                                      
            tpo=input('Covid +ve tested on (YYYY-MM-DD) : ')
            try:
                Y,M,D=map(int,tpo.split('-'))
            except ValueError or TypeError:
                print('Invalid Date Type or Format !')
                print()
                continue
            from datetime import date
            today=date.today()
            try:
                date1=date(Y,M,D)  
            except:
                print('INVALID DATE !')
                continue
            if date1>today:
                print('Please Input a Valid Date !')
                print()
                continue
            else:
                L.append(tpo)
                break
            
def addstatus():
    global L
    while True:
            try:
                if L[4]=='00000':                    
                    print('Choose Current Status of Patient :-\n')
                    S1={1:'HOME-QUARANTINE',2:'RECOVERED AT HOME',3:'DECEASED AT HOME'}
                    for i,j in S1.items():
                        print(i,'-',j)
                    D1={1:'HQUA',2:'REC_HQUA',3:'DEC_HQUA'}
                    st1=int(input("\nEnter Status No  : "))
                    status1=D1[st1]
                    L.append(status1)
                    break                   
                else:                    
                    print('Choose Current Status of Patient :-\n')
                    S2={1:'HOSPITALIZED',2:'RECOVERED AT HOSPITAL',3:'DECEASED AT HOSPITAL'}
                    for i,j in S2.items():
                        print(i,'-',j)
                    D2={1:'HOSP',2:'REC_HOSP',3:'DEC_HOSP'}
                    st2=int(input("\nEnter Status No  : "))
                    status2=D2[st2]
                    L.append(status2)
                    break
            except:
                print('INVALID CHOICE !')
                
def adddeceasedon():
          global L
          if L[8].upper() in ['DEC_HQUA','DEC_HOSP']:
                   while True:                                      
                           dco=input('Deceased on (YYYY-MM-DD) : ')
                           try:
                               Y,M,D=map(int,dco.split('-'))
                           except ValueError or TypeError:
                               print('Invalid Date Type or Format!')
                               print()
                               continue
                           from datetime import date
                           today=date.today()
                           try:
                               date1=date(Y,M,D)  
                           except:
                               print('INVALID DATE !')
                               continue
                           if date1>today:
                               print('Please Input a Valid Date!')
                               print()
                               continue
                           else:
                               L.append(dco)
                               break               
          else:
               L.append('NULL')
               
def AddPatRec():
    global L
    h=headextract('patient_rec')
    p=1
    while p==1:
        addadr()
        addpname()
        addage()
        addgen()
        addpathosp_id()
        addgrel()
        addtpo()
        addstatus()
        adddeceasedon()
        sql='insert into patient_rec values ("'+L[0]+'","'+L[1]+'","'+L[2]+'","'+L[3]+'","'+L[4]+'","'+L[5]+'","'+L[6]+'","'+L[7]+'","'+L[8]+'",'+('"'+L[9]+'"',L[9])[L[9].upper()=='NULL']+')'  
        c.execute(sql)
        db.commit()

        print()
        print('Following Record is added:')
        s=sfinder(h,[L])
        t=tableprinter([L],s,h)
        L.clear()
        for i in t:
             print(i)
        print('PATIENT ADDED TO RECORDS SUCCESSFULLY\n')
        while True:
            x=input('Want to add more records? (y/n) : ')
            if x in ['n','N']:
                p=0
                break
            elif x in ['y','Y']:
                print()
                p=1
                break
            else:
                print('INVALID CHOICE !')

def AddRec():
     while True:
          abedupdater()
          print('\n'+'*'*27)
          print('\n1 - Add Record in Patient Table')
          print('2 - Add Record in Hospital Table')
          print('3 - Return to previous menu  ')
          print('\n'+'*'*27)
          ch=input('Enter Your Choice(1/2/3) : ')
          if ch=='1':AddPatRec()
          elif ch=='2':AddHospRec()
          elif ch=='3':break
          else:print('INVALID CHOICE')
def DeleteRec():
     while True:
          print('\n'+'*'*27)
          print("1 - Delete From Patient's Table")
          print("2 - Delete From Hospital's Table")
          print("3 - Return to Previous Menu")
          ch=input('Enter choice(1/2/3)')
          if ch=='1':DeleteRecPat()
          elif ch=='2':DeleteRecHosp()
          elif ch=='3':break
          else:print('INVALID CHOICE')
          
def DeleteRecHosp():
    while True:
        while True:
            try:
                r=input('Enter Hospital ID of Record to be deleted : ')
                if len(str(r))==5 :
                    c.execute("select * from hosp_rec where hosp_id="+str(r))
                    p=c.fetchone()
                    if p is None:   
                        print('Record Deletion Failed \nHospital ID NOT FOUND!')
                    else:
                        print('Following record is deleted...')
                        h=headextract('hosp_rec')
                        s=sfinder(h,[p])
                        t=tableprinter([p],s,h)
                        for i in t:
                             print(i)
                        c.execute('delete from hosp_rec where hosp_id='+str(r))
                        db.commit()
                        print('Record Deletion Successful !')
                        abedupdater()
                        break     
                else:
                    print('INVALID HOSPITAL ID\nHOSPITAL ID IS A UNIQUE 5 DIGIT NUMBER !')                
            except ValueError:
                print('INVALID HOSPITAL ID\nHOSPITAL ID IS A UNIQUE 5 DIGIT NUMBER !')                
        x=input('Want to Delete more records? (y/n) : ')
        if x in ['n','N']:
            break
     
def DeleteRecPat():
    while True:
        while True:
            try:
                r=int(input('Enter Aadhar No. of Record to be deleted : '))
                if len(str(r))==12:
                    c.execute("select * from patient_rec where AADHAR_NO="+str(r))
                    p=c.fetchone()
                    if p is None:   
                        print('Record Deletion Failed \nAADHAR NO. NOT FOUND!')
                    else:
                        print('Following record is deleted...')
                        h=headextract('patient_rec')
                        s=sfinder(h,[p])
                        t=tableprinter([p],s,h)
                        for i in t:
                             print(i)
                        c.execute('delete from patient_rec where AADHAR_NO='+str(r))
                        db.commit()
                        print('Record Deletion Successful !')
                        abedupdater()
                        break     
                else:
                    print('INVALID AADHAR NO.\nAADHAR NO. IS A UNIQUE 12 DIGIT NUMBER !')                
            except ValueError:
                print('INVALID AADHAR NO.\nAADHAR NO. IS A UNIQUE 12 DIGIT NUMBER !')                
        x=input('Want to Delete more records? (y/n) : ')
        if x in ['n','N']:
            break

def abbr():
    print('Abbreviations used :-\n')
    for i,j in {'HQUA    ':'HOME-QUARANTINE','HOSP    ':'HOSPITALIZED','REC_HQUA':'RECOVERED AT HOME','REC_HOSP':'RECOVERED AT HOSPITAL','DEC_HQUA':'DECEASED AT HOME','DEC_HOSP':'DECEASED AT HOSPITAL'}.items():
        print(i,'-',j)
    print()
    
def UpdateRec():
    global L,gname
    print("TO UPDATE HOSPITAL'S TABLE, DELETE AND RE-ADD RECORD")
    L=[]
    while True:
        z=1
        while z==1:
            try:
                r=int(input('Enter Aadhar No. of Record to be Updated : '))
                if len(str(r))==12:
                    c.execute("select * from patient_rec where AADHAR_NO="+str(r))
                    p=c.fetchone()
                    if p is None:   
                        print('Record Updation Failed \nAADHAR NO. NOT FOUND!')
                    else:
                        h=headextract('patient_rec')
                        R=[]
                        for i in p:
                            R.append(str(i))
                        s=sfinder(h,[R])
                        t=tableprinter([R],s,h)
                        for i in t:
                             print(i)
                        print()
                        print('Due to security and verification concerns, AADHAR No. cannot be updated !\nIn order to update AADHAR No. first delete the patient record and re-add it.')
                        while z==1:
                            x=input('Do you want to continue updation of other details? (y/n) : ')
                            if x in ['n','N']:
                                break
                            elif x in ['y','Y']:
                                L.append(R[0])
                                while True:
                                    u=1
                                    print('\nColumn codes :-')
                                    S={1:'Patient Name',2:'Age',3:'Gender',4:'Hospital ID',5:'Guarantor Details- Name',6:'Guarantor Details- Type',7:'(+) Test date',8:'Status'}
                                    for i,j in S.items():
                                        print(i,'-',j)
                                    print("\nINSTRUCTIONS :- ")
                                    print("Enter the columns which you want to update by entering column codes separated by ','(comma)")
                                    print("For eg: If you want to update Guarantor Name and Guarantor Type - type 4,5")
                                    y=input('Enter the column codes which are to be updated : ')
                                    w=y.split(',')
                                    w.sort()
                                    j,k=0,0
                                    for i in range(1,len(R)):
                                        if str(i) in w:
                                            if i==1:
                                                print('Current Patient Name :',R[1])
                                                x=input('Do you want to update Patient Name? (y/n) : ')
                                                if x in ['y','Y']:
                                                    addpname()
                                                else:
                                                    L.append(R[1])

                                            elif i==2:
                                                print('Current Age :',R[2])
                                                x=input('Do you want to update Age? (y/n) : ')
                                                if x in ['y','Y']:
                                                    addage()
                                                else:
                                                    L.append(R[2])
                                                if (int(R[2])>=18 and L[2]!=R[2] and int(L[2])<18) or (int(R[2])<18 and L[2]!=R[2] and int(L[2])>=18):
                                                    j=1
                                                    if '5' not in w and '6' not in w:
                                                        w.append('5')
                                                        w.sort()
                                            elif i==3:
                                                 print('Given Gender ',R[3])
                                                 x=input('Do you want to update Gender? (y/n) : ')
                                                 if x in ['y','Y']:
                                                     addgen()
                                                 else:
                                                     L.append(R[3])
                                                
                                            elif i==4:
                                                c.execute('select HOSPITAL_NAME from hosp_rec where HOSP_ID='+R[4])
                                                m=c.fetchone()
                                                M=[]
                                                for i in m:
                                                    M.append(str(i))
                                                print('Current Hospital :',M[0])
                                                x=input('Do you want to update Hospital? (y/n) : ')
                                                if x in ['y','Y']:
                                                    addpathosp_id()
                                                else:
                                                    L.append(R[4])
                                                if (L[4]=='00000' and R[4]!='00000') or (L[4]!='00000' and R[4]=='00000'):
                                                    k=1
                                                    if '5' not in w and '6' not in w:
                                                        w.append('5')
                                                        w.sort()
                                                    if '8' not in w:
                                                        w.append('8')
                                                        w.sort()

                                            elif i==5:
                                                if j==1 or k==1:
                                                    print('Current Guarantor Name :',R[5])
                                                    print('Current Guarantor Type :',R[6])
                                                    addgrel()
                                                else:
                                                    print('Current Guarantor Name :',R[5])
                                                    print('Current Guarantor Type :',R[6])
                                                    x=input('Do you want to update Guarantor Details? (y/n) : ')
                                                    if x in ['y','Y']:
                                                        addgrel()
                                                    else:
                                                        L.append(R[5])
                                                        L.append(R[6])

                                            elif i==6:
                                                if '5' in w:
                                                    pass
                                                else:
                                                    if j==1 or k==1:
                                                        print('Current Guarantor Name :',R[5])
                                                        print('Current Guarantor Type :',R[6])
                                                        addgrel()
                                                    else:
                                                        print('Current Guarantor Name :',R[5])
                                                        print('Current Guarantor Type :',R[6])
                                                        x=input('Do you want to update Guarantor Details? (y/n) : ')
                                                        if x in ['y','Y']:
                                                            addgrel()
                                                        else:
                                                            L.append(R[5])
                                                            L.append(R[6])

                                            elif i==7:
                                                print('Current Covid-19 (+) Tested Date :',R[7])
                                                x=input('Do you want to update Covid-19 (+)Tested Date? (y/n) : ')
                                                if x in ['y','Y']:
                                                    addtpo()
                                                else:
                                                    L.append(R[7])

                                            elif i==8:
                                                if k==1:
                                                    print('Current Patient Status :',R[8])
                                                    addstatus()
                                                else:
                                                    print('Current Patient Status :',R[8])
                                                    abbr()
                                                    x=input('Do you want to update the Status of Patient? (y/n) : ')
                                                    if x in ['y','Y']:
                                                        addstatus()
                                                    else:
                                                        L.append(R[8])
                                                    adddeceasedon()
                                            else:
                                                print('INVALID CHOICE !')
                                                u=0
                                        else:
                                            if '5' in w:
                                                if i!=6:  
                                                  L.append(R[i])  
  
                                            elif '6' in w:
                                                if i!=5:  
                                                  L.append(R[i])
                                            else:
                                                L.append(R[i])
                                    if u==1:
                                            if L[9]=='None':
                                                 L[9]='NULL'
                                            c.execute('delete from patient_rec where AADHAR_NO='+str(r))
                                            db.commit()
                                            sql='insert into patient_rec values ("'+L[0]+'","'+L[1]+'","'+L[2]+'","'+L[3]+'","'+L[4]+'","'+L[5]+'","'+L[6]+'","'+L[7]+'","'+L[8]+'",'+('"'+L[9]+'"',L[9])[L[9].upper()=='NULL']+')'
                                            c.execute(sql)
                                            db.commit()
                                            print('\nRECORD UPDATION SUCCESSFUL !\n')
                                            L.clear()
                                            z=0
                                            break
                                        
                                    else:
                                            continue
                                break
                            else:
                                print('INVALID CHOICE !')
                        
                else:
                    print('INVALID AADHAR NO.\nAADHAR NO. IS A UNIQUE 12 DIGIT NUMBER !')                
            except ValueError:
                print('INVALID AADHAR NO.\nAADHAR NO. IS A UNIQUE 12 DIGIT NUMBER !')
                
        x=input('Want to Update more records? (y/n) : ')
        if x in ['n','N']:
            print()
            break
        else:
            z=1
            continue
          
def abedupdater():
     c.execute('update hosp_rec set AVAILABLE_BEDS=TOTAL_BEDS')
     c.execute('select hosp_id,count(*) from patient_rec where status="hosp" group by hosp_id')
     r=c.fetchall()
     D=dict(r)
     for i in D:
          if i!=0:
               sql='update hosp_rec set AVAILABLE_BEDS=TOTAL_BEDS-'+str(D[i])+' where HOSP_ID='+str(i)
               c.execute('update hosp_rec set AVAILABLE_BEDS=TOTAL_BEDS-'+str(D[i])+' where HOSP_ID='+str(i))
     db.commit()
     
def totalcases():
        r=c.execute('select * from patient_rec')
        print('Total cases as of',t,' - ',r)

def activecases():
        a=c.execute('select * from patient_rec where STATUS in ("HOSP","HQUA")')
        print('Active cases as of',t,' - ',a)
        
def allbeds():
        p=c.execute('select sum(AVAILABLE_BEDS) from hosp_rec')
        q=c.fetchone()
        for i in q:
                i=str(i)
        print('Available beds as of',t,' - ',i)
        
def totbeds():
        p=c.execute('select sum(TOTAL_BEDS) from hosp_rec')
        q=c.fetchone()
        for i in q:
                i=str(i)
        print('Total beds as of',t,' - ',i) 

def plot1():
                x = np.array(Months)
                y = np.array(daily_cases)
                plt.subplot(1, 2, 1)
                plt.plot(x,y,marker='o',linestyle='dotted',label='Monthly Cases')
                y = np.array(total_cases)
                plt.plot(x,y,marker='v',label='Total Cases')
                plt.xlabel("Months")
                plt.ylabel("Number of Cases (Orange:Total Cases, Blue:Monthly Cases)")
                plt.title("COVID-19 Cases of Delhi", fontsize = 20)
                plt.show()

def plot2():
                p1=c.execute('select * from patient_rec where AGE between 0 and 17')
                p2=c.execute('select * from patient_rec where AGE between 18 and 59')
                p3=c.execute('select * from patient_rec where AGE between 60 and 120')
                category = ["Children(0-17 yrs)", "Adult(18-59 yrs)", "Senior Citizen(60+ yrs)"]
                count = [p1, p2, p3]
                plt.xlabel('Age-group')
                plt.ylabel('Number of Cases')
                plt.title('COVID-19 Cases Among Various Age-groups')
                plt.bar(category,count,0.3)
                plt.show()

def main():
     global c,dbname,db
     print('\nLogged in -',t)
     print('\n','*'*81,sep='')
     print('Welcome to COVID-19 Patient and Healthcare Database Management System Version 1.0\nMinistry of Health and Family Welfare, Government Of Delhi')
     print('*'*81)
     while True:
                     abedupdater()
                     print('\nCurrent Statistics:-\n')
                     print('*'*50)
                     totalcases()
                     activecases()
                     totbeds()
                     allbeds()
                     n1=c.execute('select * from patient_rec where TESTED_ON="'+d.strftime( "%Y-%m-%d" )+'"')
                     n2=c.execute('select * from patient_rec where TESTED_ON like "'+t2+'-__"')
                     print('Tested Positive today -',n1)
                     print('Tested Positive this month -',n2)
                     print('*'*50)
                     print('\nYou can navigate to the following options :-\n')
                     print('1 - View Statistics (Curves and Graphs)')
                     print('2 - Enter Database Management System  ')
                     print('3 - Reset Tables')
                     print('4 - Exit\n')
                     x=input('Enter choice(1/2/3/4) : ')
                     if x=='1':
                          while True:         
                               y=input('\n1 - Epidemic Curve\n2 - Widespread by Age-group\n3 - Return to Previous menu\n\nEnter Choice(1/2/3) : ')
                               if y=='1':
                                    plot1()
                               elif y=='2':
                                    plot2()
                               elif y=='3':
                                    break
                               else:
                                    print('INVALID CHOICE !')
                     elif x=='2':
                             initi()
                     elif x=='3':tablereset()
                     elif x=='4':
                          print('Ending The Program......')
                          break
                     else:
                          print('INVALID CHOICE !')

def initi():
     while True:
               abedupdater()
               print('\n'+'*'*27)
               print('1 - View Records')
               print('2 - Add Records ')
               print('3 - Update Records ')
               print('4 - Delete Records ')
               print('5 - Return to Previous menu')
               print('*'*27+'\n')
               ch=input('Select your choice(1/2/3/4/5) : ')
               if ch=='1':ViewRec()
               elif ch=='2':AddRec()
               elif ch=='3':UpdateRec()
               elif ch=='4':DeleteRec()
               elif ch=='5':break
               else:print('INVALID CHOICE !')

#Main Code
d = datetime.today()
now=d.strftime( "%Y/%m/%d" )
nowa = datetime.now()
t=nowa.strftime("%Y-%m-%d %H:%M:%S")
L=[]
c,db,dbname=0,0,0
ans=1
t2 = str(datetime.now())[0:7]
month=int(t2[5:])
year=int(t2[:4])-1
D={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
Dates=[]
Months=[]
daily_cases=[]
total_cases=[]
for i in range(12):
        y=month+i
        x=(12,y%12)[y!=12]
        year=(year,year+1)[y==13]
        m=str(year).rjust(4,'0')+'-'+str(x).rjust(2,'0')
        Dates.append(m)
        Months.append(D[x]+'\n'+str(year))
try:
     F=open('installlog.txt','r')
     dbname=F.read()
     F.close()
     while True:
          try:
               p=input('Enter Password : ')
               db=MS.connect(host='localhost',user='root',passwd=p)
               c=db.cursor()
               c.execute('use '+dbname)
               print('Connection Established')
               break
          except:
               print('INVALID PASSWORD !')     
except FileNotFoundError:
     c,db,dbname=installer()
     F=open('installlog.txt','w')
     F.write(dbname);F.close()
     if ans==1:
          tablereset()

sql='select PATIENT_NAME from patient_rec where TESTED_ON like "'

for i in Dates:
        s=sql+i+'-__"'
        r=c.execute(s)
        daily_cases.append(r)
r=0
for i in Dates:
        s=sql+i+'-__"'
        r+=c.execute(s)
        total_cases.append(r)
main()
