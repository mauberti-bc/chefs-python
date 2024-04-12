import json
from datetime import datetime

def json_to_dict(json_input):
    '''
    Purpose: Loads data from JSON into python dict.
    
    Args:
        json_input (str)
    
    Returns:
        python list of objects (dict)
    
    '''
    return json.loads(json_input)
  

def map_data_header(json_input, column_mapping):
    """
    Takes the new py dict data, and a user inputted mapping key and replaces columns based on name in map
    
    Args:
        input data in the form of python dict (dict)
        Column mapping (str) - value pair mapping key created by user.
        
    Returns: 
        mapped_data which is the column transformed data with newly attributed column headings (dict)
    """
    mapped_data = []
    for item in json_input:
        mapped_item = {}
        for old_key, new_key in column_mapping.items():
            if isinstance(new_key, tuple):
                new_key, transform_function = new_key
                mapped_item[new_key] = transform_function(item[old_key])
            else:
                mapped_item[new_key] = item[old_key]
        mapped_data.append(mapped_item)
    return mapped_data
  
  

def convert_back(mapped_data):
    """
    This will convert the data bac into a JSON format
    
    Args: 
      data output with the newly mapped headers (dict)
      
    Returns:
      Dumps python dict back into JSON (str).
    
    """
    print(json.dumps({"data": mapped_data}, indent=2, default=str))



# The below variables would need to be edited to contain the users data.
fake_data = '''
{
  "data": [
    {"Species_Name": "Alces alces", "Name": "Big Moose", "Count": "1", "Observation_date": "2023-01-01"},
    {"Species_Name": "Erinaceus europaeus", "Name": "Spiky Boy", "Count": 14, "Observation_date": "2023-02-01"}
  ]
}
'''

# This needs to be edited for each new source of data and use. Matchign the mapping for the columns as needed.

column_mapping = {
    "Species_Name": "Species",
    "Name": "Individual_Name",
    "Count": ("Total_count", int),  
    "Observation_date": ("Date", lambda x: datetime.strptime(x, '%Y-%m-%d'))  # Convert to datetime
}


# Using the fake_data andthe column_mapping object, we can run below.

loaded_data = json_to_dict(fake_data)
mapped_data = map_data_header(loaded_data['data'], column_mapping)
print(mapped_data)

# 
# Future: 
# These set of functions can and should be edited into a wider class that only needs to be called once.