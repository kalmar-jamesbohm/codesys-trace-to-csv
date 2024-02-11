import csv
import xml.etree.ElementTree as ET

class LazyXMLLoader:
    def __init__(self, filename):
        self.filename = filename
        self.context = iter(ET.iterparse(filename, events=('start', 'end')))
        self.root = None
        self.current_element = None
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while True:
            event, element = next(self.context)
            if event == 'start':
                if self.root is None:
                    self.root = element
                self.current_element = element
            elif event == 'end':
                if element == self.root:
                    raise StopIteration
                return element

# Example usage
xml_file = 'example.trace'
lazy_loader = LazyXMLLoader(xml_file)

for element in lazy_loader:
    if element.tag == 'TraceVariable':
        var_name = element.get('VarName')
        if var_name is not None:
            # Find 'values' and 'timestamps' children
            values_elem = element.find('Values')
            timestamps_elem = element.find('Timestamps')
            if values_elem is not None and timestamps_elem is not None:
                # Split comma-separated values and timestamps into lists
                values = values_elem.text.split(',')
                timestamps = timestamps_elem.text.split(',')
                # Create a list of tuples containing values and timestamps
                data = list(zip(timestamps, values))
                # Write data to CSV file
                csv_filename = f"{var_name}.csv"
                with open(csv_filename, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['Timestamp', 'Value'])
                    csv_writer.writerows(data)
                print(f"CSV file '{csv_filename}' created.")
