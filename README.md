# Ellie's AI-generated data tracking app

## Overview
A better journaling and data tracking app.

## Short term goals
- I want data to be stored in a SQLite database
- I want the table that stores the types of data being collected to look like the following:
    - key: auto-increment unique ID
    - label: Human readable label presented to user
    - data_type: One of: `int`, `date`, or `text`
    - int_max: If the data type is `int`, the user is asked if a max int value should be specified
    - int_min: If the data type is `int`, the user is asked if a minimum int value should be specified
    - prompt: The question presented to the user when they run the program
- I want the table that stores the actual data to look like the following:
    - key: auto-increment unique ID
    - data_type_id: Foreign key pointing to the `key` value in the `data_types` table
    - int_val: The integer value, if the data is of `int` type
    - date_val: The date value, if the data is of `date` type
    - text_val: The text, if data is of type `text`
    - created: Time/date stamp of when the record was inserted
    - last_updated: Time/date stamp of when the record was last updated/edited
- I want to have one command line program
    - If run with --config, it will ask the user to add a new data type
    - If run with --list-data-types, it will display all the contents of the `data_types` table
