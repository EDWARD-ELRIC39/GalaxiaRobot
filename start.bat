@echo off
TITLE Galaxia Robot 
:: Enables virtual env mode and then starts Galaxia 

env\scripts\activate.bat && py -m GalaxiaRobot 
