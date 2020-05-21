from flask import Flask, render_template, request, send_from_directory,redirect,flash,session,Response,stream_with_context
from flask import send_file
import subprocess, sys
import pexpect
import sys
from multiprocessing import Value
import netmiko
from netmiko import ConnectHandler
import flask_monitoringdashboard as dashboard
import sqlite3
import os
import urllib.request
from application import application
from werkzeug.utils import secure_filename
import datetime
import fnmatch
import time
from file_verify import *

##Depended Scripts for Network Alarms Processing Tool
#1)Applicaton.py #2)file_verify.py #3)/data/Project


def sqlliteQueryResult():
    userData = list()
    conn = sqlite3.connect('flask_monitoringdashboard.db')
   
    
    cur = conn.execute('Select Count(*) from Request where endpoint_id = 13;')
    cur1 = conn.execute('SELECT COUNT(DISTINCT ip) FROM Request')
    cur2 = conn.execute('Select Count(*) from Endpoint;')
    for row in cur:
       userData.append(row[0]) 
    for row in cur1:
         userData.append(row[0]) 
    for row in cur2:
         userData.append(int(row[0]) - 16) 
    return userData;
   

    

app = Flask(__name__)
dashboard.bind(app)
app.config["FILE_UPLOADS"] = "/data/vivek/twampFiles"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["CSV", "XLSX"]
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route('/')
def home():
    userData = sqlliteQueryResult()
    return render_template('index.html', userCount= userData[0], uniqueUsers=userData[1], projectsHosted = userData[2] )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/genie')
def genie():
    output = ''
    return render_template('genie.html', len = len(output))

# @app.route('/genie', methods=['POST'])


# def genie_form():
#     name = request.form['name']
#     nodeip = request.form['nodeip']
#     uname = request.form['username']
# #    pword = request.form['pword']
#     action = request.form['action']
#     feature = request.form['feature']
#     result = 'wonderful'
#     folderName = uname+ "_"  + name

#     pobj = pexpect.spawn('/bin/bash', timeout=120)

#     if "precheck" in action:
#         fout = open('static/genieprecheck.txt', 'w')
#         pobj.expect('$', timeout=10)
#         pobj.sendline("sudo su root")
#         pobj.expect('mpls', timeout=10)
#         pobj.sendline("Airtel@123")
#         pobj.expect(['#'])
#         pobj.sendline("source /data/SunilB/genie/bin/activate")
#         pobj.expect('#')
#         pobj.sendline("mkdir /data/SunilB/genie/test/"+folderName)
#         pobj.expect('#')
#         pobj.sendline("kill $(ps aux | grep 9888 | awk '{print $2}');kill $(ps aux | grep 9887 | awk '{print $2}');kill $(ps aux | grep 9888 | awk '{print $2}')")
#         pobj.expect('#')
#         pobj.sendline("mkdir /data/SunilB/genie/test/"+folderName+"/precheck")
#         pobj.expect('#')
#         pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/precheck")
#         pobj.expect('#')
#         pobj.sendline("python3.4 -m http.server 9887 &> /dev/null & pid=$!")
#         pobj.expect('#')
#         # pobj.sendline("cd /data/SunilB/genie/test/precheck/")
#         # pobj.expect(['#'])
#         # pobj.sendline("rm -rf *")
#         # pobj.expect(['#'])
#         # pobj.sendline("cd /data/SunilB/genie/test/postcheck/")
#         # pobj.expect(['#'])
#         pobj.sendline("mkdir /data/SunilB/genie/test/"+folderName+"/postcheck")
#         pobj.expect('#')
#         pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/postcheck")
#         pobj.expect('#')
#         pobj.sendline("python3.4 -m http.server 9888 &> /dev/null & pid=$!")
#         pobj.expect('#')
#         #pobj.sendline("rm -rf *")
#         #pobj.expect(['#'])
#         # pobj.sendline("cd /data/SunilB/genie/test/diff/")
#         # pobj.expect(['#'])
#         pobj.sendline("mkdir /data/SunilB/genie/test/"+folderName+"/diff")
#         pobj.expect('#')
#         pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/diff")
#         pobj.expect('#')
#         pobj.sendline("python3.4 -m http.server 9889 &> /dev/null & pid=$!")
#         pobj.expect('#')
#         # pobj.sendline("rm -rf *")
#         # pobj.expect(['#'])
#         pobj.sendline("cd /data/SunilB/genie/test/")
#         pobj.expect(['#'])
#         pobj.sendline("python genie_builder.py "+folderName+" "+nodeip)
#         pobj.expect(['#'])
#         fout = open('static/genieprecheck.txt', 'w')
#         pobj.logfile = fout.buffer
#         pobj.sendline("genie learn " +feature+" --testbed "+name+".yaml --output "+folderName+"/precheck/")
#         pobj.expect(['#', pexpect.TIMEOUT])
#         pobj.close()
#         fin = open("static/genieprecheck.txt", "r")
#         value1 = fin.read()
#         with counter.get_lock():
#             counter.value +=1
#         fin.close()
#         result1 = 'c'
#         return render_template('pass.html', result=value1)

#     elif "postcheck" in action:
#         fout = open('static/geniepostcheck.txt', 'w')
#         pobj.expect('$', timeout=10)
#         pobj.sendline("sudo su root")
#         pobj.expect('mpls', timeout=10)
#         pobj.sendline("Airtel@123")
#         pobj.expect('#')
#         pobj.sendline("source /data/SunilB/genie/bin/activate")
#         pobj.expect('#')
#         pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/")
#         pobj.expect('#')
#         pobj.logfile = fout.buffer
#         pobj.sendline("genie learn " +feature+" --testbed "+name+".yaml --output postcheck/")
#         pobj.expect(['#', pexpect.TIMEOUT])
#         fin = open("static/geniepostcheck.txt", "r")
#         value1 = fin.read()
#         with counter.get_lock():
#             counter.value +=1
#         fin.close()
#         result1 = 'c'
#         return render_template('pass.html', result=value1)

#     elif "diff" in action:

#         fout = open('static/diff.txt', 'w')
#         pobj.expect('$', timeout=10)
#         pobj.sendline("sudo su root")
#         pobj.expect('mpls', timeout=10)
#         pobj.sendline("Airtel@123")
#         pobj.expect('#')
#         pobj.sendline("source /data/SunilB/genie/bin/activate")
#         pobj.expect('#')
#         pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/")
#         pobj.expect('#')
#         pobj.logfile = fout.buffer
#         pobj.sendline("genie diff precheck postcheck --output diff/")
#         pobj.expect(['#', pexpect.TIMEOUT])
#         fin = open("static/diff.txt", "r")
#         value1 = fin.read()
#         with counter.get_lock():
#             counter.value +=1
#         fin.close()
#         result1 = 'c'
#         return render_template('pass.html', result=value1)


@app.route('/traceroute/')
def traceroute():
    output = ''
    return render_template('traceroute.html', len = len(output))
@app.route('/traceroute/', methods=['POST'])
def traceroute_form():
    username = request.form['form']
    password = request.form['form1']
    Source_IP = request.form['form2']
    Destination_IP = request.form['form3']
    ping_count = request.form['form4']
   # print(input2)
    # input1  = request.form['data_array']
    # print(input1)
    pobj = pexpect.spawn('/bin/bash')
    pobj.setwinsize(400,400)
    fout = open('static/mylog.txt', 'w')

    #result = StringIO()
    #sys.stdout = result

    pobj.expect('$', timeout=10)
    pobj.sendline("sudo su root")
    pobj.expect('#',timeout=10)
    pobj.sendline("cd /root/ts")
    pobj.expect('#', timeout=10)

    pobj.sendline("python3.4 Route_Analyser.py")

    pobj.expect("username")
    pobj.sendline(username)
    while True:
        try:
            pobj.expect("Password", timeout=1)
            pobj.sendline(password)
            break
        except pexpect.TIMEOUT:
            value2 = 'Error: Password is a mandatory field'
            return render_template('home.html', value2 = value2)
    pobj.logfile = fout.buffer
    pobj.expect("Enter Source IP", timeout=10)
    pobj.sendline(Source_IP)
    pobj.expect("Enter Destination IP", timeout=10)
    pobj.sendline(Destination_IP)

    pobj.expect("Input ping repeat count", timeout=10)
    pobj.sendline(ping_count)
    pobj.expect('root@', timeout=600)



    #output = result.getvalue().decode
    fin = open("static/mylog.txt", "r")
    contents = []
    value1 = fin.read()

    pobj.close()

    fin.close()
    #print(result.getvalue())
    #pobj.close()

    # output = subprocess.check_output(["test.py", str(a)], shell = True).decode('UTF-8')
    #print(output)
    return render_template('traceout.html', value = value1)

@app.route('/kpi-utility/')
def kpi():
    output = ''
    return render_template('kpi.html',len = len(output))

@app.route('/kpi-1') # this is a job for GET, not POST
def kpi_1():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-1.csv',mimetype='text/csv',attachment_filename='ISP-ISIS_LDP_Missing_Report.csv',as_attachment=True)

@app.route('/kpi-2') # this is a job for GET, not POST
def kpi_2():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-2.csv',mimetype='text/csv',attachment_filename='ISP-ISIS_IPv6_Missing_Report.csv',as_attachment=True)

@app.route('/kpi-3') # this is a job for GET, not POST
def kpi_3():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-3.csv',mimetype='text/csv',attachment_filename='ISP-Description_Deviation_Backbone_Report.csv',as_attachment=True)

@app.route('/kpi-4') # this is a job for GET, not POST
def kpi_4():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-4.csv',mimetype='text/csv',attachment_filename='ISP-ISIS_Metric_B2B_Deviation_Report.csv',as_attachment=True)

@app.route('/kpi-5') # this is a job for GET, not POST
def kpi_5():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-5.csv',mimetype='text/csv',attachment_filename='MPLS-ISIS_Metric_Deviation_10G_Report.csv',as_attachment=True)

@app.route('/kpi-6') # this is a job for GET, not POST
def kpi_6():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-6.csv',mimetype='text/csv',attachment_filename='CEN-LDP-Missing-Report.csv',as_attachment=True)

@app.route('/kpi-7') # this is a job for GET, not POST
def kpi_7():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/Junos-ISP-Interface.csv',mimetype='text/csv',attachment_filename='JUNIPER-ISP-Interface.csv',as_attachment=True)

@app.route('/kpi-8') # this is a job for GET, not POST
def kpi_8():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-8.csv',mimetype='text/csv',attachment_filename='MPLS-BGP-Static-Deviation.csv',as_attachment=True)

@app.route('/nni-kpi-1') # this is a job for GET, not POST  #For NNI Reports 
def nni_kpi_1():
    now = datetime.datetime.now()
    dt_string_csv = now.strftime("%d%b%Y")
    try:
        return send_file('/home/Python_Tool/nniAuditScript/csvOutput/nniAuditDashboard'+dt_string_csv+'.csv',mimetype='text/csv',attachment_filename='MPLS-NNI-Audit-Report'+dt_string_csv+'.csv',as_attachment=True)
    except:
        return render_template('error.html',value = "File not found")
@app.route('/myapp')        
def myapp():
    return send_file('/home/Python_Tool/nniAuditScript/myapp.log',mimetype='text',attachment_filename='myapp.log',as_attachment=True)

@app.route('/db') # this is a job for GET, not POST
def db():
    return render_template('db.html')

@app.route('/dbapp') # this is a job for GET, not POST
def dbApp():
    return send_file('/data/vivek/mysql-gui-tools-noinstall-5.0-r17-win32.zip',mimetype='application/zip',as_attachment=True)

@app.route('/nniaudit/')
def nniaudit():
    output = ''
    return render_template('nniaudit.html', len = len(output))
@app.route('/nniaudit/', methods=['POST'])
def nniaudit_form():
    username = request.form['form']
    password = request.form['form1']
    deviceIp = request.form['form2'] #
    bundleId = int(request.form['form3'])
    command = "sudo python3 /home/Python_Tool/nniAuditScript/nniAuditScripttest.py -u %s -p '%s' -deviceip %s -bundleid %d"%(username,password,deviceIp,bundleId)
    try:list_services = subprocess.check_output(command,shell=True).decode()
    except subprocess.CalledProcessError as e: list_services = str(e.output.decode())
    if("➜" in list_services):
        return render_template('output.html',value = list_services,value2=deviceIp, value3="none")
    else:
        return render_template('output.html',value = list_services,value2=deviceIp, value3="block")
@app.route("/nnidiff/")
def nnidiff():
    return render_template('diff.html')


################## Feedback ############################

@app.route("/feedback/")  
def feedback():  
    return render_template("feedback.html")

@app.route('/feedback/',methods = ['POST'])
def feedback_form():
    if request.method == 'POST':
        msg="msg"
        name = request.form["Name"]
        id1 = request.form["id1"]
        Email = request.form["Email"]
        tool = request.form.get("tools", None)
        feedback = request.form["feedback"]
        suggestion = request.form["suggestion"]
        
        with sqlite3.connect("feedback.db") as con:
            cur = con.cursor()
            cur.execute("INSERT into feedback (Name,id,TOOL,feedback,Email,suggestion) values (?,?,?,?,?,?)",(name,id1,tool,feedback,Email,suggestion))
            print("execute")
            con.commit()
            print("commit")
            msg="Your feedback has been successfully submited."
            return render_template("feedback.html",msg=msg)  

####################################################Network Alarms Processing Tool###################################################
ALLOWED_EXTENSIONS = set(['xlsx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/tac3report')
def upload_form():
    return render_template('tac3opticsreport.html')

@app.route('/tac3report', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        get_file_names_and_remove() #To remove old files 
        #Check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        flash('File(s) successfully uploaded')
        return redirect('/tac3report')

@app.route('/processtac3report',methods=['POST'])
def process_file():
    file_type=file_in_directory()
    if file_type=="huawei":
        cmd = r"sudo python3.6 /data/PROJECTS/NAPT_Project/WebApp/huawei_excel_process.py"
    if file_type=="ciena":
        cmd = r"sudo python3.6 /data/PROJECTS/NAPT_Project/WebApp/ciena_excel_process.py"
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()  
    p_status = p.wait()
    print(output)
    if b"Report has been generated successfully" not in output:flash("Please upload or check the uploaded files.")
    if b"Report has been generated successfully" in output:flash("Report has been generated successfully.")

    return redirect('/tac3report')

@app.route('/downloadtac3report',methods=['POST'])
def download_file():

    date_object = str(datetime.date.today())
    location=(r"/data/PROJECTS/NAPT_Project/rawdata/inventory/")
    file_type=file_in_directory()
    if file_type=="huawei":
        path=(r"/data/PROJECTS/NAPT_Project/rawdata/processed_reports"+"/Huawei_Report"+"_"+date_object+".csv")
        return send_file(path,mimetype='text/csv',attachment_filename='Huawei_Processed_Report_'+date_object+'.csv',as_attachment=True)

    if file_type=="ciena":
        path=(r"/data/PROJECTS/NAPT_Project/rawdata/processed_reports"+"/Ciena_Report"+"_"+date_object+".csv")
        return send_file(path,mimetype='text/csv',attachment_filename='Ciena_Processed_Report_'+date_object+'.csv',as_attachment=True)

###############################################################TWAMP##########################################################

def allowed_file(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/twamp", methods=["GET", "POST"])
def twamp():
    f = []
    for (dirpath, dirnames, filenames) in os.walk("/home/Python_Tool/twampDataProcess/inputExcelFiles/"):
        f.extend(filenames)
        break
    print(f)
    if request.method == "POST":
        if request.files:
            file1 = request.files["file"]
            if file1.filename == "":
                session["message"] = "No filename"
                return redirect(request.url)

            if allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                file1.save(os.path.join(app.config["FILE_UPLOADS"], file1.filename))
                session["message"] =  "File saved"  
                return redirect(request.url)

            else:
                session["message"] = "That file extension is not allowed"
                return redirect(request.url)
    
    return render_template("twamp.html",f=f)

@app.route('/runtwamp/')
def runtwampn():
    return render_template("runtwamp.html")

# def stream_template(template_name, **context):                                                                                                                                                 
#     app.update_template_context(context)          #for dynamic output check commented code in outputFortwamp.html                                                                                                                                             
#     t = app.jinja_env.get_template(template_name)                                                                                                                                              
#     rv = t.stream(context)                                                                                                                                                                     
#     rv.disable_buffering()                                                                                                                                                                     
#     return rv                                                                                                                                                                                  

                                                                                                                                                     
# def generate(p,d):   
#     command = f"/home/Python_Tool/twampDataProcess/twampDataProcess.py"                                                                                                                                                                             
#     cmd = ["sudo", "python3", "-u",command, "-p",p,"-d",d]   # -u: don't buffer output
#     proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
#     for line in proc.stdout:
#         yield line.decode()
#         time.sleep(0.100)  

@app.route('/runtwamp/',methods=['POST'])
def runtwamp1():
    packet = request.form['form']
    days = request.form['form1']
    command = f"/home/Python_Tool/twampDataProcess/twampDataProcess.py"                                                                                                                                                                             
    cmd = ["sudo", "python3", "-u",command, "-p",packet,"-d",days]
    # rows = generate(packet,days)                                                                                                                                                                          
    # return Response(stream_template('outputFortwamp.html', rows=stream_with_context(rows)))
    try:list_services = subprocess.check_output(cmd).decode()
    except subprocess.CalledProcessError as e: list_services = str(e.output.decode())
    print("hello")
    return render_template('outputFortwamp.html')
   
   


if __name__ == '__main__':
    app.run(use_reloader= True,debug=True,host='0.0.0.0', port=8080)
