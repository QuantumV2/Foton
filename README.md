# Foton

## Overview
Foton is a very simple esolang/cellular automaton themed around light beams.

## Usage
1. Run `pip install -r requirements.txt`.
2. Run main.py and pass in the path to the program you want to run as an argv.

## Commands

    /, \	Reflect beam
    +	Split beam into two
    #	Absorb beam
    $D	Emit a beam when a beam touches it
    *D	Emit beam (D = direction)
    1, 0	Sensor: Toggle on hit
    u,n,[,]	Emit a beam if the sensor behind it is 1  (for example 1[ )
    !	Skip instruction 


    <,>,^,V - Two mirrors in one character (for example going into a > from above or bottom will do what you expect but going forwards will make it reflect two times (180 degrees) and going backwards will do nothing)

    Beams colliding means they get destroyed
