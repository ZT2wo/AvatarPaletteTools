import palette_util as util
from pathlib import Path
import json

palette_json = {
  "editableRgb": []
}
material_json = {
  "row": 0,
  "shadow": [
    0,0,0
  ],
  "midtone": [
    0,0,0
  ],
  "highlight": [
    0,0,0
  ]
}

path_to_defaults = "palettes_to_inject/defaults"

def extract_palettes(character_files):
  character: util.CharacterFile
  for character in character_files:
    palettes_extracted = 0
    character_folder = Path(path_to_defaults).joinpath(character.name)
    if not character_folder.is_dir():
      character_folder.mkdir( )
    if character_folder.is_dir():
      palette : util.Palette
      for palette in character.palettes:
        if palette.slot_id == "color1" or palette.slot_id == "gold": continue #skip ignorable entries
        palette_file_path = character_folder.joinpath(f'{palette.slot_id}.json')
        with palette_file_path.open("w") as palette_file:
          collected_palette = palette_json.copy()
          material : util.Material
          for index, material in enumerate(palette.materials):
            collected_material = material_json.copy()
            collected_material["row"] = index
            collected_material["shadow"] = material.color1.get_color()
            collected_material["midtone"] = material.color2.get_color()
            collected_material["highlight"] = material.color3.get_color()
            collected_palette["editableRgb"].append(collected_material)
          palette_file.write(json.dumps(collected_palette))
    print(f'Extracted {palettes_extracted} palettes for {character.name}')

def main() -> None:
  character_files = util.load_character_files()

  if len(character_files) == 0:
    input("Press Enter to Exit...")
    return
  
  choice = input("Do you wish to extract current palettes? y/n : ")

  if choice.lower() in ["y", "yes"]: extract_palettes(character_files)

  input("Press Enter to Exit...")
  return


if __name__ == "__main__":
  main()