from pathlib import Path
import palette_util as util
import json

def batch_inject_palettes(character_files) -> None:
  inject_folder = Path("palettes_to_inject")
  for character in character_files:
    palettes_injected = 0
    character_folder = inject_folder.joinpath(character.name)
    if character_folder.is_dir():
      print(f'Folder found: {character_folder}')
      for palette in character.palettes:
        if palette.slot_id == "color1" or palette.slot_id == "gold": continue #skip ignorable entries
        palette_file_path = character_folder.joinpath(f'{palette.slot_id}.json')
        if palette_file_path.exists():
          palette_file = palette_file_path.read_bytes()
          palette_json = json.loads(palette_file)
          for json_material in palette_json["editableRgb"]:
            mat_to_edit = palette.materials[json_material["row"]]
            mat_to_edit.color1.set_color(json_material["shadow"] + [255])
            mat_to_edit.color2.set_color(json_material["midtone"] + [255])
            mat_to_edit.color3.set_color(json_material["highlight"] + [255])
          palettes_injected += 1
      print(f'Injected {palettes_injected} palettes for {character.name}')
      if palettes_injected > 0: character.save_file()
    else:
      print(f'Folder for character: {character.name} not found')
    


def main() -> None:
  character_files = util.load_character_files()
  if len(character_files) == 0:
    input("Press Enter to Exit...")
    return
  choice = input("Do you wish to inject local palettes? y/n : ")
  if choice.lower in ["y", "yes"]:
    batch_inject_palettes(character_files)
    return
  else:
    return

if __name__ == "__main__":
  main()