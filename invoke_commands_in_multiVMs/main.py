#Importing required modules
import os
import csv
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential
import logging
# Acquire a credential object using CLI-based authentication.
subscription_id = os.environ['ARM_SUBSCRIPTION_ID']
subscription_id = os.environ['ARM_SUBSCRIPTION_ID']
credentials = ClientSecretCredential(
    client_id=os.environ['ARM_CLIENT_ID'],
    client_secret=os.environ['ARM_CLIENT_SECRET'],
    tenant_id=os.environ['ARM_TENANT_ID']
)
compute_client = ComputeManagementClient(credentials,subscription_id)
#Variables
run_command_parameters = {
    'command_id': 'RunShellScript', # For linux, don't change it
    'script': ['sudo apt list --installed']
    }
#to read CSV file
with open("resources/AzureVirtualMachines.csv",newline='',encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print (f"Executing Commands on {row['NAME']}")
        poller = compute_client.virtual_machines.begin_run_command(
        resource_group_name = row['RESOURCE GROUP'],
        vm_name = row['NAME'],
        parameters = run_command_parameters,
        logging_enable = True);
        result = poller.result()
        print (result.value[0].message)