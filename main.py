from flask import Flask
import os
import sys
app = Flask(__name__)

@app.route("/")
def hello():
    filename = '/tmp/result'
    ret_str = "<!DOCTYPE html> <html><head><META HTTP-EQUIV=\"refresh\" CONTENT=\"60\"></head>"
    ret_str += "<body> Apporbit Postgres Data Migrator  <br/> <A HREF=\"javascript:history.go(0)\">Click to refresh the page</A> <br/>"
    if os.path.isfile(filename):
        with open(filename, 'r') as infile:
            str = infile.readline()
        if str == 'success':
            ret_str += "Data Migrator completed. Ready for Snapshot."
        elif str == 'failure':
            ret_str += "Data Migration failed. Click "
    else:
        ret_str += "Data Migration in progress. PLEASE DO NOT TAKE ANY SNAPSHOTS TILL IT FINISHES."

    ret_str += " <br/> Current Log status of Data Migration step: <br/> <pre>"
    try:
        with open('/tmp/dm.log', 'r') as fin:
                ret_str += " <pre>"
	        ret_str += fin.read()
                ret_str += " </pre>"
    except: 
	print "Unexpected error:", sys.exc_info()[0]
        pass
    ret_str += " </body> </html> "
    return ret_str


if __name__ == "__main__":
    app.run(host="0.0.0.0")
