from azure.core.exceptions import HttpResponseError
def vnet_creation(RG_NAME,VNET_NAME,network_client,RG_LOCATION):
    try:
        poller = network_client.virtual_networks.begin_create_or_update(
        RG_NAME,
        VNET_NAME,
        {
            'location': RG_LOCATION,
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
        )
        vnet_result = poller.result()
        print(f"VNet created succesfully: {vnet_result.name},location: {vnet_result.location} ")
    except HttpResponseError as error:
        print ({error})
    return None