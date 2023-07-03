# glove80KeymapFormatter

This is a Formatter for .keymap file of glove80.

This formatter affects only the part of the code that describes the layer.

## Befor
![before](https://github.com/shinamon610/glove80KeymapFormatter/assets/76248816/56853cfc-38d1-4002-97f5-e8ce7eab971d)

## After
![after](https://github.com/shinamon610/glove80KeymapFormatter/assets/76248816/1dda9b3e-7f46-4c4b-8542-a42b58c65c6a)

# How to use?
1. git clone this repo.
2. Create config.txt in this repo.
3. Write the absolute path of the original .keymap file in the first line of config.txt
4. Write the path that outputs the formatted .keymap file on the second line of config.txt. If you want to overwrite the original .keymap, write the same path as the first line.
5. Execute keymap_formatter.py
  
  ```
   python3 keymap_formatter.py
   ```
