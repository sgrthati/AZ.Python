#Variables
RG_NAME = "SRI"
RG_LOCATION = "eastus"
NO_OF_VMS = 2
VNET_NAME = (f"{RG_NAME}-VNet")
SUBNET_NAME = (f"{VNET_NAME}-SUBNET1")
print ("importing Required modules")
#importing required modules
import os
from azure.core.exceptions import ( ClientAuthenticationError,
    HttpResponseError,
    ServiceRequestError,
    ResourceNotFoundError,
    AzureError)
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from resources.rg import rg_creation
from resources.vnet import vnet_creation
from resources.subnet import subnet_creation
from resources.pip import pip_creation
from resources.nic import nic_creation
from resources.vm import vm_creation

def main():
    #creating VNet
    print ("setting up azure API Client")
    # Set up the Azure API client
    subscription_id = os.environ['ARM_SUBSCRIPTION_ID']
    credentials = ClientSecretCredential(
        client_id=os.environ['ARM_CLIENT_ID'],
        client_secret=os.environ['ARM_CLIENT_SECRET'],
        tenant_id=os.environ['ARM_TENANT_ID']
    )
    compute_client = ComputeManagementClient(credentials, subscription_id)
    resource_client = ResourceManagementClient(credentials, subscription_id)
    network_client = NetworkManagementClient(credentials, subscription_id)
    # Creating RG
    rg_creation(RG_NAME,RG_LOCATION,resource_client)
    vnet_creation(RG_NAME,VNET_NAME,network_client,RG_LOCATION)
    subnet_creation(RG_NAME,VNET_NAME,SUBNET_NAME,network_client)
    for i in range(NO_OF_VMS):
        VM_NAME = (f"{RG_NAME}-VM-{str(i+1)}")
        PIP_NAME = (f"{VM_NAME}-PIP")
        NIC_NAME = (f"{VM_NAME}-NIC")
        vm_size = 'Standard_D1_v2'
        image_reference = {
            'publisher': 'Canonical',
            'offer': 'UbuntuServer',
            'sku': '18.04-LTS',
            'version': 'latest'
        }
        pip_id = pip_creation(RG_NAME,PIP_NAME,RG_LOCATION,network_client)
        nic_id = nic_creation(RG_NAME,NIC_NAME,network_client,RG_LOCATION,subscription_id,VNET_NAME,SUBNET_NAME,pip_id)
        vm_creation(RG_NAME,VM_NAME,RG_LOCATION,vm_size,image_reference,nic_id,compute_client)
        
        
if __name__ == "__main__":
    main()