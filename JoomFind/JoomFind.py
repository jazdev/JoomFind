#!/usr/bin/env python

import sys,  re,  urllib,  urllib2,  string, time, os
from urllib2 import Request, urlopen, URLError, HTTPError
from urlparse import urlparse

joomla_version="undefined"   #used for joomla veersin info

provided_url=""   #the selected provided url

verbose_flag = 0 # If set to 1, prints verbose information

default_input_path = "" # The default input file path
 
default_output_path = "" # The default output file path

if os.name == "nt":
    path_slash = "\\"
else:
    path_slash = "/"

# Prints usage
def print_usage():
    """
	print_usage()
	
	Prints help screen and exits.

    """
    print ""
    print ""
    print " JoomFind v0.1"
    print ""
    print " Script made by Jasdev Singh"
    print ""
    print "  This script is made only for educational and offline self-testing  "
    print "  purposes. The creator is not responsible or accountable for any  "
    print "  damage or loss caused that you perform with this script. "
    print ""
    print "  Usage example:"
    print '\tpython joomfind.py -f filepath | -v'
    print ""
    print "        Put URL(s) to scan in a newline delimited file"
    print "        URL(s) must point to homepage of the CMS "
    print ""
    print "  Options:"
    print "    -f filename    (specify input file)"
    print "    -v, --verbose  (show detailed output)"
    print "    --help         (displays this help text)"
    print ""
    return


# Testing if URL is reachable, with error handling
def test_url():
    """
	test_url()
	
	Checks whether URL is rechable. Prints relevant infomation.

    """
    global provided_url
    global verbose_flag
    # extracting url
    provided_url = urlparse(provided_url).scheme+"://"+urlparse(provided_url).netloc
    print provided_url    
    if verbose_flag: print "\t[.] Checking if connection can be established...",# + provided_url
    try:
        response = urllib2.urlopen(provided_url)
        
    except HTTPError,  e:
        if verbose_flag: print "[!] Failed"
        return 0
    except URLError,  e:
        if verbose_flag: print "[!] Failed"
        return 0
    else:
        valid_target = 1
        if verbose_flag: print "Success"
        return 1

# Scans for the HTML meta tag information
def scan_target_metatag():
    """
	scan_target_metatag()
	
	Scans the meta-tag of the website. 

	The meta-tag has information that can lead to the detection of Joomla.

    """
    target_meta_url=provided_url+"/index.php"
    if verbose_flag: print "\t[.] Trying to access meta tag information...", #+ target_meta_url
    try:
    	response = urllib2.urlopen(target_meta_url)
    	html = response.read(2000)
    	#print html
    	# Now extract the interesting information
    	get_metatag = string.find(html,  "Joomla! - Open Source Content Management")

    	# If  the target is not vulnerable exit
    	if get_metatag == -1:
            meta_flag=0
            if verbose_flag: print "Failed"
        else:
            meta_flag=1
            if verbose_flag: print "Success"
        #print "meta flag="+str(meta_flag)
        return meta_flag

    except:
	if verbose_flag: print "Failed"

# Tests whether the URL has a '/administrator' login page
def scan_admin_url():
    """
	scan_admin_url()
	
	Scans the administrator URL of the website. 

	The administrator URL, if reachable, is a clue that Joomla is being used.

    """
    target_admin_url=provided_url+"/administrator/index.php"
    if verbose_flag: print "\t[.] Trying to access admin login page...", #+ target_admin_url
    try:
        response = urllib2.urlopen(target_admin_url)
    except HTTPError,  e:
        admin_flag=0
        #print "admin flag="+str(admin_flag)
        if verbose_flag: print "Failed"
        return admin_flag
    else:
        admin_flag=1
        #print "admin flag="+str(admin_flag)
        if verbose_flag: print "Success"
        return admin_flag

# Scans content of 'com_content' component
def scan_com_content():
    """
	scan_com_content()
	
	Scans the content.xml file of the default component of the website. 

	The content.xml file, if readable, is a clue that Joomla is being used.

    """
    target_com_content=provided_url+"/administrator/components/com_content/content.xml"
    if verbose_flag: print "\t[.] Trying to access com_content component...", #+ target_com_content
    try:
        response = urllib2.urlopen(target_com_content)
        html = response.read()
        get_com = string.find(html,  "Joomla")
    except HTTPError,  e:
        com_component_flag=0
        #print "com_component flag="+str(com_component_flag)
        if verbose_flag: print "Failed"
        return com_component_flag
    else:
        if get_com==-1:
            com_component_flag=0
            if verbose_flag: print "Failed"
        else:
            com_component_flag=1
            if verbose_flag: print "Success"
        #print "com_component flag="+str(com_component_flag)
        return com_component_flag

# Scans the robots.txt file
def scan_robots_txt():
    """
	scan_robots_txt()
	
	Scans the robots.txt file of website. 

	The robots.txt file, if readable, has clues that Joomla is being used.

    """
    target_robots_txt=provided_url+"/robots.txt"
    if verbose_flag: print "\t[.] Trying to access robots.txt file...",#+target_robots_txt
    try:
        response = urllib2.urlopen(target_robots_txt)
        html = response.read()
        get_robots = string.find(html,  "Joomla")
    except HTTPError,  e:
        robots_flag=0
        #print "robots flag="+str(robots_flag)
        if verbose_flag: print "Failed"
        return robots_flag
    else:
        if get_robots==-1:
            robots_flag=0
            if verbose_flag: print "Failed"
        else:
            robots_flag=1
            if verbose_flag: print "Success"
        #print "robots flag="+str(robots_flag)
        return robots_flag

# Scans the htaccess.txt file
def scan_htaccess():
    """
	scan_htaccess()
	
	Scans the htaccess file of website. 

	The htaccess file, if readable, has clues that Joomla is being used.

    """
    target_htacess=provided_url+"/htaccess.txt"
    if verbose_flag: print "\t[.] Trying to access htaccess file...",#+target_htacess
    try:
        response = urllib2.urlopen(target_htacess)
        html = response.read()
        get_htaccess = string.find(html,  "Joomla")
    except HTTPError,  e:
        htaccess_flag=0
        #print "htaccess flag="+str(htaccess_flag)
        if verbose_flag: print "Failed"
        return htaccess_flag
    else:
        if get_htaccess==-1:
            htaccess_flag=0
            if verbose_flag: print "Failed"
        else:
            htaccess_flag=1
            if verbose_flag: print "Success"
        #print "htaccess flag="+str(htaccess_flag)
        return htaccess_flag

# Scans the system.css file    
def scan_system_css():
    """
	scan_system_css()
	
	Scans the system.css file of website. 

	The system.css file, if readable, has clues that Joomla is being used.

    """
    pass

# Scans the MooTools.js file
def scan_mootools():
    """
	scan_mootools()
	
	Scans the mootools.js file of website. 

	The mootools.js file, if readable, has clues that Joomla is being used.

    """
    target_mootools=provided_url+"/media/system/js/mootools-more.js"
    if verbose_flag: print "\t[.] Trying to access MooTools file...", #+ target_mootools
    try:
        response = urllib2.urlopen(target_mootools)
        html = response.read(3300)
        #print html
        get_mootools = string.find(html,  'MooTools.More={version:"1.4.0.1"')
    except HTTPError,  e:
        mootools_flag=0
        #print "mootools flag="+str(mootools_flag)
        if verbose_flag: print "Failed"
        return mootools_flag
    else:
        if get_mootools==-1:
            mootools_flag=0
            if verbose_flag: print "Failed"
        else:
            mootools_flag=1
            if verbose_flag: print "Success"
            joomla_version="2.x or 3.x"
        #print "mootools flag="+str(mootools_flag)
        return mootools_flag    

# Scans the en-GB.xml file
def scan_engb_ini():
    """
	scan_engb_ini()
	
	Scans the en-GB.ini file of website. 

	The en-GB.ini file, if readable, has clues that Joomla is being used.

    """
    target_engb=provided_url+"/language/en-GB/en-GB.xml"
    if verbose_flag: print "\t[.] Trying to access en-GB file...", #+ target_engb
    try:
        response = urllib2.urlopen(target_engb)
        html = response.read(200)
        #print html
        t1 = string.find(html,  '<version>')
        target_engb = html[t1+9:t1+14]
        
    except HTTPError,  e:
        engb_flag=0
        #print "engb flag="+str(engb_flag)
        if verbose_flag: print "Failed"
        return engb_flag
    else:
        if t1==-1:
            engb_flag=0
            if verbose_flag: print "Failed"
        else:
            engb_flag=1
            if verbose_flag: print "Success"
            global joomla_version
            joomla_version=target_engb
        #print "engb flag="+str(engb_flag)
        return engb_flag 

# Computes the result of the scans
def compute_result(a,b,c,d,e,f,g):
    """
	compute_result()
	
	Computes the final result. 

    """
    if (a or b or c or d or e or f or g)and ((a+b+c+d+e+f+g)>=3):
        return 1
    else:
        return 0

# Reads URL's from an input file and processes them
def process_from_file():
    """
	process_from_file()
	
	Starts processing the URL's from the input file. 

    """
    global default_input_path
    print "JoomFind v 1.0"
    print "\n\nTrying to read URL(s) form " + default_input_path + " file...\n"
    try:
        if not default_input_path:
            f = open("urls.txt")
        else:
            f=open(default_input_path)
        cwd=os.getcwd()
        file_path = cwd + path_slash + f.name
	# extracting url's to list from file
        start_urls = [url.strip() for url in f.readlines() if url[0] not in ['#',' ',"\n"]]
        if not start_urls:
            print "File is empty. Add some URL(s) first.\n"
            f.close()
            return 0
    except:
        print "File not found. Make sure it exists.\n"
        return 0
    #print start_urls
    
    num=str(len(start_urls))
    print "Found " + num + " URL(s) on " + time.asctime(time.localtime(time.time())) + "\n"
    
    of=open(default_output_path,'a+')
    of.write("\n\n\tScanning " + num + " URL(s) ")
    of.write("\n\n\tDate\Time : " + time.asctime(time.localtime(time.time())) )
    of.write("\n\n\tInput file path : " + default_input_path + "\n\n")
    of.close()
    
    for url in start_urls:
        global provided_url
        provided_url=url
        print "\nWorking on URL " + str(start_urls.index(url)+1) + ": " + provided_url
        processing()
    print "\nAll done! Check '" + default_output_path +"' file for results.\n"    


# Calls other scans and writes results to output file
def processing():
    """
	processing()
	
	Calls other helper functions. 

    """
    err=test_url()
    of=open(default_output_path,'a+')
    if err!=0:           
        metaf=scan_target_metatag()
        adminf=scan_admin_url()
        comf=scan_com_content()
        robotsf=scan_robots_txt()
        htf=scan_htaccess()
        moof=scan_mootools()
        engbf=scan_engb_ini()
        result=compute_result(metaf,adminf,comf,robotsf,htf,moof,engbf)
        if result==1:
            #print "THE TARGET IS USING JOOMLA CMS"
            #print "Joomla version is " + joomla_version
            of.write("\nJOOMLA USED (version : " + joomla_version + ") --> " + provided_url + "\n")
        else:
            #print "JOOMLA NOT USED"
            of.write("\nJOMLA NOT USED --> " + provided_url + "\n")
    else:
        of.write("\nBAD URL --> " + provided_url + "\n")
    of.close()
    return 0

# main method
def main():
    """
	main()
	
	Starting point of program execution. 

    """
# Checking if argument was provided
    if len(sys.argv) <=1:
        print_usage()
        sys.exit(1)
        
    for arg in sys.argv:
        # Checking if help was called
        if arg == "-h" or arg == "--help":
            print_usage()
            sys.exit(1)
            
        # Checking for verbose mode   
        if arg == "-v" or arg == "--verbose":
            global verbose_flag
            verbose_flag=1

        # Checking for input file
        if arg == "-f" or arg == "--file":
            global default_input_path
            global default_output_path
            default_input_path = sys.argv[2]
            default_output_path=default_input_path[:-4] + "_results.txt"

        #if arg == "-u" or arg == "--url":
        #    input_url = sys.argv[2]
	    
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
        
    process_from_file()


if __name__=="__main__":
    main()
    
#EOF
