from pathlib import Path
import re

character_paks = [
  "aang",
  "azula",
  "katara",
  "korra",
  "korra_nightmare",
  "kyoshi",
  "ozai",
  "sokka",
  "toph",
  "zaheer",
  "zuko"
]

class Color:
  def __init__(self, color_pos, character_file) -> None:
    self.color_pos = color_pos
    self.character_file = character_file

    self.r = None
    self.g = None
    self.b = None
    self.a = None
    self.float_tuple = None


    self.read_color()

  def as_float_tuple(self):
    return (self.r / 255.0, self.g / 255.0, self.b / 255.0, self.a / 255.0)
  def float_to_u32(self, float_tuple):
    return ((int(float_tuple[0] * 255.0)), (int(float_tuple[1] * 255.0)), (int(float_tuple[2] * 255.0)), (int(float_tuple[3] * 255.0)))

  def read_color(self) -> None:
    self.r = self.character_file.data[self.color_pos]
    self.g = self.character_file.data[self.color_pos + 1]
    self.b = self.character_file.data[self.color_pos + 2]
    self.a = self.character_file.data[self.color_pos + 3]
    self.float_tuple = self.as_float_tuple()
  def write_color(self) -> None:
    self.character_file.data[self.color_pos] = self.r
    self.character_file.data[self.color_pos + 1] = self.g
    self.character_file.data[self.color_pos + 2] = self.b
    self.character_file.data[self.color_pos + 3] = self.a

  def set_color(self, rgba) -> None:
    if len(rgba) != 4:
      raise ValueError(f"RGBA tuple must have 4 components, got {len(rgba)}")
    for component in rgba:
      if type(component) is not int:
        raise ValueError(f"RGBA components must be integers, got {type(component)}")
    self.r, self.g, self.b, self.a = rgba
    self.float_tuple = self.as_float_tuple()
    self.write_color()

  def get_color(self) -> tuple:
    return (self.r, self.g, self.b, self.a)

  def __str__(self) -> str:
    return f"Color(RGBA): ({self.r}, {self.g}, {self.b}, {self.a})"
#--------------------------------------------------------------------------------------------------
class Material:
  def __init__(self, material_pos, character_file) -> None:
    self.material_pos = material_pos
    self.character_file = character_file
    if not material_pos:
      raise ValueError("Material position cannot be None")

    self.color1 = None
    self.color2 = None
    self.color3 = None
    self.bloom_color = None
    self.read_material()

  def read_material(self) -> None:
    self.color1 = Color(self.material_pos, self.character_file)
    self.color2 = Color(self.material_pos + 4, self.character_file)
    self.color3 = Color(self.material_pos + 8, self.character_file)
    self.bloom_color = Color(self.material_pos + 12, self.character_file)
  def write_material(self) -> None:
    self.color1.write_color()
    self.color2.write_color()
    self.color3.write_color()
    self.bloom_color.write_color()

  def __str__(self) -> str:
    return f"Material Found | Colors - Color1: {self.color1}, Color2: {self.color2}, Color3: {self.color3}, Bloom Color: {self.bloom_color}"
#--------------------------------------------------------------------------------------------------
class Palette:
  def __init__(self, character_file, marker) -> None:
    self.character_file = character_file

    self.marker = marker #match groups 1: character name, 2: palette name, 3: end of path ascii
    self.marker_pos = marker.start()
    self.slot_id = str(marker.group(2)[len(marker.group(1))+1:-4].decode('utf-8'))

    self.unlock_flag_pos = self.marker_pos - 5  # Unlock flag is 5 bytes to the left of the palette marker
    self.is_locked = self.check_locked()

    self.materials = []

    self.read_palette()

  def set_lock_flag(self, state) -> None:#Locked is 0x01, unlocked is 0x00
    if 0 <= self.unlock_flag_pos < len(self.character_file.data):
      self.character_file.data[self.unlock_flag_pos] = 0x01 if state else 0x00
      self.is_locked = state

  def check_locked(self) -> bool:
    if 0 <= self.unlock_flag_pos < len(self.character_file.data):
      return self.character_file.data[self.unlock_flag_pos] == 0x01
    return False

  def read_palette(self) -> None:
    material_start_pos = self.marker.end() + 19  # Materials start 19 bytes after the end of path ascii
    for i in range(63):
      material_pos = material_start_pos + (i * 16)  # Each material is 16 bytes
      if material_pos < len(self.character_file.data):
        material = Material(material_pos, self.character_file)
        self.materials.append(material)
#--------------------------------------------------------------------------------------------------
class CharacterFile:
  def __init__(self, file_path) -> None:
    self.path = Path(file_path)
    self.name = self.path.stem
    self.data = bytearray(self.path.read_bytes())
    self.palettes = []

    self.find_palettes()

  def save_file(self, file_name = None) -> None:
    if file_name is None:
      file_name = self.path.name
    self.path.write_bytes(self.data)
    print(f"Saved modified character file: {file_name}")

  def get_palette_by_id(self, id) -> Palette:
    for palette in self.palettes:
      if palette.slot_id == id: return palette

  def find_palettes(self) -> None:
    palette_num = 1
    marker = re.compile(rb'!src/sprites\\([^\\]+)\\palettes\\([^\x00]+)\x00*([^\x00])') 
    for match in marker.finditer(self.data):#match groups 1: character name, 2: palette name, 3: end of path ascii

      if "colormap" in match.group(2).decode('utf-8'):
        continue  # Skip colormap palettes

      found_palette = Palette(self, match)
      #print(f"Found palette {palette_num}: {match.group(2).decode('utf-8')} in {self.path.name}")

      self.palettes.append(found_palette)
      palette_num += 1
#--------------------------------------------------------------------------------------------------

def load_character_files() -> list:
  character_files = []
  data_folder = Path("data_packages")
  if not data_folder.exists():
    print("Data folder 'data_packages' not found. Is script running in the correct directory?")
    return character_files

  for file in data_folder.glob("*.pak"):
    if file.stem not in character_paks:
      #print(f'Skipped {file.name}')
      continue
    character = CharacterFile(file)
    if len(character.palettes) < 1:
      continue  # Skip files with no palettes
    character_files.append(character)
    print(f"Character file: {file.name} - {len(character.palettes)} Palette(s) found")
  return character_files