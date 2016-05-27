import glob
import numpy as np
import re

import os
import commands
#from flask import Flask
#app = Flask(__name__)


import pdb

# Directories where forecast plots are - seems easiest, and most future proof to use filenames rather than directory structure... The idea is that with regular expression pattern matching, all the info to generate the web pages comes from the file name.

forecast_plot_search = '/group_workspaces/jasmin2/incompass/public/restricted/MetUM_Monitoring/project/'
# Relative location of files, from forecast_plot_search
sfiles = '*/*/*'

# These three lines search for forecasts. 'T0' may need to be changed
# depending on the file naming

files = np.array(glob.glob(forecast_plot_search+sfiles))
f_inits = np.where(['T0' in f for f in files])[0]
forecasts = np.unique([re.search(r'\d{8}_\d\dZ', os.path.basename(f)).group() for f in files[f_inits]])

# Where the template html files are

script_path = '/home/users/pdwilletts/web_page_python_scripts/'
TEMPLATE_FILE_f = "%sINCOMPASS_Jinja_Template_Forecast_regions.html" % script_path
TEMPLATE_FILE_an = "%sINCOMPASS_Jinja_Template_Analysis.html" % script_path

# Where html files will be, for viewing in browser
web_page_dir = '/group_workspaces/jasmin2/incompass/public/restricted/MetUM/'

relative_path = os.path.relpath(forecast_plot_search , web_page_dir)+'/'
#pdb.set_trace()

def GetParams(search_for, forecast_plot_search):

    '''
    Splits globbed filenames by '_',  and gets various info from them
    This may need to be edited for future use
    '''

    paths = [os.path.relpath(fn, forecast_plot_search) for fn in  glob.glob(search_for)]

    rel_paths = [fn.replace(re.search(r'_\d{8}_\d{2}Z_T\d+\S*', fn).group(), "") for fn in paths]
    regions_full = [fn.replace(re.search(r'\S*_T\d+', fn).group(), "").strip('.png') for fn in paths]
    
    regions = np.unique(regions_full)

    
    diags_full = np.array([os.path.basename(d) for d in rel_paths])
    #pdb.set_trace()

    #diags = np.unique(diags_full)
    diags_full = np.array([''.join([d, r]) for d, r in zip(diags_full, regions_full)])
    diags_reg = np.unique(diags_full)
    
    diags=[]
    for d in diags_reg:
        for r in regions[regions!='']:

            d = d.replace(r, "")
        diags.append(d)

    #pdb.set_trace()    
    dates_times = np.array([re.search(r'_\d{8}_\d{2}Z_T\d+', fn).group() for fn in paths])

    #pdb.set_trace()
    
    tpluss_full = np.array([re.search(r'T\d+', f).group().strip('T') for f in dates_times])    

    #pdb.set_trace()

    tpluss = np.sort(np.unique(np.array(tpluss_full)).astype(int)).astype(str)

    fdates = np.array([re.search(r'\d{8}', f).group() for f in dates_times])    
    fhours = np.array([re.search(r'\d\dZ', f).group() for f in dates_times])    

    return fdates, fhours, tpluss_full, tpluss, diags_full, diags, diags_reg, rel_paths, regions_full
    
# Now for html page generation

import jinja2

templateLoader = jinja2.FileSystemLoader( searchpath="/" )
templateEnv = jinja2.Environment( loader=templateLoader )


#Forecasts

template = templateEnv.get_template( TEMPLATE_FILE_f )

#pdb.set_trace()

for forecast in forecasts:

    #pdb.set_trace()

    fdates, fhours, tpluss_full, tpluss, diags_full, diags, diags_reg, rel_paths, regions_full \
                                                                           = GetParams('%s*/%s/*' 
                                                                           % (forecast_plot_search, forecast), 
                                                                           forecast_plot_search)

    templateVars = { "fdates" : list(fdates),
                     "fhours" : list(fhours),
                 "tpluss_full" : list(tpluss_full),
                "rel_paths":list(rel_paths),
                 "diags_full" : list(diags_full),
                     "regions_full" : list(regions_full),
                     "tpluss":list(tpluss),
                         "diagnostics":list(diags_reg),
                         "diags":list(diags),
                "image_dir":relative_path
               }

    outputText = template.render( templateVars )

    with open("%sForecast_%s.html" %(web_page_dir, forecast), "wb") as fh:
        fh.write(outputText)

# Analysis

template = templateEnv.get_template( TEMPLATE_FILE_an )

fdates, fhours, tpluss_full, tpluss, diags_full, diags, diags_reg, rel_paths, regions_full \
                                                                           = GetParams('%s*/*/*T0*' 
                                                                           % (forecast_plot_search), 
                                                                           forecast_plot_search)

fdates_full = [('_').join([d,h]) for d,h in zip(fdates,fhours)]

pdb.set_trace()
templateVars = {"rel_paths":list(rel_paths),
                 "diags_full" : list(diags_full),
                     "regions_full" : list(regions_full),
                     "fdates_un":list(np.unique(fdates_full)),
                   "fdates_full":fdates_full,
                         "diagnostics":list(diags_reg),
                         "diags":list(diags),
                "image_dir":relative_path
               }

outputText = template.render( templateVars )
    
with open("%s/Analysis.html" %(web_page_dir), "wb") as fh:
        fh.write(outputText)


