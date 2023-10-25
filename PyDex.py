import tkinter as tk
from urllib3 import PoolManager
from PIL import Image, ImageTk
from io import BytesIO
import pypokedex as pokedex

def set_images(none: bool, *, defImg, shnImg):
    pokemon_image_def.config(image=defImg if not none else None)
    pokemon_image_def.image = defImg if not none else None
    pokemon_image_shiny.config(image=shnImg if not none else None)
    pokemon_image_shiny.image = shnImg if not none else None

def capitalize_string(string: str) -> str:
    return ' '.join(word.capitalize() for word in string.split('-'))

def get_pokedex_info(pokemon: pokedex.pokemon.Pokemon) -> str:
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
    info += f'Base Stat Total: {pokemon.base_stats.hp + pokemon.base_stats.attack + pokemon.base_stats.defense + pokemon.base_stats.sp_atk + pokemon.base_stats.sp_def + pokemon.base_stats.speed}\n\n'
    info += f'Base Experience: {pokemon.base_experience}\n\n' if pokemon.base_experience is not None else 'No Base Experience\n\n'
    
    return info

def search_pokemon(event=None):
    try:
        dexnum = int(entry.get())
        if dexnum < 1 or dexnum > 1017:
            result_label.config(text='Invalid Pokédex Number!', fg='red')
            set_images(none=True, defImg=None, shnImg=None)
        else:
            pokemon = pokedex.get(dex=dexnum)
            result_label.config(text=get_pokedex_info(pokemon), fg='black')
            show_sprites(pokemon)
    except:
        result_label.config(text='Not a Number!', fg='red')
        set_images(none=True, defImg=None, shnImg=None)

def show_sprites(pokemon: pokedex.pokemon.Pokemon):
    try:
        response = PoolManager().request('GET', pokemon.sprites.front.get('default'))
        responseShiny = PoolManager().request('GET', pokemon.sprites.front.get('shiny'))
        default = Image.open(BytesIO(response.data))
        shiny = Image.open(BytesIO(responseShiny.data))
        defImg = ImageTk.PhotoImage(default)
        shnImg = ImageTk.PhotoImage(shiny) 
        set_images(none=False, defImg=defImg, shnImg=shnImg)
    except:
        set_images(none=True, defImg=None, shnImg=None)

window = tk.Tk()
window.title("Pokédex")
window.configure(bg='light blue')
window.geometry(f"500x700+{window.winfo_screenwidth() // 2 - 250}+{window.winfo_screenheight() // 2 - 350}")

label = tk.Label(window, text="Enter Pokédex Number (1-1017):", bg='light blue', fg='black')
label.pack()

entry = tk.Entry(window, fg='white')
entry.pack()
entry.bind("<Return>", search_pokemon)

search_button = tk.Button(window, text="Search", command=search_pokemon, bg='light blue', fg='black')
search_button.pack()

result_label = tk.Label(window, text="", justify="center", bg='light blue', fg='black')
result_label.pack()

pokemon_image_def = tk.Label(window, bg='light blue')
pokemon_image_def.pack()

pokemon_image_shiny = tk.Label(window, bg='light blue')
pokemon_image_shiny.pack()

window.mainloop()
