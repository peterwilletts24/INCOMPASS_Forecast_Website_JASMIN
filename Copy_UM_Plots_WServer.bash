#!/bin/bash 

_args="-a --ignore-existing"

latest_forecast_dir="/group_workspaces/jasmin2/incompass/public/restricted/MetUM/Images/Latest_Forecast/"
analysis_dir="/group_workspaces/jasmin2/incompass/public/restricted/MetUM/Images/Analysis/"

ftp_dir=''

rm $latest_forecast_dir*.png

last_dir=$(ls -rX $ftp_dir --ignore '*06Z' --ignore '*18Z*' | head -1)

# Latest Forecast

files=$(ls $ftp_dir$last_dir/*.png)


for f in $files

do

    if [ -f "$f" ]
    then
        rsync $_args "$f" "$latest_forecast_dir"
    else
        echo "Error $f file not found."
    fi
done
chmod 777 $latest_forecast_dir*.png

# Analysis

an_f=$(ls -t $ftp_dir/*/*_T+0_*.png)

for f in $an_f
do
    if [ -f "$f" ]
    then
        rsync $_args "$f" "$analysis_dir"
    
    else
        echo "Error $f file not found."
    fi
done
chmod 777 $analysis_dir*.png

/apps/canopy-1.5.2/bin/python /nfs/see-fs-01_users/eepdw/python_scripts/INCOMPASS_2015_Website/INCOMPASS_Jinja_Insert_Vars_gen_HTML.py
