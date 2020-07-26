# WetLabApp

Application to assist in research & lab work!
Created with Python using the Kivy framework with Peewee ORM.

## Motivation

Solution calculators exist, but they typically require being able to control the mass of the solute. Since we weren't able to control that parameter, I created a GUI application that could give the volume needed for a solution knowing the desired concentration and mass of the solute. I realized I really liked programming quickly after, and started adding other features just to extend the project in my free time.

## Screenshots

Coming soon!

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

Coming soon!

## Old Project

I included this to folder serve as a reminder of what this project started as:

1. The project had a lot of unnecesary customized widgets, leading to overcomplication.

2. The logic was deeply tied to UI code, so technical changes were difficult to implement.

3. CRUD for solvent data was utterly broken. Lots of edge cases weren't considered.

I fixed these points by incorporating an ORM and object models for data, and refactoring the codebase into the MVVM architecture. 
