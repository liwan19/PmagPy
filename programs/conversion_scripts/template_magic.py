#!/usr/bin/env python
"""
EXAMPLE DOCSTRING for script

NAME
    template_magic.py

DESCRIPTION
    converts TEMPLATE format files to MagIC format files

SYNTAX
    template_magic.py [command line options]

OPTIONS
    -h : prints the help message and quits.
    -usr : colon delimited list of analysts (default : "")
    -f : magnetometer file path
"""
import os,sys
import pmagpy.pmag as pmag
import pmagpy.new_builder as nb
from pandas import DataFrame

def main(**kwargs):
    """
    EXAMPLE DOCSTRING for function (you would usually put the discription here)

    Parameters
    -----------
    user : colon delimited list of analysts (default : "")

    Returns
    -----------
    type - Tuple : (True or False indicating if conversion was sucessful, meas_file name written)
    """

    #get parameters from kwargs.get(parameter_name, default_value)
    user = kwargs.get('user', '')
    magfile = kwargs.get('magfile')

    #do any extra formating you need to variables here

    #open magfile to start reading data
    try:
        infile=open(magfile,'r')
    except Exception as ex:
        print("bad file path: ", magfile)
        return False, "bad file path"

    #Depending on the dataset you may need to read in all data here put it in a list of dictionaries or something here. If you do just replace the "for line in infile.readlines():" bellow with "for d in data:" where data is the structure you put your data into

    #define the lists that hold each line of data for their respective tables
    SpecRecs,SampRecs,SiteRecs,LocRecs,MeasRecs=[],[],[],[],[]

    #itterate over the contence of the file
    for line in infile.readlines():
        MeasRec,SpecRec,SampRec,SiteRec,LocRec={},{},{},{},{}

        #extract data from line and put it in variables

        #fill this line of the Specimen table using above variables
        if specimen!="" and specimen not in map(lambda x: x['specimen'] if 'specimen' in x.keys() else "", SpecRecs):
            SpecRec['analysts']=user
            SpecRecs.append(SpecRec)
        #fill this line of the Sample table using above variables
        if sample!="" and sample not in map(lambda x: x['sample'] if 'sample' in x.keys() else "", SampRecs):
            SampRec['analysts']=user
            SampRecs.append(SampRec)
        #fill this line of the Site table using above variables
        if site!="" and site not in map(lambda x: x['site'] if 'site' in x.keys() else "", SiteRecs):
            SiteRec['analysts']=user
            SiteRecs.append(SiteRec)
        #fill this line of the Location table using above variables
        if location!="" and location not in map(lambda x: x['location'] if 'location' in x.keys() else "", LocRecs):
            LocRec['analysts']=user
            LocRecs.append(LocRec)

        #Fill this line of Meas Table using data in line
        MeasRec['analysts']=user
        MeasRecs.append(MeasRec)

    #open a Contribution object
    con = nb.Contribution(output_dir_path,read_tables=[])

    #Create tables
    con.add_empty_magic_table('specimens')
    con.add_empty_magic_table('samples')
    con.add_empty_magic_table('sites')
    con.add_empty_magic_table('locations')
    con.add_empty_magic_table('measurements')

    #turn above data structures into something that can be put in a contribution
    con.tables['specimens'].df = DataFrame(Specs)
    con.tables['samples'].df = DataFrame(Samps)
    con.tables['sites'].df = DataFrame(Sites)
    con.tables['locations'].df = DataFrame(Locs)
    Fixed=pmag.measurements_methods3(MeasRecs,noave) #figures out method codes for measuremet data
    con.tables['measurements'].df = DataFrame(Fixed)

    #write to file
    con.tables['specimens'].write_magic_file(custom_name=spec_file)
    con.tables['samples'].write_magic_file(custom_name=samp_file)
    con.tables['sites'].write_magic_file(custom_name=site_file)
    con.tables['locations'].write_magic_file(custom_name=loc_file)
    con.tables['measurements'].write_magic_file(custom_name=meas_file)

    return True, meas_file

def do_help():
    """
    returns help string of script
    """
    return __doc__

#this if statement insures it's being called from the commandline
if __name__ == "__main__":
    kwargs = {} #create a key word argument dictionary
    if "-h" in sys.argv:
        help(__name__)
        sys.exit()
    if "-usr" in sys.argv: #check for flag
        ind=sys.argv.index("-usr") #find flag
        kwargs['user']=sys.argv[ind+1] #get data and store in dictionary
    if '-f' in sys.argv:
        ind=sys.argv.index("-f")
        kwargs['magfile']=sys.argv[ind+1]

    main(**kwargs)