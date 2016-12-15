import psycopg2
from faker import Faker
import os
import traceback
import psycopg2.extras
import random
import string
import time
from threading import Condition
from subprocess import Popen, PIPE


def connect_db(dbname, user, host, passwd, port):
    conn = psycopg2.connect(
           "dbname='{0}' user='{1}' host='{2}' password='{3}' port='{4}'".format(dbname,
                                                                                user,
                                                                                host,
                                                                                passwd,
										port))
    return conn

def exec_cmd( cmd):
    results = []
    print "Executing Command: ", cmd
    process = Popen(cmd, bufsize=2048, stdin=PIPE, stdout=PIPE, shell=True)
    (child_stdin, child_stdout) = (process.stdin, process.stdout)
    if process.wait() != 0:
        print "There were some errors"
    for line in child_stdout:
        # the real code does filtering here
        line = line.rstrip()
        results.append(line)
        print line
    return results


def migrate():
    srcdb = os.getenv('SRC_POSTGRES_DB', 'appdb')
    srcuser = os.getenv('SRC_POSTGRES_USER', 'appuser')
    srcpasswd = os.getenv('SRC_POSTGRES_PASSWORD', 'apppassword')
    srcport = os.getenv('SRC_POSTGRES_PORT', '5432')
    srchost = os.getenv('SRC_POSTGRES_HOST', 'Please.Set.Hostname.Variable')

    passwd = os.getenv('POSTGRES_PASSWORD', 'jkshah')
    sysdb = os.getenv('POSTGRES_SYSDB', 'postgres')
    user = os.getenv('POSTGRES_USER', 'jkshah')
    passwd = os.getenv('POSTGRES_PASSWORD', 'postgres')
    host = os.getenv('APPORBIT_DBTIERNAME', 'postgres')
    print "Environment variables:"
    print "\nSource: ", srchost, srcport, srcdb, srcuser
    print "\nTo: ", host, "Using system cred:", sysdb, user, "\n"
    for i in range (0,3):
           try:
	      print "Attempt:", i
	      with connect_db(sysdb,user, host, passwd, 5432) as sysconn:
                with sysconn.cursor() as cur:
                  sysconn.autocommit = True  
                  cur.execute("DROP DATABASE IF EXISTS " + srcdb + ";")
                  #cur.execute("DROP OWNED BY " + srcdb + ";")
                  cur.execute("DROP USER IF EXISTS " + srcuser + ";")
                  cur.execute("CREATE USER " + srcuser + " WITH  PASSWORD '" + srcpasswd + "';")
                  #cur.execute("CREATE DATABASE " + srcdb + " WITH OWNER='" + srcuser + "' ;")

	      srconn = connect_db(srcdb,srcuser, srchost, srcpasswd, srcport)

              pg2pgcmd = "PGPASSWORD=" + srcpasswd + " pg_dump -Fc -b -h " + srchost +\
                         " -p " + str(srcport) + " -d " + srcdb + "  -U " + srcuser 
              pg2pgcmd += "| PGPASSWORD=" + passwd + " pg_restore -C -h " + host +\
                          " -p 5432 -d " + sysdb + "  -U " + user 
              exec_cmd(pg2pgcmd)

	      with connect_db(sysdb,user, host, passwd, 5432) as sysconn:
                with sysconn.cursor() as cur:
                  sysconn.autocommit = True  
                  cur.execute("ALTER DATABASE " + srcdb + " OWNER TO " + srcuser + " ;")
                  cur.execute("CHECKPOINT;")

              with open("/tmp/result", 'w') as outf:
                  outf.write("success")
	      break
           except:
		   print "FAILED ATTEMPT: to Migrate data on try:", i
                   traceback.print_exc()
	           if i ==2:
                      with open("result", 'w') as outf:
                          outf.write("failure")
		      break
	           time.sleep(30)
                   continue

if __name__ == '__main__':
    migrate()
