import json
import requests
import os
from openai import OpenAI
from prompts import  assistant_instructions
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
GOOGLE_CLOUD_API_KEY = os.environ['GOOGLE_CLOUD_API_KEY']
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']

# Init OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)


# # Add lead to Airtable
# def create_lead(name, phone, address):
#   url = "https://api.airtable.com/v0/appM1yx0NobvowCAg/Leads"  # Change this to your Airtable API URL
#   headers = {
#       "Authorization": AIRTABLE_API_KEY,
#       "Content-Type": "application/json"
#   }
#   data = {
#       "records": [{
#           "fields": {
#               "Name": name,
#               "Phone": phone,
#               "Address": address
#           }
#       }]
#   }
#   response = requests.post(url, headers=headers, json=data)
#   if response.status_code == 200:
#     print("Lead created successfully.")
#     return response.json()
#   else:
#     print(f"Failed to create lead: {response.text}")


# # Get coordidinates from address via Geocoding API
# def get_coordinates(address):
#   geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_CLOUD_API_KEY}"
#   response = requests.get(geocoding_url)
#   if response.status_code == 200:
#     location = response.json().get('results')[0].get('geometry').get(
#         'location')
#     print(f"Coordinates for {address}: {location}")
#     return location['lat'], location['lng']
#   else:
#     print(f"Error getting coordinates: {response.text}")


# # Get solar data for coordinate from Solar API
# def get_solar_data(lat, lng):
#   solar_api_url = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={lat}&location.longitude={lng}&requiredQuality=HIGH&key={GOOGLE_CLOUD_API_KEY}"
#   response = requests.get(solar_api_url)
#   if response.status_code == 200:
#     print("Solar data retrieved successfully.")
#     return response.json()
#   else:
#     print(f"Error getting solar data: {response.text}")


# # Extract financial data LIST from solar data
# def extract_financial_analyses(solar_data):
#   try:
#     return solar_data.get('solarPotential', {}).get('financialAnalyses', [])
#   except KeyError as e:
#     print(f"Data extraction error: {e}")


# # Get financial data for the address
# def get_financial_data_for_address(address):
#   lat, lng = get_coordinates(address)
#   if not lat or not lng:
#     return {"error": "Could not get coordinates for the address provided."}
#   return extract_financial_analyses(get_solar_data(lat, lng))


# # Match user's bill to scenario in the financial data
# def find_closest_financial_analysis(user_bill, financial_analyses):
#   closest_match = None
#   smallest_difference = float('inf')
#   for analysis in financial_analyses:
#     bill_amount = int(analysis.get('monthlyBill', {}).get('units', 0))
#     difference = abs(bill_amount - user_bill)
#     if difference < smallest_difference:
#       smallest_difference = difference
#       closest_match = analysis
#   return closest_match


# # Use GPT completion to extract most relevant data from financial analysis
# def simplify_financial_data(data):
#   try:

#     data_str = json.dumps(data, indent=2)

#     # Getting formatter prompt from "prompts.py" file
#     system_prompt = formatter_prompt

#     # Replace 'client' with your actual OpenAI client initialization.
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         # model="gpt-4-1106-preview",
#         messages=[
#             {
#                 "role": "system",
#                 "content":
#                 system_prompt  # Getting prompt from "prompts.py" file
#             },
#             {
#                 "role":
#                 "user",
#                 "content":
#                 f"Here is some data, parse and format it exactly as shown in the example: {data_str}"
#             }
#         ],
#         temperature=0,
#         # stream=True,

#         )

#     simplified_data = json.loads(completion.choices[0].message.content)
#     print("Simplified Data:", simplified_data)
#     return simplified_data

#   except Exception as e:
#     print("Error simplifying data:", e)
#     return None


# # Main calculation function for solar data output
# def solar_panel_calculations(address, monthly_bill):
#   print(
#       f"Calculating solar panel potential for {address} with bill amount {monthly_bill}."
#   )
#   financial_analyses = get_financial_data_for_address(address)
#   if "error" in financial_analyses:
#     print(financial_analyses["error"])
#     return financial_analyses
#   closest_financial_analysis = find_closest_financial_analysis(
#       int(monthly_bill), financial_analyses)
#   if closest_financial_analysis:
#     return simplify_financial_data(closest_financial_analysis)
#   else:
#     print("No suitable financial analysis found.")
#     return {
#         "error": "No suitable financial analysis found for the given bill."
#     }

# def get_chocolate_price(brand, quantity):
#   print(
#       f"Calculating price for {brand} chocolate for amount {quantity}."
#   )
#   # Mock price for 1 KitKat bar
#   kitkat_price = 1.50
  
#   # Calculate total price based on quantity
#   total_price = kitkat_price * quantity
  
#   return {
#       "price": total_price,
#       "message": f"The estimated price for {quantity} {brand} bar(s) is ${total_price:.2f}"
#   }
  


# Create or load assistant
# def create_assistant(client):
#   assistant_file_path = 'assistant.json'

#   # If there is an assistant.json file already, then load that assistant
#   if os.path.exists(assistant_file_path):
#     with open(assistant_file_path, 'r') as file:
#       assistant_data = json.load(file)
#       assistant_id = assistant_data['assistant_id']
#       print("Loaded existing assistant ID.")
#   else:
#     # If no assistant.json is present, create a new assistant using the below specifications

#     # To change the knowledge document, modifiy the file name below to match your document
#     # If you want to add multiple files, paste this function into ChatGPT and ask for it to add support for multiple files
#     file = client.files.create(file=open("knowledge.docx", "rb"),
#                                purpose='assistants')
#     print("file of knowledge",file)
#     assistant = client.beta.assistants.create(
#         # Getting assistant prompt from "prompts.py" file, edit on left panel if you want to change the prompt
#         instructions=assistant_instructions,
#         model="gpt-3.5-turbo",
#         # model="gpt-4-1106-preview",
#         tools=[
#             {
#                 "type": "retrieval"  # This adds the knowledge base as a tool
#             },
#             {
#                 "type": "function",  # This adds the solar calculator as a tool
#                 "function": {
#                     "name": "get_chocolate_price",
#                     "description":
#                     "Calculate the price of a chocolate bar based on the type of chocolate given.",
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "brand": {
#                                 "type":
#                                 "string",
#                                 "description":
#                                 "The type or brand of chocolate ex. KitKat, Snickers, Mars, etc."
#                             },
#                             "quantity": {
#                                 "type":
#                                 "integer",
#                                 "description":
#                                 "Number of chocolate bars requested by the user."
#                             }
#                         },
#                         "required": ["brand", "quantity"]
#                     }
#                 }
#             },
#             {
#                 "type": "function",  # This adds the solar calculator as a tool
#                 "function": {
#                     "name": "solar_panel_calculations",
#                     "description":
#                     "Calculate solar potential based on a given address and monthly electricity bill in USD.",
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "address": {
#                                 "type":
#                                 "string",
#                                 "description":
#                                 "Address for calculating solar potential."
#                             },
#                             "monthly_bill": {
#                                 "type":
#                                 "integer",
#                                 "description":
#                                 "Monthly electricity bill in USD for savings estimation."
#                             }
#                         },
#                         "required": ["address", "monthly_bill"]
#                     }
#                 }
#             },
#             {
#                 "type": "function",  # This adds the lead capture as a tool
#                 "function": {
#                     "name": "create_lead",
#                     "description":
#                     "Capture lead details and save to Airtable.",
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "name": {
#                                 "type": "string",
#                                 "description": "Name of the lead."
#                             },
#                             "phone": {
#                                 "type": "string",
#                                 "description": "Phone number of the lead."
#                             },
#                             "address": {
#                                 "type": "string",
#                                 "description": "Address of the lead."
#                             }
#                         },
#                         "required": ["name", "phone", "address"]
#                     }
#                 }
#             }
#         ],
#         file_ids=[file.id])

#     # Create a new assistant.json file to load on future runs
#     with open(assistant_file_path, 'w') as file:
#       json.dump({'assistant_id': assistant.id}, file)
#       print("Created a new assistant and saved the ID.")

#     assistant_id = assistant.id

#   return assistant_id




def create_assistant(client):
    assistant_file_path = 'assistant.json'
    
    # Check if the assistant.json file exists
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        # Create a new assistant with a specific knowledge document
        # file = client.files.create(file=open("california_real_estate.docx", "rb"), purpose='assistants')
        # print("File of knowledge uploaded:", file)
        
        assistant = client.beta.assistants.create(
            instructions=assistant_instructions,
            model="gpt-4-turbo",  # Use GPT-4 model
            tools=[
                {
                    "type": "retrieval"  # Adds the knowledge base as a tool
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_property_value_estimate",
                        "description": "Estimate the value of a property based on its location and features.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "address": {
                                    "type": "string",
                                    "description": "Address of the property."
                                },
                                "features": {
                                    "type": "object",
                                    "description": "Features of the property such as number of bedrooms, bathrooms, etc.",
                                    "properties": {
                                        "bedrooms": {
                                            "type": "integer",
                                            "description": "Number of bedrooms."
                                        },
                                        "bathrooms": {
                                            "type": "integer",
                                            "description": "Number of bathrooms."
                                        },
                                        "square_feet": {
                                            "type": "integer",
                                            "description": "Total square footage of the property."
                                        }
                                    },
                                    "required": ["bedrooms", "bathrooms", "square_feet"]
                                }
                            },
                            "required": ["address", "features"]
                        }
                    }
                }
            ],
            file_ids=[file.id]
        )
        
        # Save the new assistant ID for future use
        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")
        
        assistant_id = assistant.id

    return assistant_id
