import json
import os
import re
import requests
from bs4 import BeautifulSoup

def sanitize_filename(text):
    """
    Sanitize text for use as a safe filename.
    Replaces spaces with underscores and removes non-alphanumeric characters.
    """
    text = re.sub(r'[^\w\s-]', '', text).strip()
    return text.replace(" ", "_")

def clean_text(text):
    """
    Clean the given text by removing newline characters, Unicode en-dashes,
    extra blank spaces, and trailing dashes.
    """
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\u2013", "")
    text = " ".join(text.split())
    text = re.sub(r"\s*[-–]+\s*$", "", text)
    return text

def extract_intro_and_desc(html_content):
    """
    Extracts the introduction and description from a Wikipedia page.
    
    - The introduction is defined as all text from the <p> tags within the 
      main content (div with class "mw-parser-output") until a <div> with class 
      "mw-heading" containing the word "Description" is encountered.
    - The description is defined as all text from the <p> tags after the 
      "Description" heading until the next <div class="mw-heading"> is reached.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    content_div = soup.find("div", class_="mw-parser-output")
    if not content_div:
        return "", ""
    
    introduction_paragraphs = []
    description_paragraphs = []
    in_description = False

    for child in content_div.children:
        # Skip non-tags (like newline strings)
        if not hasattr(child, 'name'):
            continue

        # Check if we have encountered a heading div.
        if child.name == "div" and "mw-heading" in child.get("class", []):
            heading_text = child.get_text(" ", strip=True)
            # When we see a heading that contains "Description", start collecting description.
            if "description" in heading_text.lower():
                in_description = True
                continue
            # If already collecting description and another mw-heading is found, stop.
            if in_description:
                break

        # Collect text from <p> tags.
        if child.name == "p":
            text = clean_text(child.get_text())
            if text:
                if not in_description:
                    introduction_paragraphs.append(text)
                else:
                    description_paragraphs.append(text)
    
    introduction = "\n\n".join(introduction_paragraphs)
    description = "\n\n".join(description_paragraphs)
    return introduction, description

def main():
    input_file = "../data/plants.json"   # JSON file containing the plant objects.
    output_dir = "../data/plant_details" # Directory where individual JSON files will be saved.
    
    # Create the output directory if it doesn't exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load the plant objects.
    with open(input_file, "r", encoding="utf-8") as f:
        plants = json.load(f)
    
    # Process each plant.
    for plant in plants:
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
                introduction, description = extract_intro_and_desc(html_content)
                plant_details = {
                    "species": species,
                    "link": link,
                    "introduction": introduction,
                    "description": description
                }
                filename = sanitize_filename(species) + ".json"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "w", encoding="utf-8") as outfile:
                    json.dump(plant_details, outfile, indent=4)
                print(f"Saved details to {filepath}")
            else:
                print(f"Failed to fetch {link}. HTTP status: {response.status_code}")
        except Exception as e:
            print(f"Error fetching {link}: {e}")

if __name__ == "__main__":
    main()