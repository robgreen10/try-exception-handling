# Importing the necessary Azure SDK modules to authenticate and manage storage resources
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient

# Creating this deployment class to handle our infrastructure creation logic cleanly


class AzureInfrastructureDeployer:
    # Initializing the deployer with your subscription details and setting up the API client
    def __init__(self, subscription_id: str):
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()
        self.storage_client = StorageManagementClient(
            self.credential, self.subscription_id)

    # Method to deploy a new storage account
    def deploy_storage_account(self, resource_group_name: str, location: str, storage_account_name: str):
        print(
            f"🚀 [DEPLOY] Starting deployment of storage account '{storage_account_name}'...")

        try:
            # Triggering the Azure API to provision the storage account with specific parameters
            poller = self.storage_client.storage_accounts.begin_create(
                resource_group_name,
                storage_account_name,
                {
                    "location": location,
                    # Standard Locally Redundant Storage (cost-effective for testing)
                    "sku": {"name": "Standard_LRS"},
                    "kind": "StorageV2"
                }
            )
            result = poller.result()
            print(
                f"✅ [SUCCESS] Storage account created successfully! Resource ID: {result.id}")
            return result
        except Exception as e:
            print(f"❌ [DEPLOY FAILED] Could not create storage account: {e}")
            return None

        # The safety valve! This ensures the script only runs when we execute this file directly.
if __name__ == "__main__":
    # 1. Pulls your secret subscription ID safely from your terminal's memory
    MY_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")

    # 2. REPLACE THIS: Put your actual, existing Azure Resource Group name here
    EXISTING_RESOURCE_GROUP = "rg-automation-testing"

    # 3. Azure region where your resource group lives
    REGION = "eastus"

    # 4. REPLACE THIS: Must be globally unique across all of Azure!
    # Use only lowercase letters and numbers (e.g., "auditorstorage77")
    UNIQUE_STORAGE_NAME = "auditorstorage77"

    # Initialize our deployer tool
    deployer = AzureInfrastructureDeployer(subscription_id=MY_SUBSCRIPTION_ID)

    # Kick off the deployment pipeline
    deployer.deploy_storage_account(
        resource_group_name=EXISTING_RESOURCE_GROUP,
        location=REGION,
        storage_account_name=UNIQUE_STORAGE_NAME
    )
