# FMC_IPS_configuration


This tool shows how a script can create and modify Snort 3 IPS rules using a web portal (python Flask) application.  

  
# How to install:

  Copy these files into a working directory and make sure `requests` is an installed python library:
  
  `pip install requests` 
  
  Please install Flask python package as well: 
  
  `pip install flask`


  The `fmc_config.py` file contains the FMC paramters.  
  Please create a `local` intrustion rule group (like: `ips_rulegroup`) and   
  assign to an intrustion policy (like: `ips_policy`).  
  
  This script will modify the the intrustion rules in this given intrusion group.  


# How to use:

  Please run Flask python package from CLI: 
  
  `flask run`

Visit this web page using your browser: http://127.0.0.1:5000/  

![Flask GUI](/flask_gui.jpg?raw=true "Flask GUI")


Python Flask based script's menu:  
- IPSApp: It shows the configured entries. 
- Create: You can add new entry. 
- Settings: FMC configuration.   
- Deploy: The script deploys the current rules into FMC using `block` action.  
- Reset: The script deploys the current rules into FMC using `alert` action.  

