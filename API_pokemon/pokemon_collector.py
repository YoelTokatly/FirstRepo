import json
import random
import requests
import os
from datetime import datetime

class PokemonCollector:
    def __init__(self, db_filename='pokemon_collection.json'):
        self.db_filename = db_filename
        self.pokeapi_base_url = 'https://pokeapi.co/api/v2/'
        self.collection = self.load_collection()
    
    def load_collection(self):
        """Load existing collection from JSON file"""
        if os.path.exists(self.db_filename):
            try:
                with open(self.db_filename, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Error reading collection file. Starting with empty collection.")
                return {}
        return {}
    
    def save_collection(self):
        """Save collection to JSON file"""
        with open(self.db_filename, 'w') as file:
            json.dump(self.collection, file, indent=4)
    
    def get_pokemon_list(self):
        """Get list of all Pokémon from PokeAPI"""
        try:
            response = requests.get(f"{self.pokeapi_base_url}pokemon?limit=1000")
            response.raise_for_status()
            data = response.json()
            return data['results']
        except requests.RequestException as e:
            print(f"Error fetching Pokémon list: {e}")
            return []
    
    def get_pokemon_details(self, pokemon_name):
        """Get detailed information about a specific Pokémon"""
        try:
            response = requests.get(f"{self.pokeapi_base_url}pokemon/{pokemon_name}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Pokémon details: {e}")
            return None
    
    def format_pokemon_data(self, pokemon_data):
        """Format Pokémon data with selected attributes"""
        # Extract abilities
        abilities = [ability['ability']['name'] for ability in pokemon_data['abilities']]
        
        # Extract types
        types = [ptype['type']['name'] for ptype in pokemon_data['types']]
        
        # Extract stats
        stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
        
        return {
            'name': pokemon_data['name'],
            'id': pokemon_data['id'],
            'height': pokemon_data['height'],
            'weight': pokemon_data['weight'],
            'types': types,
            'abilities': abilities,
            'stats': stats,
            'base_experience': pokemon_data.get('base_experience', 'Unknown'),
            'caught_at': datetime.now().isoformat()
        }
    
    def display_pokemon(self, pokemon_data, is_new=True):
        """Display Pokémon information nicely to the user"""
        print("\n" + "="*50)
        if is_new:
            print(f"🌟 NEW POKÉMON CAUGHT! 🌟")
        else:
            print(f"📋 POKÉMON ALREADY IN COLLECTION 📋")
        
        print("="*50)
        print(f"Name: {pokemon_data['name'].title()}")
        print(f"ID: #{pokemon_data['id']}")
        print(f"Height: {pokemon_data['height']/10} m")
        print(f"Weight: {pokemon_data['weight']/10} kg")
        print(f"Types: {', '.join(pokemon_data['types']).title()}")
        print(f"Abilities: {', '.join(pokemon_data['abilities']).title()}")
        print(f"Base Experience: {pokemon_data['base_experience']}")
        
        print("\nBase Stats:")
        for stat_name, stat_value in pokemon_data['stats'].items():
            print(f"  {stat_name.title()}: {stat_value}")
        
        print(f"\nCaught on: {pokemon_data['caught_at']}")
        print("="*50 + "\n")
    
    def run(self):
        """Main program loop"""
        print("Welcome to the Pokémon Collector!")
        print("="*30)
        
        while True:
            user_input = input("\nWould you like to draw a Pokémon? (yes/no): ").lower().strip()
            
            if user_input in ['yes', 'y']:
                print("\nFetching Pokémon list...")
                pokemon_list = self.get_pokemon_list()
                
                if not pokemon_list:
                    print("Could not fetch Pokémon list. Please try again.")
                    continue
                
                # Choose random Pokémon
                random_pokemon = random.choice(pokemon_list)
                pokemon_name = random_pokemon['name']
                
                print(f"\nYou drew: {pokemon_name.title()}!")
                
                # Check if Pokémon is already in collection
                if pokemon_name in self.collection:
                    print(f"{pokemon_name.title()} is already in your collection!")
                    self.display_pokemon(self.collection[pokemon_name], is_new=False)
                else:
                    print(f"Catching {pokemon_name.title()}...")
                    pokemon_details = self.get_pokemon_details(pokemon_name)
                    
                    if pokemon_details:
                        # Format and save Pokémon data
                        formatted_data = self.format_pokemon_data(pokemon_details)
                        self.collection[pokemon_name] = formatted_data
                        self.save_collection()
                        
                        self.display_pokemon(formatted_data, is_new=True)
                        print(f"✅ {pokemon_name.title()} has been added to your collection!")
                        print(f"You now have {len(self.collection)} Pokémon in your collection.")
                    else:
                        print(f"Could not fetch details for {pokemon_name}. Please try again.")
                
            elif user_input in ['no', 'n']:
                print("\n👋 Thanks for playing Pokémon Collector!")
                print(f"You collected {len(self.collection)} Pokémon in total.")
                print("See you next time, Trainer! Gotta catch 'em all! 🎮")
                break
            
            else:
                print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    collector = PokemonCollector()
    collector.run()
