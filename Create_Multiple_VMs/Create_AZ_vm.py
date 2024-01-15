RG_NAME = "SRI"
RG_LOCATION = "eastus"
NO_OF_VMS = 2
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
print (f"creating New ResourceGroup: {RG_NAME}")
# Create a new resource group
resource_group_name = RG_NAME
location = RG_LOCATION
resource_client.resource_groups.create_or_update(
    resource_group_name,
    {'location': location}
)
#Create a new VNet with Subnet
GROUP_NAME = RG_NAME
VNET_NAME =  (RG_NAME + "-VNet")
LOCATION = RG_LOCATION
SUBNET_NAME = (VNET_NAME + "-Subnet1")
print (f"Creating a Vnet: {VNET_NAME}")

network_client = NetworkManagementClient(credentials, subscription_id)
try:
    vnet = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VNET_NAME,
        {
            'location': LOCATION,
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    )
except AzureError as error:
    if "InUseSubnetCannotBeDeleted" in error.message:
        print("Subnet already exist")
    else:
        print (error.message)
        raise
# Create Subnet
try:
    async_subnet_creation = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    )
except AzureError as error:
    # if error.response.status_code == "InUseSubnetCannotBeDeleted":
    #     print("resource already exist")
    # else:
    print(error.message)
subnet_info = async_subnet_creation.result()
print (f"Created a SubNet: {subnet_info.name}")
# Create a new VM
for i in range(NO_OF_VMS):
    vm_name = (RG_NAME + "-VM-" + str(i+1))
    NIC_NAME = (vm_name + "-NIC")
    IP_NAME = (vm_name + "-PIP")
    vm_size = 'Standard_D1_v2'
    image_reference = {
        'publisher': 'Canonical',
        'offer': 'UbuntuServer',
        'sku': '18.04-LTS',
        'version': 'latest'
    }
    try:
        pip = network_client.public_ip_addresses.begin_create_or_update(resource_group_name,
            IP_NAME,
            {
                "location": RG_LOCATION,
                "sku": { "name": "Standard" },
                "public_ip_allocation_method": "Static",
                "public_ip_address_version" : "IPV4"
            }
        )
    except HttpResponseError as error:
        # if error.response.status_code == "InUseSubnetCannotBeDeleted":
        #     print("resource already exist")
        # else:
            print(error.message)
    ip_address_result = pip.result()
    print (f"Created a PIP: {ip_address_result.name}")
    try:
        nic = network_client.network_interfaces.begin_create_or_update(
            resource_group_name,
            NIC_NAME,
            {
                'location': LOCATION,
                'ip_configurations': [{
                    'name': (NIC_NAME + "-myipconfig"),
                    'subnet': {
                        'id': '/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Network/virtualNetworks/{}/subnets/{}'.format(subscription_id, resource_group_name,VNET_NAME,SUBNET_NAME),
                    'public_ip_address': {'id': ip_address_result.id}
                    }
                }]
            }
        )
    except HttpResponseError as error:
        # if error.response.status_code == "InUseSubnetCannotBeDeleted":
        #     print("resource already exist")
        # else:
            print(error.message)
    nic_result = nic.result()
    print (f"Created a NIC: {nic_result.name}")
    try:
        vm = compute_client.virtual_machines.begin_create_or_update(
            resource_group_name,
            vm_name,
            {
                'location': location,
                'hardware_profile': {
                    'vm_size': vm_size
                },
                'storage_profile': {
                    'image_reference': image_reference
                },
                'network_profile': {
                    'network_interfaces': [{
                        'id': nic_result.id
                    }]
                },
                "os_profile": {
                "computer_name": vm_name,
                "admin_username": "Sagar",
                "admin_password": "Sagar@22331818"
                }
            }
        )
    except HttpResponseError as error:
        # if error.response.status_code == "InUseSubnetCannotBeDeleted":
        #     print("resource already exist")
        # else:
            print(error.message)
    vm_result = vm.result()
    print(f"Provisioned virtual machine: {vm_result.name}")