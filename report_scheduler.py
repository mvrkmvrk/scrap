from config import CONF
from time import time
import os
from send_email import send_email
import csv

def merge_files(f1, f2, f3):
    with open(f1, 'rb') as csvfile:
        rows1 = csv.reader(csvfile, delimiter=',', quotechar='"')
        rows1 = [[r.lower().replace("\r", " ").replace("/", " ") for r in row] for row in rows1]

    with open(f2, 'rb') as csvfile:
        rows2 = csv.reader(csvfile, delimiter=',', quotechar='"')
        rows2 = [[r.lower().replace("\r", " ").replace("/", " ") for r in row] for row in rows2]
    
    f1_columns = len(rows1[0])
    f2_columns = len(rows2[0])
     
    with open(f3, 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        i = 0
        while True:
            if i < len(rows1) and i < len(rows2):
                merged_row = rows1[i] + rows2[i]
            elif i < len(rows1) and i >= len(rows2):
                merged_row = rows1[i] + [""]*f2_columns
            elif i >= len(rows1) and i < len(rows2):
                merged_row = [""]*f1_columns + rows2[i]
            else:
                break
            i += 1
        
            writer.writerow(merged_row)

def send_report():
    """ send updated csv links and then archive it for a fresh new report at the next interval
    combine vip info with links in a seperate column
    send email
        
    """
    
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    master_file = os.path.join(directory, "Masterlist database_CSV.csv")
    report_file = os.path.join(directory, "reports.csv")
    
    #if there is no reports file for the first time, then create it
    if not os.path.exists(report_file):
        open(report_file, "wb").write(",") #for two column report
    
    email_report_file = os.path.join(directory, "email_reports.csv")
    
    #archive or delete the old first
    if os.path.exists(email_report_file):
        os.rename(email_report_file, email_report_file.replace("email_reports.csv", "email_reports%s.csv" % (str(time()))))
        
    #merge
    merge_files(master_file, report_file, email_report_file)
    
    #send email
    send_email(email_report_file)
    
    #archive the reports file or delete it for new reports
    os.rename(report_file, report_file.replace("reports.csv", "reports_%s.csv" % (str(time()))))

def start_report_scheduler():
    #get gresh updated config
    current_time = time()
    # print "REPORT"
    # print current_time
    # print CONF.last_report_date_time
    # print CONF.report_interval
    # print current_time > (CONF.last_report_date_time + CONF.report_interval)
    if (CONF.last_report_date_time == -1) or (current_time > (CONF.last_report_date_time + CONF.report_interval)):
        send_report()
        CONF.last_report_date_time = current_time