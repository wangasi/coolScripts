#!/usr/bin/env python
import sys,types
import getopt
import json,time

def Usage():
    print 'AutoCreateFile.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-o, --output: input an output verb'
    print '--desc: description for the file will create'
    #print '--fre: another test option'
def Version():
    print 'AutoCreateFile.py 0.0.1'

def GetTextFromConfig(path,desc):
	name = path[:-3]
	content = "/**\n * @FileName: "+name+"\n * @Description: "+desc+"\n"
	textDict = []
	try:
		fp = open("config.json", 'r')
		textStr  = fp.read()
		try: 
			textDict = json.loads(textStr)
		except Exception, e:
			print "error: config.json may got wrong type, please check your config file.\n",Exception,":",e
		finally:
			if len(textDict) < 1:
				print "config.json has errors, cause this..."
				sys.exit(2)
			header = textDict["header"]
			for eatch in header:
				content += " * @"+eatch+": " + header[eatch] + "\n"

		content += " * @Create: " + time.strftime('%Y-%m-%d %H:%M:%S') + "\n */\n"
		content += "import React, { Component } from \'react\';\n"
		content += "import {\n  AppRegistry,\n  Text,\n  View\n} from \'react-native\';\n\n"
		content += "export default class "+ name.capitalize()+" extends Component {\n"
		content += "\tconstructor(props) {\n\t\tsuper(props);\n\t}\n\n"
		body = textDict["body"]
		for eatch in body:
			if body[eatch]:
				content += "\t"+eatch+"() {\n\n\t}\n\n"
		content += "\trender() {\n\t\treturn (\n\t\t\t<View>\n\t\t\t</View>\n\t\t);\n\t}\n}"
	except Exception, e:
		print "error: file create error,check your file name."
	finally:
		fp.close()
		return content

def CreateFile(fileName, fileDesc):
	print 'fileName: %s'%fileName,' fileDesc: %s'%fileDesc
	if ".js" not in fileName:
		fileName = fileName + ".js"
	textContent = GetTextFromConfig(fileName, fileDesc)
	output = open(fileName, 'w+')
	output.write(textContent)
	output.close()

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hvo:', ['output=', 'desc='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)

    fileName = ""
    fileDesc = ""
    for opt, value in opts:
        if opt in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif opt in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif opt in ('-o', '--output'):
            fileName = value
        elif opt in ('--desc',):
            fileDesc = value
        else:
            print 'unhandled option'
            sys.exit(3)
    CreateFile(fileName, fileDesc)

if __name__ == '__main__':
    main(sys.argv)
