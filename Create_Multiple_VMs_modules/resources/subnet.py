from azure.core.exceptions import HttpResponseError
def subnet_creation(RG_NAME,VNET_NAME,SUBNET_NAME,network_client):
    try:
        poller = network_client.subnets.begin_create_or_update(
        RG_NAME,
        VNET_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
        )
        subnet_result = poller.result()
        subnet_id = subnet_result.id
        print(subnet_id)
        print(f"subnet created succesfully: {subnet_result.name} ")
    except HttpResponseError as error:
        if "InUseSubnetCannotBeDeleted" in error.message:
            print("resource already exist")
        else:
            print(error.message)
            raise  
    return None