import tkinter as tk
import urllib3
from PIL import Image, ImageTk
from io import BytesIO
import pypokedex as pokedex

def capitalize_string(string: str) -> str:
    return ' '.join([word.capitalize() for word in string.split('-')])

def get_pokedex_info(pokemon: pokedex.pokemon.Pokemon):
    info = f'Name: {capitalize_string(pokemon.name)}\n\n'
    info += f'Height: {pokemon.height}\n'
    info += f'Weight: {pokemon.weight}\n\n'

    for i, type in enumerate(pokemon.types, 1):
        info += f'Type {i}: {capitalize_string(type)}\n'

    info += '\n'

    for i, ability in enumerate(pokemon.abilities, 1):
        hidden = ' (Hidden)' if ability.is_hidden else ''
        info += f'Ability {i}: {capitalize_string(ability.name)}{hidden}\n'

    info += '\n'
    info += f'Base HP: {pokemon.base_stats.hp}\n'
    info += f'Base Attack: {pokemon.base_stats.attack}\n'
    info += f'Base Defense: {pokemon.base_stats.defense}\n'
    info += f'Base Special Attack: {pokemon.base_stats.sp_atk}\n'
    info += f'Base Special Defense: {pokemon.base_stats.sp_def}\n'
    info += f'Base Speed: {pokemon.base_stats.speed}\n'
    if pokemon.base_experience is not None:
        info += f'Base Experience: {pokemon.base_experience}\n\n'
    else:
        info += 'No Base Experience\n\n'
    
    return info

def search_pokemon(event=None):
    try:
        dexnum = int(entry.get())
        if dexnum < 1 or dexnum > 1017:
            result_label.config(text='Invalid Pokédex Number!', fg='red')
            pokemon_image_def.config(image=None)
            pokemon_image_def.image = None
            pokemon_image_shiny.config(image=None)
            pokemon_image_shiny.image = None
        else:
            pokemon = pokedex.get(dex=dexnum)
            result_label.config(text=get_pokedex_info(pokemon), fg='black')
            show_sprites(pokemon)
    except:
        result_label.config(text='Not a Number!', fg='red')
        pokemon_image_def.config(image=None)
        pokemon_image_def.image = None
        pokemon_image_shiny.config(image=None)
        pokemon_image_shiny.image = None

def show_sprites(pokemon: pokedex.pokemon.Pokemon):
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', pokemon.sprites.front.get('default'))
        responseShiny = http.request('GET', pokemon.sprites.front.get('shiny'))
        default = Image.open(BytesIO(response.data))
        shiny = Image.open(BytesIO(responseShiny.data))
        defImg = ImageTk.PhotoImage(default)
        shnImg = ImageTk.PhotoImage(shiny)

        pokemon_image_def.config(image=defImg)
        pokemon_image_def.image = defImg
        pokemon_image_shiny.config(image=shnImg)
        pokemon_image_shiny.image = shnImg
    except:
        pokemon_image_def.config(image=None)
        pokemon_image_def.image = None
        pokemon_image_shiny.config(image=None)
        pokemon_image_shiny.image = None

window = tk.Tk()
window.title("Pokédex")
window.configure(bg='light blue')
window.geometry(f"500x700+{window.winfo_screenwidth() // 2 - 250}+{window.winfo_screenheight() // 2 - 350}")

label = tk.Label(window, text="Enter Pokédex Number (1-1017):")
label.configure(bg='light blue', fg='black')
label.pack()

entry = tk.Entry(window)
entry.configure(fg='white')
entry.pack()
entry.bind("<Return>", search_pokemon)

search_button = tk.Button(window, text="Search", command=search_pokemon)
search_button.configure(bg='light blue', fg='black')
search_button.pack()

result_label = tk.Label(window, text="", justify="center")
result_label.configure(bg='light blue', fg='black')
result_label.pack()

pokemon_image_def = tk.Label(window, justify='left')
pokemon_image_def.configure(bg='light blue')
pokemon_image_def.pack()

pokemon_image_shiny = tk.Label(window, justify='right')
pokemon_image_shiny.configure(bg='light blue')
pokemon_image_shiny.pack()

window.mainloop()