# FMC_IPS_configuration


This tool shows how a script can create Snort IPS rules using web portal (Flask).  


  
# How to install:

  Copy these files into a working directory and make sure `requests` is an installed python library:
  
  `pip install requests` 
  
  Please install Flask python package as well: 
  
  `pip install flask`


  The  `fmc_config.py` contains the FMC paramters. 
  Please create a `local` intrustion rule group and assign a policy.
  This script will modify the the intrustion rules in this given group.


# How to use:

  Please run Flask python package from CLI: 
  
  `flask run`



