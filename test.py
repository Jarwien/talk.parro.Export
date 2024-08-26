import requests
import json
import xml.etree.ElementTree as ET

# Set the API endpoint and Bearer token
url = "https://rest-v2.parro.com/rest/v2/attachment?attachmentType=IMAGE&attachmentType=VIDEO&group=xxxxx"  # Replace with your actual API endpoint 
bearer_token = "" # Put in here your bearer token from the rest-v2 request

# Set up the headers that do not change in the loop

headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/vnd.topicus.geon+json"  # Updated to the specific content type some times the response is not always json but xml
}

# Loop to fetch data in increments of 50 items, 60 times Change the range if you need more after the last json/xml is still giving you response
for i in range(60):
    start_item = i * 50
    end_item = start_item + 49
    range_header = f"items={start_item}-{end_item}"
    
    # Add the range header to the headers dictionary
    headers["Range"] = range_header
    
    # Make the API call
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code in [200, 206]:  # 200 OK or 206 Partial Content
        content_type = response.headers.get('Content-Type', '')

        if 'application/json' in content_type or 'application/vnd.topicus.geon+json' in content_type:
            # Handle JSON response
            data = response.json()
            
            # Define the output file, appending the range to the filename
            output_file = f"api_response_{start_item}_{end_item}.json"
            
            # Save the JSON response to a file
            with open(output_file, "w") as file:
                json.dump(data, file, indent=4)
            
            print(f"JSON response for items {start_item} to {end_item} saved to {output_file}")
        
        elif 'application/xml' in content_type or 'text/xml' in content_type:
            # Handle XML response
            root = ET.fromstring(response.content)
            
            # Define the output file, appending the range to the filename
            output_file = f"api_response_{start_item}_{end_item}.xml"
            
            # Save the XML response to a file
            tree = ET.ElementTree(root)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            print(f"XML response for items {start_item} to {end_item} saved to {output_file}")
        
        else:
            print(f"Unsupported content type: {content_type}")
        
    else:
        print(f"Failed to fetch data for items {start_item} to {end_item}. Status code: {response.status_code}")
        print(f"Response: {response.text}")