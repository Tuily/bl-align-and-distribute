# Align and Distribute Tools

<img width="185" alt="ALIGN-AND-DISTRIBUTE-ADD-ON-ACTIVE" src="https://user-images.githubusercontent.com/9062786/226108983-4b76dc59-cf81-4583-88d1-65c9a35ad56c.png">

Align and Distribute Tools is a free Blender add-on, as the name says, created to make aligning and distributing objects easier.

Features:

- Align object location
- Distribute objects evenly
- Distribute objects using a fixed spacing

## How to install

Check the instalation instructions [here](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html#installing-add-ons)

## How to use

- Aligning objects
  - Select at least two objects
  - Select the [active object](https://docs.blender.org/manual/en/latest/scene_layout/object/selecting.html#selections-and-the-active-object) ( the algorithm will align the objects based on this one).
  - Click on one of the alignment options `X`, `Y` or `Z`
- Distribute objects evenly
  - Select at least three objects
  - Click on one of the distribute evenly options `X`, `Y` or `Z`
    - In this mode, the algorithm will distribute the objects evenly between first and the last element
- Distribute objects using a fixed spacing (experimental)
  - Select at least two objects
  - Select the [active object](https://docs.blender.org/manual/en/latest/scene_layout/object/selecting.html#selections-and-the-active-object) ( the algorithm will distribute the objects starting from this one).
  - Adjust the spacing (gap field)
    - Positive or negative values are accepted
  - Click on one of the distribute with gap options, `X`, `Y`, or `Z`.
  - There are a few edge cases were the order is messed up.

## Known issues

- Undo does not work on some cases

## Demo

https://user-images.githubusercontent.com/9062786/226111783-fd2bb540-8e4d-4a81-b694-609fbee42259.mov

## Contributing

Found a bug? Have any feedback? Feel free to open an [issue](https://github.com/Tuily/bl-align-and-distribute/issues)
