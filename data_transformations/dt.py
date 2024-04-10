import json
from datetime import datetime

#So this is where the output from the Chefs Python would be attricuted to this object "anna's output"

annas_output = '''
{
  "data": [
    {"Species_Name": "Alces alces", "Name": "Big Moose", "Count": "1", "Observation_date": "2023-01-01"},
    {"Species_Name": "Erinaceus europaeus", "Name": "Spiky Boy", "Count": 14, "Observation_date": "2023-02-01"}
  ]
}
'''
#Create a dict and a map for the transformation

data_dict = json.loads(annas_output)

print(data_dict)

column_mapping = {
    "Species_Name": "Species",
    "Name": "Individual_Name",
    "Count": ("Total_count", int),  
    "Observation_date": ("Date", lambda x: datetime.strptime(x, '%Y-%m-%d'))  # Convert to datetime
}

# Transform the data
transformed_data = []
for item in data_dict["data"]:
    transformed_item = {}
    for old_key, new_key in column_mapping.items():
        if isinstance(new_key, tuple):
            new_key, transform_function = new_key
            transformed_item[new_key] = transform_function(item[old_key])
        else:
            transformed_item[new_key] = item[old_key]
    transformed_data.append(transformed_item)


print(json.dumps({"data": transformed_data}, indent=2, default=str))
