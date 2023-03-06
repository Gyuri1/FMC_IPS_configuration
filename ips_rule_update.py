#
# FMC IPS rule updater
# 


# import required dependencies
import json


# FMC Credential file
import fmc_config

# FMC Class
from fmc_class import fmc



def deploy(posts, action):

    gid=2000
    sid=fmc_config.ips_rule_number
    revision=1

    target_domain = "Global"

    ips_policy_id =""
    ips_rulegroup_id =""

 
    print("Get FMC token:")
    yield "Get FMC token:\n"

    # Set variables for execution.
    # Make sure your credentials are correct.
    device   = fmc_config.host
    username = fmc_config.admin
    password = fmc_config.password

    # Initialize a new api object
    print("FMC authentication for this FMC:", device)
    yield "FMC authentication for this FMC:" 
    yield device+'\n'
    api = fmc(host = device, username=username, password=password)
    api.tokenGeneration(target_domain)
    print("Token received.")
    yield "Token received."
    print("Authorized domains:")
    for domain in api.domains["domains"]:
        print("Domain name:",domain["name"],"UUID:",domain["uuid"] )
        yield "Domain name:"+domain["name"]+"\n"
        yield "UUID:"+domain["uuid"]+"\n"


    print("Reading IPS policy ID:")
    yield "Reading IPS policy ID:\n"
    result=api.get_ips_policies()
    json_formatted_str = json.dumps(result, indent=2)
    #print(json_formatted_str)
    ips_policies = result["items"]
    for i in ips_policies:
        #print("name:",i["name"], UUID)
        if (i["name"] == fmc_config.ips_policy) and (i["type"] == "intrusionpolicy") :
          ips_policy_id = i["id"]
    print("Intrusionpolicy name:", fmc_config.ips_policy, "ips_policy_id:",ips_policy_id)
    yield "Intrusionpolicy name:"+fmc_config.ips_policy+"\n"
    yield "ips_policy_id:"+ips_policy_id+"\n"
    

    print("Reading IPS rule group ID:")
    yield "Reading IPS rule group ID:\n"
    result=api.get_ips_rulegroup(ips_policy_id)
    json_formatted_str = json.dumps(result, indent=2)
    #print(json_formatted_str)
    ips_rulegroups = result["items"]
    for i in ips_rulegroups:
        #print("name:",i["name"], UUID)
        if (i["name"] == fmc_config.ips_rulegroup) and (i["type"] == "IntrusionRuleGroup") :
          ips_rulegroup_id = i["id"]
    print("Intrusion rulegroup name:", fmc_config.ips_rulegroup, "ips_rulegroup_id:",ips_rulegroup_id)
    yield "Intrusion rulegroup name:"+ fmc_config.ips_rulegroup+"\n"
    yield "ips_rulegroup_id:"+ips_rulegroup_id+"\n"
 

    # loop for IPS rules

    k=0
    for i in posts:

        s=''
        for j in str(i['title']):
          s+= j+'|00|'
         
        
        rule= action + " tcp " + str(i['content']) +' any -> any 1433' \
         + ' (msg:\"BAD SQL query detected\";content:\"' \
         + str(s) + '\"; sid:'+ str(sid+k)+ "; gid:"+str(gid)+"; rev:"+str(revision)+"; )"

        print("rule:",rule) 
        yield "\n"
        data={
            "type": "IntrusionRule",
            "name": str(gid)+":"+str(sid),
            "gid": gid,
            "sid": sid+k,
            "revision": revision,
            "msg": "BAD SQL query detected!",
            "ruleData": rule,
            "ruleGroups": [
              {
               "name": fmc_config.ips_rulegroup,
                "id": ips_rulegroup_id,
                "type": "IntrusionRuleGroup"
                }
            ]
        }      


        print("Reading the rule:")
        yield "Reading the rule:\n"
        result=api.get_ips_rule(str(sid+k))
        json_formatted_str = json.dumps(result, indent=2)
        #print(json_formatted_str)

        if "items" in result:
          print("THIS IS A KNOWN RULE, SCRIPT WILL REWRITE IT!")
          yield "THIS IS A KNOWN RULE, SCRIPT WILL REWRITE IT!\n"
          ips_id=result["items"][0]["id"]
          print("IPS ID:",ips_id )
          yield "IPS ID:"+ips_id+"\n"

          print("Deleting the rule:")
          yield "Deleting the rule:\n"
          json_formatted_str = json.dumps(api.delete_ips_rule(str(ips_id)), indent=2)
          #print(json_formatted_str)

        print("Updating the Rule: ")
        yield "Updating the Rule: \n"
        json_formatted_str = json.dumps(api.put_ips_rule(data), indent=2)
        #print(json_formatted_str)

        print("SID:",sid+k)
        yield "SID:"+str(sid+k)+"\n"
        k=k+1
    

    print("GET deployabledevices ")
    yield "GET deployabledevices\n"
    result=api.get_deployabledevices()
    json_formatted_str = json.dumps(result, indent=2)
    print(json_formatted_str)


    if 'items' in result: 
      deploy_version=result["items"][0]["version"]
      device_name=result["items"][0]["name"]

      print("GET devices ")
      yield "GET devices \n"
      result=api.get_devices()
      json_formatted_str = json.dumps(result, indent=2)
      print(json_formatted_str)
      
      for i in result['items']:
      	if device_name == i["name"]:
      		device_uuid = i["id"]	

    else:
      print("ERROR: no device")
      exit()


    print("device UUID", device_uuid)
    yield "device UUID"+ device_uuid +"\n"

    deploy_post={
      "type": "DeploymentRequest",
      "version": deploy_version,
      "forceDeploy": False,
      "ignoreWarning": True,
       "deviceList": [ device_uuid ],
      "deploymentNote": "yournotescomehere"
    }

    print("Deployement: started ... ")
    yield "Deployement: started... \n"
    result=api.deploymentrequests(deploy_post)
    json_formatted_str = json.dumps(result, indent=2)
    print(json_formatted_str)
    yield json_formatted_str+"\n"
    yield "Deployment : done! \n"
    return True
