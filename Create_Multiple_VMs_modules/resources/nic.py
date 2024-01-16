def nic_creation(RG_NAME,NIC_NAME,network_client,ip_address_result,RG_LOCATION,subscription_id,VNET_NAME,SUBNET_NAME):
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
            'public_ip_address': {'id': ip_address_result.id}
        }]
    }
    )
    nic_result = nic.result()
    return nic_result