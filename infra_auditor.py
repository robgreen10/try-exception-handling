import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import AzureError


class AzureinfraAuditor:
    def __init__(self, subscription_id: str):
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()
        # Switching to the base ResourceManagementClient to look at assets
        self.client = ResourceManagementClient(
            self.credential, self.subscription_id)

    def run_audit(self) -> list:
        print("🔐 [AUTHENTICATING] Verifying credentials with Azure control plane...")
        try:
            discovered_assets = []

            # 1. Get the lightweight list of resources
            resources = self.client.resources.list()

            for resource in resources:
                print(
                    f"🔎 [FETCHING DETAILS] Pulling full profile for {resource.name}...")

                try:
                    # 2. FORCE Azure to give us the full profile using its unique ID
                    full_resource = self.client.resources.get_by_id(
                        resource.id, api_version="2021-04-01")
                    raw_data = vars(full_resource)
                except Exception:
                    # Fallback to the basic resource if the full lookup fails
                    raw_data = vars(resource)

                # 3. Check our smart checklist on the full profile data
                status_value = "Unknown"
                if "provisioning_state" in raw_data and raw_data["provisioning_state"]:
                    status_value = raw_data["provisioning_state"]
                elif "properties" in raw_data and raw_data["properties"]:
                    # Check inside nested properties if it's hiding there
                    props = raw_data["properties"]
                    if isinstance(props, dict):
                        status_value = props.get(
                            "provisioningState", "Unknown")
                    else:
                        status_value = getattr(
                            props, "provisioning_state", "Unknown")

                discovered_assets.append({
                    "name": resource.name or "Unnamed",
                    "location": resource.location or "Global",
                    "status": status_value,
                    "type": resource.type or "UnknownType"
                })
            return discovered_assets

        except AzureError as api_error:
            print(
                f"❌ [API ERROR] Failed to fetch resources from Azure: {api_error}")
            return []


# === LOCAL EXECUTION ===
if __name__ == "__main__":
    #  CORRECT (This looks into your MacBook's memory)
    MY_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")

    auditor = AzureinfraAuditor(subscription_id=MY_SUBSCRIPTION_ID)
    active_infrastructure = auditor.run_audit()

    print(
        f"\n🖥️ [INFRASTRUCTURE REPORT] Discovered {len(active_infrastructure)} Live Assets:")
    for asset in active_infrastructure:
        print(
            f"  -> Type: [{asset['type']}] | Name: {asset['name']} | Region: {asset['location']} | Status: {asset['status']}")
