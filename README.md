# WetLabApp

Application to assist in research & lab work!
Created with Python using the Kivy framework with Peewee ORM.

![example](./media/example.png)

## Motivation

Solution calculators exist, but they typically require being able to control the mass of the solute. Since we weren't able to control that parameter, I created a GUI application that could give the volume needed for a solution knowing the desired concentration and mass of the solute. I realized I really liked programming quickly after, and started adding other features just to extend the project in my free time.

## Demo

#### Making a New Solution
![make new solution .gif](./media/example_solvent.gif)

#### Dynamic Data Fields
![resize menu .gif](./media/example_menu_resize.gif)

#### Create and Read
![create and read .gif](./media/create_read.gif)

#### Update
![update .gif](./media/update.gif)

#### Delete
![delete .gif](./media/delete.gif)

## Technology Used

- Python
- Kivy framework
- Peewee ORM
- SQLite

## Features

- calculation of volume needed for making solutions of a certain concentration
- calculation of film thickness (approximation assuming uniform thickness, only accurate for dropcast films)
- CRUD capabilities with solvents and materials

## Installation

#### Ubuntu

clone the repo and cd into it

`$ clone https://github.com/Svaught598/WetLabApp wetlabapp && cd ./wetlabapp`

in a terminal:

```
$ sudo add-apt-repository ppa:kivy-team/kivy
$ sudo apt-get update
$ sudo apt-get install python3-kivy

# This one is a dependency, but isn't installed by apt-get for some reason
$ sudo apt-get install xclip xsel
```

activate the env, and install requirements

```
$ source ./env/bin/activate
$ sudo python3 ./env/bin/pip3 install -r requirements.txt
```

then just run the Main.py file!

`python3 Main.py`
