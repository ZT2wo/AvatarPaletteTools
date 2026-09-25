import palette_util as util

def unlock_all_palettes(character_files) -> None:
  for character in character_files:
    changes_made = False
    for palette in character.palettes:
      if palette.is_locked:
        palette.set_lock_flag(False)
        changes_made = True
        print(f"Unlocked palette {palette.marker.group(2).decode('utf-8')} in {character.path.name}")
    if changes_made:
      character.save_file()


def main():
  character_files = util.load_character_files()
  if len(character_files) == 0:
    input("Press Enter to Exit...")
    return
  choice = input("Do you wish to unlock all (Non-DLC) palettes? y/n : ")
  if choice.lower() in ["y", "yes"]:
    unlock_all_palettes(character_files)
    return

if __name__ == "__main__":
  main()