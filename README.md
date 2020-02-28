## MaterialSolution

Open source cross-platform application to assist in research & lab work!
Created with Python using the Kivy framework with Peewee ORM.

Research in Materials Science require performing tedious approximations/calculations for:
- solution concentration
- film thickness
- inter-particle spacing
- etc. 
The purpose of this app is to speed-up the tedious tasks associated with experimental work.

Some applications exist that offer similar functionality, but differ in key ways:

1. Applications to assist with creating new solutions calculate the amount of compound needed for a solution. With nothing more than digital scales, it is VERY difficult to obtain a precise amount of material. Instead, this application uses an arbitrary amount of compound and calculates the amount of solvent needed for a given concentration.

2. In materials science, it is often necesary to make simple order of magnitude estimations based on physical models. These can be error-prone and usually take a decent amount of time to calculate. No other application makes these estimates.

3. Some types of solutions require knowledge of certain properties held by the solvent/material being used. Other applications use a text entry to incorporate these parameters. Using text-entry can sometimes lead to an incorrect assumption of units being used, and requires that the user have knowledge of these properties (knowledge they might not have). Since most solutions use common solvents/materials within a department, this application offers CRUD of materials and solvents - along with their properties - to a local SQLite database. This ensures that research groups can make quick and effective calculations while preserving any confidential data related to materials used.\

At the time of writing (02/25/20), the project is a work in progress.

## Project Goal

The 'Completed' version of this project should include several features (bold means complete):
- **tool to calculate volume needed for making new solutions**
- tool to calculate film thickness with at least one theoretical model
- tool to calculate intermolecular distance of particles in a thin film
- tool to calculate dilutions
- **CR**UD with solvents/materials/compounds

Some features that may be useful/interesting to complete:
- automatic calculation of molecular weight based on chemical formula in CRUD display
- incorporating PubChem API

## Old Project

I included this to serve as a reminder of what this project almost remained. Some points:

1. The project had a lot of unnecesary customized widgets, leading to overcomplication.

2. The logic was deeply tied to UI code, so technical changes were difficult to implement.

3. CRUD for solvent data was utterly broken. Deleting a selected entry would actually delete two.

All code is bad, but that means it can be better.