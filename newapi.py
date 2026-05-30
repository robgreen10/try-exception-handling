import requests
from requests.exceptions import RequestException

ip_address = input("Insert IPAddress: ")

# Checking if an IP is a known malicious threat, and formatting a clean security alert report.


class ipanalyzer:
    def __init__(self):
        self.api_url = "http://ip-api.com/json/"

    def check_ip(self, ip_address):
        '''Queries API to fetch location data for the given IP address'''
        target_url = f"{self.api_url}{ip_address}"

        try:
            response = requests.get(target_url, timeout=5)
        except RequestException as e:
            print(f"Error fetching IP data for {ip_address}: {e}")
            return None
        data = response.json()

        return data

    def generate_report(self, ip_data):
        '''Generates a clean security alert report based on IP data'''
        if not ip_data or ip_data.get("status") == "fail":
            return ("API failure or network failure..")

        # 2. Extract specific values from the API dictionary using .get()
        country = ip_data.get("country", "Unknown")
        isp = ip_data.get("isp", "Unknown")
        org = ip_data.get("org", "Unknown")
        as_number = ip_data.get("as", "Unknown")

        malicious_countries = ["China", "France", "Russia"]
        if country in malicious_countries:
            assessment = f"{country} is a known malicious location. This IP address needs to be blocked."
        else:
            assessment = f"{country} is a benign location. No further actions required."

        # 3. Format the report
        report = f"""
Security Alert: Suspicious IP Activity Detected
================================================

IP Address: {ip_address}
Country: {country}
ISP: {isp}
Organization: {org}
AS Number: {as_number}
Analysis: {assessment}

This IP address has been flagged for review.
        """
        return report

    '''Execution Pipeline'''


if __name__ == "__main__":
    scanner = ipanalyzer()
    # Example suspicious IP address (This one belongs to Google's public DNS)
    test_ip = ip_address

    print(f"📡 Querying Threat Intel for: {test_ip}...")

    raw_data = scanner.check_ip(test_ip)
    final_report = scanner.generate_report(raw_data)

print(final_report)
