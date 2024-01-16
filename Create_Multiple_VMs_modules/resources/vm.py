def vm_creation(RG_NAME,vm_name,RG_LOCATION,vm_size,image_reference,nic_result,compute_client):
    vm = compute_client.virtual_machines.begin_create_or_update(
    RG_NAME,
    vm_name,
    {
        'location': RG_LOCATION,
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
    vm_result = vm.result()
    return vm_result