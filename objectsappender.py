from panos import panorama
from panos import policies
import csv
import getpass
print("$$$$__O B J E C T S__A P P E N D E R__$$$$\nVersion-1.0\n")
#Prompting for Panorama hostname, username and password
pan_hostname = input("Please enter the hostname of Panorama: ")
username = input("Please enter your username:  ")
password = getpass.getpass("Please enter your password:  ")
#Connecting to the Panorama
pano = panorama.Panorama(hostname=pan_hostname, api_username=username, api_password=password)
#Fetching all the Device Groups in the Panorama
device_groups = panorama.DeviceGroup.refreshall(pano)
#Creating 2 empty lists for each column of the csv file
old_objects = []
new_objects = []
#Opening file is read mode
objfile = open('objects.csv', 'r')
#Creating a temp list of all the values in the csv file.
temp_list = csv.reader(objfile)
#Appending the values to its respective lists
for obj in temp_list:
    old_objects.append(obj[0])
    new_objects.append(obj[1])
#initializing a value which acts as a pointer to reference the values in the list new_objects
pointer = 0
output_file = open('output.csv', 'w')
print("Device_Group,Security_Rule,Existing_Object,New_object,Appended_in(Source or Destination)", file = output_file)
output_file.flush()
for old_object in old_objects:
    for device_group in device_groups:
        dg = panorama.DeviceGroup(device_group)
        pano.add(dg)
        rulebase = policies.PreRulebase()
        dg.add(rulebase)
        SecRules = policies.SecurityRule.refreshall(rulebase)
        new_object = new_objects[pointer]
        for SR in SecRules:
            if (old_object in SR.source and new_object not in SR.source) and (old_object in SR.destination and new_object not in SR.destination):
                SR.source.append(new_object)
                SR.destination.append(new_object)
                SR.apply()
                print("{dg},{SR},{old_object},{new_object},Source and Destination", file = output_file)
                output_file.flush()
            elif old_object in SR.source and new_object not in SR.source:
                SR.source.append(new_object)
                SR.apply()
                print("{dg},{SR},{old_object},{new_object},Source", file = output_file)
                output_file.flush()
            elif old_object in SR.destination and new_object not in SR.destination:
                SR.destination.append(new_object)
                SR.apply()
                print("{dg},{SR},{old_object},{new_object},Destination", file = output_file)
                output_file.flush()
            else:
                continue
    pointer = pointer + 1
output_file.close()
