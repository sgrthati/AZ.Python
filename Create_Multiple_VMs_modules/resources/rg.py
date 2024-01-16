from azure.core.exceptions import HttpResponseError
# Create a new resource group
def rg_creation(RG_NAME,RG_LOCATION,resource_client):
    resource_group_name = RG_NAME
    location = RG_LOCATION
    try:
        rg_result = resource_client.resource_groups.create_or_update(
                resource_group_name,
                {'location': location}
        )
        print(f"RG created succesfully in {rg_result.name},location {rg_result.location} ")
    except HttpResponseError as error:
        print ({error})
    return None