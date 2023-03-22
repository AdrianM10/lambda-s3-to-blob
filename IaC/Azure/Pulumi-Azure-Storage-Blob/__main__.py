"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("rg_demo")

# Create an Azure resource (Storage Account)
account = storage.StorageAccount(
    "s3tostrblob",
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(
        name=storage.SkuName.STANDARD_LRS,
    ),
    kind=storage.Kind.STORAGE_V2,
)
# Create an Azure resource (Blob Container)
blob_container = storage.BlobContainer(
    account_name = account.name,
    resource_group_name=resource_group.name,
    resource_name = "demo-container"
)

# Export the primary key of the Storage Account
primary_key = (
    pulumi.Output.all(resource_group.name, account.name)
    .apply(
        lambda args: storage.list_storage_account_keys(
            resource_group_name=args[0], account_name=args[1]
        )
    )
    .apply(lambda accountKeys: accountKeys.keys[0].value)
)


pulumi.export("primary_storage_key", primary_key)
pulumi.export("storage_account_name", account.name)
pulumi.export("container_name", blob_container.name)
pulumi.export("connection_string", pulumi.Output.concat("DefaultEndpointsProtocol=https;AccountName=", account.name, ";AccountKey=", primary_key, ";EndpointSuffix=core.windows.net"))

