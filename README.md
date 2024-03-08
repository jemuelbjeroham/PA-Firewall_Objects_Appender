# PA-Firewall_Objects_Appender
Python Script that appends new firewall objects to the security rules where the respective existing objects reside.
This script only works on Palo Alto Panorama and appends only if the new firewall objects already exist on the Panorama.

The Script takes the list of old and new objects provided in the objects.csv file, appends the new objects in the security rules where the respective old objects are called, and finally generates an output file that lists the Security Rules the script has modified.
