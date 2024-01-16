from azure.core.exceptions import HttpResponseError
def vm_creation(RG_NAME,VM_NAME,RG_LOCATION,vm_size,image_reference,nic_id,compute_client):
    try:
        vm = compute_client.virtual_machines.begin_create_or_update(
        RG_NAME,
        VM_NAME,
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
                    'id': nic_id
                }]
            },
            "os_profile": {
            "computer_name": VM_NAME,
            "admin_username": "Sagar",
            "admin_password": "Sagar@22331818"
            }
        }
        )
        vm_result = vm.result()
        print(f"vm created succesfully: {vm_result.name},location: {vm_result.location} ")
        vm_id = vm_result.id
        print(f"vm_id:{vm_id}")      
    except HttpResponseError as error:
        print ({error})
    return None        