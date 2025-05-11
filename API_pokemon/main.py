import requests
import pandas as pd
import random as rd
import json

def main(BASE_URL):
    user_answer = input(' would like to draw a Pokémon? (y/n)')
    if user_answer in 'y':
        drew_a_card(BASE_URL)
    



def drew_a_card(BASE_URL):
    ENDPOINT = "pokemon/"
    data = api_get(BASE_URL,ENDPOINT)
    # print(df_data['name'])
    df_data = pd.DataFrame(data['results'])
    rndom_pok = df_data.sample(n=1).iloc[0].to_dict() 
    # rd.randint(0,df_data['name'].count())

    # new_base =  df.sample(n=1).iloc[0].to_dict() str(rndom_pok['url'])
    # print(rndom_pok['url'])
    data2 = api_get(rndom_pok['url'],"")
    print( '#############')
    print(f'name: {data2['name']}')
    print(f'height: {data2['height']}')
    print(f'weight: {data2['weight']}')
    print(f'base_experience: {data2['base_experience']}')
    print(f'order: {data2['order']} ')
    print( '#############')

    basic_info = {
        'id': data2['id'],
        'name': data2['name'],
        'height': data2['height'],
        'weight': data2['weight'],
        'base_experience': data2['base_experience'],
        'order': data2['order']
    }

    # basic_df = pd.DataFrame([basic_info])
    # print(basic_df)

    # new_pokemon = {}
    # new_pokemon['name'] = rndom_pok['name']
    # new_pokemon["url"] = rndom_pok['url']

    



    # with open('pokemons.json', 'w') as file:
    #     json.dump(data, file, indent=4)


    
    # #     json.dump(new_pokemon, file, indent=4)
    # # df_data
    # # rndom_pok
    # print( rndom_pok['url'])
    
   


def api_get(BASE_URL,ENDPOINT):
    response = requests.get(f'{BASE_URL}{ENDPOINT}')
    print(response)     
    data = response.json()
    return data
    




if __name__ == "__main__":
    BASE_URL="https://pokeapi.co/api/v2/"
    # CATEGORY = "gender"
    main(BASE_URL)


    # https://pokeapi.co/api/v2/pokemon/ditto
