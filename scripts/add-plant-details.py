import json
import re
import requests
import uuid
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Clean text by removing newlines, Unicode en-dashes, extra spaces, and trailing dashes.
    """
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\u2013", "")
    text = " ".join(text.split())
    text = re.sub(r"\s*[-–]+\s*$", "", text)
    return text

def extract_intro_and_description(html_content):
    """
    Extracts introduction and description from a Wikipedia page.

    - Introduction: All text from <p> tags in the main content (div with class "mw-parser-output")
      until a <div class="mw-heading"> containing "Description" is encountered.
    - Description: All text from subsequent <p> tags until the next <div class="mw-heading">.
    
    Returns a tuple: (introduction, description)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    content_div = soup.find("div", class_="mw-parser-output")
    if not content_div:
        return "", ""
    
    intro_paragraphs = []
    desc_paragraphs = []
    in_description = False

    for child in content_div.children:
        if not hasattr(child, 'name'):
            continue

        if child.name == "div" and "mw-heading" in child.get("class", []):
            heading_text = child.get_text(" ", strip=True).lower()
            if "description" in heading_text:
                in_description = True
                continue
            elif in_description:
                break

        if child.name == "p":
            text = clean_text(child.get_text())
            if text:
                if not in_description:
                    intro_paragraphs.append(text)
                else:
                    desc_paragraphs.append(text)

    introduction = "\n\n".join(intro_paragraphs)
    description = "\n\n".join(desc_paragraphs)
    return introduction, description

def main():
    input_file = "../src/assets/data/plants.json"  # Your existing JSON file with plant objects.
    
    # Load existing plant objects.
    with open(input_file, "r", encoding="utf-8") as f:
        plants = json.load(f)

    # Process each plant and update its JSON object.
    for plant in plants:
        # Generate a unique id for each plant.
        plant["id"] = str(uuid.uuid4())
        
        link = plant.get("link", "")
        species = plant.get("species", "")
        if not link or not species:
            print(f"Skipping plant due to missing link or species: {plant}")
            continue

        print(f"Processing '{species}' from {link}...")
        try:
            response = requests.get(link)
            if response.status_code == 200:
                html_content = response.text
                intro, desc = extract_intro_and_description(html_content)
                full_description = intro
                if desc:
                    full_description += "\n\n" + desc
                plant["description"] = full_description
                print(f"Extracted description for '{species}'")
            else:
                print(f"Failed to fetch {link}. HTTP status: {response.status_code}")
        except Exception as e:
            print(f"Error fetching {link}: {e}")

    # Write the updated plant objects back to the same JSON file.
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(plants, f, indent=4)
    
    print("Updated plants.json with descriptions and unique IDs.")

if __name__ == "__main__":
    main()