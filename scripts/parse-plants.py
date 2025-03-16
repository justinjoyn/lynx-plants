import json
import re
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Clean the given text by removing newline characters,
    Unicode en-dashes, extra blank spaces, and any trailing dashes.
    """
    if not text:
        return ""
    # Replace newline characters and en-dash characters.
    text = text.replace("\n", " ").replace("\u2013", "")
    # Collapse multiple spaces into one.
    text = " ".join(text.split())
    # Remove trailing dashes (regular or en-dash).
    text = re.sub(r"\s*[-–]+\s*$", "", text)
    return text

def parse_li(li):
    """
    Parse a single <li> element into a flat plant object.
    The plant object will include:
      - 'name': the common name (from the first non-empty text node),
      - 'species': the species name from the first <a> tag,
      - 'link': the href from the first <a> tag (with Wikipedia URL prepended if needed).
    If the name is empty, None is returned.
    """
    entry = {}

    # Get the common name: use the first non-empty string from li's direct contents.
    common_name = ""
    for child in li.contents:
        if isinstance(child, str) and child.strip():
            common_name = child
            break
    common_name = clean_text(common_name)
    if not common_name:
        return None  # Skip this li if the common name is empty.
    entry["name"] = common_name

    # Process the first <a> tag for species info.
    a_tag = li.find("a")
    if a_tag:
        species_text = clean_text(a_tag.get_text())
        entry["species"] = species_text
        link = a_tag.get("href", "")
        # Prepend Wikipedia URL if the link is relative.
        if link.startswith("/"):
            link = "https://en.wikipedia.org" + link
        entry["link"] = link

    return entry

def parse_html_to_json_flat(html_content):
    """
    Parse the HTML content and extract all <li> elements as flat plant objects.
    Only plant objects with a non-empty 'name' are included.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    plants = []
    for li in soup.find_all("li"):
        plant = parse_li(li)
        if plant and plant.get("name"):
            plants.append(plant)
    return plants

def main():
    input_file = "../data/plants.html"   # Input HTML file.
    output_file = "../data/plants.json"  # Output JSON file.
    
    # Read the HTML content from the file.
    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Parse the HTML and get a flat list of plant objects.
    plants_data = parse_html_to_json_flat(html_content)
    json_output = json.dumps(plants_data, indent=4)

    # Write the JSON output to the file.
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json_output)

    print(f"JSON output written to {output_file}")

if __name__ == "__main__":
    main()