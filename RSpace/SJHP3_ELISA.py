from bs4 import BeautifulSoup
import json

# Load the HTML file
with open('Imports/doc_SJHP3-ELISA-250555.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'lxml')

# Prepare a dictionary to hold the data
data = {}

# Find all <h3> titles and process their following content
for h3 in soup.find_all('h3'):
    title = h3.get_text(strip=True)
    content = []

    # Start checking siblings after this <h3>
    sibling = h3.find_next_sibling()

    while sibling:
        if sibling.name == 'h3':
            # Break if we encounter the next <h3>, we are done with this section
            break

        elif sibling.name == 'div':  # Handle <div> as well, if they contain text

            # Check for tables within this div
            tables = sibling.find_all('table')
            for table in tables:
                table_data = []

                for row in table.find_all('tr'):
                    row_data = []
                    for cell in row.find_all('td'):
                        cell_text = cell.get_text(strip=True)
                        if cell_text:  # Only include non-empty cells
                            row_data.append(cell_text)
                    if row_data:  # Only include non-empty rows
                        table_data.append(row_data)

                content.append(table_data)

        #Extract text content from divs and split by line breaks
        if sibling.name != 'table':
            # Find all <p> and <li> tags within the sibling
            paragraphs = sibling.find_all(['p', 'li'])
            for tag in paragraphs:
                text_content = tag.get_text(strip=True)
                if text_content:  # Avoid empty text nodes
                    content.append(text_content)

                # Move to the next sibling
        sibling = sibling.find_next_sibling()

    if content:  # Only add to data if there is content
        data[title] = content

# Convert to JSON
json_output = json.dumps(data, indent=4)

# Get the desired filename from console input
filename = input("Enter the name for the output file (without extension): ")

# Create the full path for the JSON file
json_output_path = f"Exports/{filename}.json"

# Save JSON to a file
with open(json_output_path, "w") as json_file:
    json_file.write(json_output)

# Print or save the JSON output
print(f"JSON output saved to {json_output_path}")
print(json_output)
