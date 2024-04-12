import json
from datetime import datetime

class DataFormat:

    def __init__(self, json_input, column_mapping):
        """
        Initialize the DataMapper class
        Args: 
            JSON input (str)
            Column mapping (str)
        """
        self.json_input = json_input
        self.column_mapping = column_mapping

    def json_to_dict(self):
        """
        Loads data from JSON into python dict.
        Args:
            json object
            returns py dict
        """
        return json.loads(self.json_input)

    def map_data_header(self, data):
        """
        Maps columns in the data according to the provided column mapping.
        """
        mapped_data = []
        for item in data:
            mapped_item = {}
            for old_key, new_key in self.column_mapping.items():
                if isinstance(new_key, tuple):
                    new_key, transform_function = new_key
                    mapped_item[new_key] = transform_function(item[old_key])
                else:
                    mapped_item[new_key] = item[old_key]
            mapped_data.append(mapped_item)
        return mapped_data

    def convert_back(self, mapped_data):
        """
        Converts the mapped data back into a JSON string and prints it.
        """
        print(json.dumps({"data": mapped_data}, indent=2, default=str))

    def process_data(self):
        """
        This function wraps the whole process together so this is the only one that needs to be called
        after establishing data
        
        """
        data = self.json_to_dict()['data']
        mapped_data = self.map_data_header(data)
        self.convert_back(mapped_data)


#this will need to be provied by user, then declared an instance of the class DataFormat
input_data = '''
{
  "data": [
    {"Species_Name": "Alces alces", "Name": "Big Moose", "Count": "1", "Observation_date": "2023-01-01"},
    {"Species_Name": "Erinaceus europaeus", "Name": "Spiky Boy", "Count": 14, "Observation_date": "2023-02-01"}
  ]
}
'''
#this also needs to be provided by the user based on their column headers and ours, linked.
column_mapping = {
    "Species_Name": "Species",
    "Name": "Individual_Name",
    "Count": ("Total_count", int),  
    "Observation_date": ("Date", lambda x: datetime.strptime(x, '%Y-%m-%d'))
}


#Now we can establish with one line of code and execute with another line of code.
#First off, we declare the user's data as a new instance of the class and assign to data_mapper object
data_mapper = DataFormat(input_data, column_mapping)
#Then execute process_data on the new object.
data_mapper.process_data()

