from azure.core.exceptions import HttpResponseError
def nic_creation(RG_NAME,NIC_NAME,network_client,RG_LOCATION,subscription_id,VNET_NAME,SUBNET_NAME,pip_id):
    try:
        nic = network_client.network_interfaces.begin_create_or_update(
        RG_NAME,
        NIC_NAME,
        {
            'location': RG_LOCATION,
            'ip_configurations': [{
                'name': (NIC_NAME + "-myipconfig"),
                'subnet': {
                    'id': '/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Network/virtualNetworks/{}/subnets/{}'.format(subscription_id,RG_NAME,VNET_NAME,SUBNET_NAME),
                },
                'public_ip_address': {'id': pip_id}
            }]
        }
        )
        nic_result = nic.result()
        print(f"NIC created succesfully: {nic_result.name},location: {nic_result.location} ")
        nic_id = nic_result.id
        print(f"nic_id:{nic_id}")      
    except HttpResponseError as error:
        print ({error})
    return nic_id       