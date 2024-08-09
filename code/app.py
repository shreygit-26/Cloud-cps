from flask_mail import *
from flask import request,Flask,render_template,session,redirect,url_for
import pymysql
import random
from random import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from math import *
import pandas as pd

app=Flask(__name__)
app.config['SECRET_KEY']='b0b4fbefdc48be27a6123605f02b6b86'
db = pymysql.connect(host='localhost',user='root',password='',db='Cloud')
cursor=db.cursor()

mail = Mail(app)
otp = randint(000000, 999999)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

#CLOUD SERVICE PROVIDER
@app.route("/csp",methods=['POST','GET'])
def csp():
    if request.method=='POST':
        Name=request.form['Name']
        Password=request.form["Password"]
        if Name == 'CSP' and Password == 'CSP':
            session["Name"]=Name
            return render_template("Cloud Service Providers Home.html",msg="success",Name=Name)
        else:
            return render_template("Cloud Service Providers.html",msg="Failure")

    return render_template("Cloud Service Providers.html")

@app.route("/homes")
def homes():
    return render_template("homes.html")
@app.route("/ViewOwnersAndAuthorization")
def ViewOwnersAndAuthorization():
    sql="select * from Dataowners "
    cursor.execute(sql)
    result=pd.read_sql_query(sql,db)
    print(result)
    return render_template("ViewOwnersAndAuthorization.html",col_name=result.columns.values,row_val=result.values.tolist())

@app.route("/authorizationkey/<s1>/<s2>")
def authorizationkey(s1=0,s2=''):
    print(s1,s2)
    otp = randint(000000, 999999)
    session["otp"]=otp
    print(otp)
    # msg="your secret key is:"
    # mail_content = msg + ' ' + str(otp)
    # sender_address = 'nagamchenchulakshmi@gmail.com'
    # sender_pass = 'lakshmi@506'
    # receiver_address = s2
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = 'Dual access control for cloud based storage and sharings'
    # message.attach(MIMEText(mail_content, 'plain'))
    # session = smtplib.SMTP('smtp.gmail.com', 587)
    # session.starttls()
    # session.login(sender_address, sender_pass)
    # text = message.as_string()
    # session.sendmail(sender_address, receiver_address, text)
    # session.quit()
    sql = "update Dataowners set Otp=%s where slno='%s' " % (otp,s1)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('ViewOwnersAndAuthorization'))

# cloud view data users
@app.route("/ViewUsers")
def ViewUsers():
    sql="select * from datausers "
    cursor.execute(sql)
    result=pd.read_sql_query(sql,db)
    results=result.drop(["Otp","Slno","fileid"],axis=1)
    return render_template("ViewUsers.html", col_name=results.columns.values,row_val=results.values.tolist())

@app.route("/ViewUsersrequest")
def ViewUsersrequest():

    sql="select * from request where status='pending'"
    cursor.execute(sql)
    result=pd.read_sql_query(sql,db)
    result=result.drop(["pkey"],axis=1)
    return render_template("ViewUsersrequest.html", col_name=result.columns.values,row_val=result.values.tolist())

@app.route('/forwaordtoauthority/<s1>/<s2>')
def forwaordtoauthority(s1=0,s2="",s3="",s4=0):
    print(s1,"dwe",s2)
    c="forworded to authority"
    print(c)
    status="Accepted"
    sql="update request set status='%s' where id='%s' "%(status,s1)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('ViewUsersrequest'))

# AUTHORITY PAGES
@app.route("/Authority",methods=['POST','GET'])
def Authority():
    if request.method=='POST':
        Name=request.form['Name']
        Password=request.form["Password"]
        if Name == 'Authority' and Password == 'Authority':
            session["Name"]=Name
            return render_template("Authority Home.html",msg="success",Name=Name)
        else:
            return render_template("Authority Home.html",msg="Failure")
    return render_template("Authority.html")

#authority viewing users
@app.route("/AuthorityViewUsers")
def AuthorityViewUsers():
    sql = "select * from request where status='Accepted'"
    cursor.execute(sql)
    result = pd.read_sql_query(sql, db)
    result=result.drop(["pkey"],axis=1)
    print(result)
    result["Key Generation"]="Generate Key"
    return render_template("AuthorityViewUsers.html",col_name=result.columns.values,row_val=result.values.tolist())

#genearating key to users
@app.route("/generatekeytouser/<s1>/<s2>/<s3>")
def generatekeytouser(s1=0,s2="",s3=0):
    print(s1,s2,s3)
    otp = randint(123593489, 600876509)
    # msg="your secret key is:"
    # mail_content = msg + ' ' + str(otp)
    # sender_address = 'nagamchenchulakshmi@gmail.com'
    # sender_pass = 'lakshmi@506'
    # receiver_address = s2
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = 'Dual access control for cloud based storage and sharings'
    # message.attach(MIMEText(mail_content, 'plain'))
    # session = smtplib.SMTP('smtp.gmail.com', 587)
    # session.starttls()
    # session.login(sender_address, sender_pass)
    # text = message.as_string()
    # session.sendmail(sender_address, receiver_address, text)
    # session.quit()
    sql="update request set pkey=%s where id='%s' " %(otp,s1)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('AuthorityViewUsers'))

@app.route("/Viewusersforauthorization")
def Viewusersforauthorization():
    sql = "select * from datausers "
    cursor.execute(sql)
    result = pd.read_sql_query(sql, db)
    results = result.drop(["fileid"], axis=1)
    print(results)
    return render_template("Viewusersforauthorization.html",col_name=results.columns.values,row_val=results.values.tolist())

@app.route("/generatekeytouserforauthorization/<s1>")
def generatekeytouserforauthorization(s1=0):
    Otp = randint(123456789, 980976509)
    # sender_address = 'nagamchenchulakshmi@gmail.com'
    # sender_pass = 'lakshmi@506'
    # receiver_address = s2
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message.attach(MIMEText(Otp, 'plain'))
    # abc = smtplib.SMTP('smtp.gmail.com', 587)
    # abc.starttls()
    # abc.login(sender_address, sender_pass)
    # text = message.as_string()
    # abc.sendmail(sender_address, receiver_address, text)
    # abc.quit()
    sql = "update datausers set Otp=%s  where Slno='%s' " % (Otp,s1)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('AuthorityViewUsers'))


# DATAOWNER PAGES
@app.route("/DataOwners",methods=['POST','GET'])
def DataOwners():
    print("aaaaaaaaaaa")
    if request.method=='POST':
        print("11111111111")
        Name=request.form['Name']
        # Password=request.form['Password']
        Email=request.form["Email"]
        Number=request.form["Number"]
        Gender=request.form["Gender"]
        Address=request.form["Address"]
        c="Authorization"
        # d="dualaccess"
        sql="insert into Dataowners (Name,Email,Number,Gender,Address,Otp) values (%s,%s,%s,%s,%s,%s)"
        print("22222222222")
        val=(Name,Email,Number,Gender,Address,c)
        print("3333333333333333")
        cursor.execute(sql,val)
        Results=cursor.fetchall()
        db.commit()
        return render_template("Data Owners.html",message="register",name=Name)
    return render_template("Data Owners.html")


@app.route("/DataOwnerslogin",methods=['POST','GET'])
def DataOwnerslogin():
    if request.method=='POST':
        Email=request.form["Email"]
        OTP=request.form["OTP"]
        sql="select * from Dataowners where Email=%s and Otp=%s "
        val=(Email,OTP)
        X=cursor.execute(sql,val)
        Results=cursor.fetchall()
        if X>0:
            print(Results)
            session["nj"]=Results[0][2]
            session["ki"]=Results[0][0]

            print(session["nj"])
            return render_template("Data Owners Home.html",msg="sucess",name=session["nj"])
        else:
            print("5555555555555")
            return render_template("Data Owners.html",mfg="not found")
    return render_template("DataOwnerslogin.html")

@app.route("/DataOwnersUploadFiles",methods=['POST','GET'])
def DataOwnersUploadFiles():
    if request.method=='POST':
        FileName=request.form["FileName"]
        Keywords=request.form["Keywords"]
        Files=request.form["Files"]
        session["dcb"]="No Request Recieved"
        dd = "D:/rupesh/cloud project-dual access/uploadFiles/" + Files
        f = open(dd, "r")
        data = f.read()
        sql="insert into filesupload (owneremail,FileName,Keywords,Files) values (%s,%s,%s,AES_ENCRYPT(%s,'rupesh'))"
        values=(session["nj"],FileName,Keywords,data)
        cursor.execute(sql,values)
        db.commit()
        return render_template("DataOwnersUploadFiles.html",msg="success",files=Files)
    return render_template("DataOwnersUploadFiles.html")

@app.route("/DataOwnersViewFiles")
def DataOwnersViewFiles():
    print("aaaaaaaaaaa")
    sql = "select * from filesupload where owneremail='%s' "%(session["nj"])
    cursor.execute(sql)
    db.commit()
    result=cursor.fetchall()
    result = pd.read_sql_query(sql, db)
    return render_template("DataOwnersViewFiles.html", col_name=result.columns.values, row_val=result.values.tolist())

@app.route("/DataOwnersViewAllFiles")
def DataOwnersViewAllFiles():
    sql="select * from filesupload where owneremail !='%s'"%(session["nj"])
    cursor.execute(sql)
    data=pd.read_sql_query(sql,db)
    data1=data.drop(["Keywords","Files"],axis=1)
    data1["Files"]="HIDDEN FILE NAME"
    return render_template("DataOwnersViewAllFiles.html", col_name=data1.columns.values, row_val=data1.values.tolist())

@app.route("/requestfordualaccess/<s1>/<s2>/<s3>")
def requestfordualaccess(s1=0,s2='',s3=''):
    print("aaaaaaaaaaaaaaaa",session["nj"])

    sql="insert into ownership (Email,fname,omail,Sl_No) values(%s,%s,%s,%s)"
    val=(s2,s3,session["nj"],s1)
    cursor.execute(sql,val)
    db.commit()
    return redirect(url_for("DataOwnersViewAllFiles"))

@app.route("/Viewdualaccessrequests")
def Viewdualaccessrequests():
    d="requestsenttouser"
    sql="select * from ownership where omail='%s' and status ='Accepted' "%(session["nj"])
    cursor.execute(sql)
    results=pd.read_sql_query(sql,db)
    result=results.drop(["status","omail"],axis=1)
    result['Action']=""
    print(result)
    return render_template("Viewdualaccessrequests.html",col_name=result.columns.values, row_val=result.values.tolist())

@app.route("/khjhjk")
def khjhjk():
    sql = "select * from filesupload where dualaccess='%s'" % (session["a"])
    cursor.execute(sql)
    res = cursor.fetchall()
    return render_template("khjhjk.html")


@app.route("/acceptdualaccess/<s1>")
def acceptdualaccess(s1=0):
    session["a"]="request accepted"
    print(session["a"],s1)
    sql="update filesupload set dualaccess='%s' where Sl_No='%s'"%(session["a"],s1)
    cursor.execute(sql)
    print("CCCCCCCCCCCCCC")
    db.commit()
    return redirect(url_for('khjhjk'))

@app.route("/Viewdualaccessresponse")
def Viewdualaccessresponse():
    sql = "select * from ownership where status='waiting' and Email='%s'" %(session["nj"])
    cursor.execute(sql)
    data=pd.read_sql_query(sql,db)
    data1 = data.drop(["status", "Email", "Sl_No"], axis=1)
    data1["action"] = 'Action'
    return render_template("Viewdualaccessresponse.html",col_name=data1.columns.values, row_val=data1.values.tolist())


@app.route("/download1/<s1>")
def download1(s1=0):
    sql = "update ownership set status='Accepted' where id='%s'" % (s1)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('Viewdualaccessresponse'))

@app.route("/download/<s1>")
def download(s1=0):
    sql="SELECT Files, AES_DECRYPT(Files, 'rupesh') FROM filesupload where Sl_No='%s'"% (s1)
    # sql = "select AES_DECRYPT(Files,'rupesh') from  where Sl_No='%s' " % (s1)
    cursor.execute(sql)
    data=pd.read_sql_query(sql,db)

    print(data)
    return render_template("download.html",row_val=[[data.values[0][1].decode('utf8')]])

# DATA USERS PAGES
@app.route("/DataUsers",methods=['POST','GET'])
def DataUsers():
    if request.method=='POST':
        Name=request.form['Name']
        # Password=request.form["Password"]
        Email=request.form["Email"]
        Number=request.form["Number"]
        Gender=request.form["Gender"]
        Address=request.form["Address"]
        j="Authorization"
        sql="insert into datausers (Name,Email,Number,Gender,Address,Otp) values (%s,%s,%s,%s,%s,%s)"
        print(sql)
        val=(Name,Email,Number,Gender,Address,j)
        cursor.execute(sql,val)
        db.commit()
        return render_template("DataUsers.html",msg="sucess",name=Name)
    return render_template("DataUsers.html")

#datausers login
@app.route("/DataUsersLogin",methods=["POST","GET"])
def DataUsersLogin():
    if request.method=='POST':
        Email=request.form["Email"]
        Otp=request.form["Otp"]
        print(Otp,Email)
        sql = "select * from dataUsers where Email=%s and Otp=%s "
        val = (Email, Otp)
        X = cursor.execute(sql, val)
        Results = cursor.fetchall()
        if X > 0:
            print("results[0]")
            session["id"]=Results[0][0]
            session["Email"]=Results[0][2]
            name=Results[0][1]
            print(session["id"])
            return render_template("DataUsers Home.html", msg="LOGIN",name=name)
        else:
            print("5555555555555")
            return render_template("DataUsers.html", mfg="not found")
    return render_template("DataUsersLogin.html")

@app.route("/ViewDataOwnerFile/<s1>")
def ViewDataOwnerFile(s1=0):
    sql = "SELECT * from OwnerUploadFiles where SL.NO='%s'" %(s1)
    print(s1)
    cursor.execute(sql)
    return render_template("ViewDataOwnerFile.html")

#user profile
@app.route("/DataUsersProfile")
def DataUsersProfile():
    sql="select * from datausers where Slno='%s' " %(session["id"])
    print(sql)
    cursor.execute(sql)
    result=pd.read_sql_query(sql,db)
    print(result.columns.values)
    Result=result.drop(["Slno","fileid"],axis=1)
    print(Result.columns.values)
    return render_template("DataUsersProfile.html",col_name=Result.columns.values,row_val=Result.values.tolist())

#searching files
@app.route("/DataUsersSearchFiles",methods=['POST','GET'])
def DataUsersSearchFiles():
    if request.method=='POST':
        Name=request.form['Keywords']
        try:
            sql = "select * from filesupload where Keywords='%s' " % (Name)
            print(sql)
            cursor.execute(sql)
            X = cursor.fetchall()
            db.commit()
            print(X[0][0])#important
            results=pd.read_sql_query(sql,db)
            results["action"]=""
            # result=results.drop(["user","dualaccess","dualaccessownerid","status"],axis=1)
            return render_template("DataUsersSearchFilesDisplay.html", col_name=results.columns.values,row_val=results.values.tolist())
        except:
            return render_template("DataUsersSearchFiles.html",msg="not found")
    return render_template("DataUsersSearchFiles.html")

@app.route("/DataUserRaiseRequest/<s1>/<s2>")
def DataUserRaiseRequest(s1=0,s2=''):
    print(s1)
    global n,fname
    n=s1
    fname=s2
    email=session.get('Email')
    sql="insert into request(email,fname,Sl_No) values(%s,%s,%s)"
    val=(email,fname,n)
    cursor.execute(sql,val)
    db.commit()
    print("CCCCCCCCC")
    db.commit()
    return redirect(url_for('DataUsersSearchFiles'))

@app.route("/secretkeyresponse")
def secretkeyresponse():
    sql="select * from request where status='Accepted' and email='%s' "%(session["Email"])
    cursor.execute(sql)
    data=pd.read_sql_query(sql,db)
    print(data.columns.values)
    vmp=data.drop(["pkey"],axis=1)
    # vmp["Action"]="FileDownload"
    return render_template("secretkeyresponsehome.html",col_name=vmp.columns.values,row_val=vmp.values.tolist())

@app.route("/enterkey/<s1>/<s2>",methods=['POST','GET'])
def enterkey(s1=0,s2=0):
    print(s1,s2)
    return render_template("enterkey.html",s1=s1,s2=s2)

@app.route("/key",methods=["POST","GET"])
def key():
    if request.method=='POST':
        file=request.form["pkey"]
        gkey = request.form['id']
        fid = request.form['fid']
        print(file,gkey,fid)
        try:
            sql="select AES_DECRYPT(Files,'rupesh') from filesupload,request where request.pkey='"+file+"' and request.id='"+gkey+"' and filesupload.Sl_No='"+fid+"' "
            data=pd.read_sql_query(sql,db)
            return render_template("key.html",row_val=[[data.values[0][0].decode('utf8')]])
        except:
            return render_template("key.html",msg="notfound")
    return render_template("key.html")
@app.route("/filedownload/<s1>")
def filedownload(s1=0):
    print(s1)
    return render_template("filedownload.html")

if(__name__)==("__main__"):
    app.run(debug=True)

