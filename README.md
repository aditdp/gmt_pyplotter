# GMT_Pyplotter

Python scripts for plotting maps with generic mapping tools in interactive command line interface.

## What is GMT

Generic Mapping Tools (GMT) is an open source collection of about 100 command-line tools for manipulating geographic and Cartesian data sets (including filtering, trend fitting, gridding, projecting, etc.) and producing high-quality illustrations ranging from simple x-y plots via contour maps to artificially illuminated surfaces, 3D perspective views and animations. The GMT supplements add another 50 more specialized and discipline-specific tools. This program can be running either as Command Line Interface (CLI) or as a script code.

### Complication

* not beginer friendly
* steep learning curve with the GMT

* Prone typing error when inputing commands or parameters
* time consuming when creating the script (trial and error)

## GMT_Pyplotter

Just type the parameters

Interactive command line interface

working in windows, linux or macOS

### Structure of the script

In the begining of the script, the GMT program is check for the installation location and the version match the required specification.

The MainMap class is inherit Layer class in which also inherit from the basic parameter class (FileName, Coordinate, Projection)

The MainMap class only contain method for printing general parameter and layers information to the screen

The Layer class determine the order of the layers, layers name, layers gmt script and downloading required data base on the user requested.

The general parameter class (FileName, Coordinate, Projection) filling the main information of the maps, self explanatory.

### Available layers

1. Coastal line
2. Earth relief
3. Contour line
4. Earthquake plot
5. Focal Mechanism plot
6. Indonesia regional tectonic plot
7. Map inset

### How it's work

The

Current feature

Creating a geographical map with mercators projection

Support up to 6 layers

### How to use

In the terminal type the command:

```python
python gmt_pyplotter
```

Then input the required parameter based on the map to be generate

## Requirements

* Generic Mapping Tools version >= 6.4.0
* Python version >= 3.10

## Installation

Make sure the required apps already installed.

Navigate to the downloaded installation folder with terminal and enter the following command:

```python
pip install .
```

## License

Copyright (c) 2024 by *BRIN* (*Badan Riset dan Inovasi Nasional* / National Research and Innovation Agency of Indonesia)
