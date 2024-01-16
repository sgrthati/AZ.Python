from azure.core.exceptions import HttpResponseError
def pip_creation(RG_NAME,PIP_NAME,RG_LOCATION,network_client):
    try:
        pip = network_client.public_ip_addresses.begin_create_or_update(RG_NAME,
        PIP_NAME,
        {
            "location": RG_LOCATION,
            "sku": { "name": "Standard" },
            "public_ip_allocation_method": "Static",
            "public_ip_address_version" : "IPV4"
        }
        )
        pip_result = pip.result()
        print(f"PIP created succesfully: {pip_result.name},location: {pip_result.location} ")
        pip_id = pip_result.id
        print(f"pip_id:{pip_id}")      
    except HttpResponseError as error:
        print ({error})
    return pip_id