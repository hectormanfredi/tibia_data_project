import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_experience_table(character_name):
    """
    Fetches the larger experience table for a given character name from the GuildStats website.

    Parameters:
    character_name (str): The name of the character to fetch the table for.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the experience table.
    """
    # Format the character name for the URL
    formatted_name = character_name.replace(" ", "+")
    url = f'https://guildstats.eu/character?nick={formatted_name}&tab=9&predict=450'

    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    # Send the request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all tables on the page
        tables = soup.find_all('table')
        
        # Extract the desired table (assuming it's the second one)
        if len(tables) > 1:  # Ensure the table exists
            table_html = str(tables[1])  # Convert the second table to a string
            
            # Convert the HTML table to a pandas DataFrame
            df = pd.read_html(table_html)[0]
            return df
        else:
            raise ValueError("Desired table not found on the page.")
    else:
        raise ConnectionError(f"Failed to fetch the page. Status code: {response.status_code}")

# Example usage
try:
    character_name = "kin freezetime"
    experience_table = get_experience_table(character_name)
    print(experience_table.head())
except Exception as e:
    print(f"An error occurred: {e}")
