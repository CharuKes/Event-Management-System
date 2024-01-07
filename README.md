# Event Management System
  ![Snippet](https://github.com/CharuKes/Event-Management-System/blob/master/Data/1%20(1).JPG)

This is a simple Event Management System implemented in Python. The system allows users to create, edit, delete events, manage attendees, and store event data in a JSON file (`event.json`). 

## Table of Contents

- [Overview](#overview)
- [Classes](#classes)
  - [EventManager (Abstract Base Class)](#eventmanager-abstract-base-class)
  - [EventManagerWithLogging (Concrete Subclass of EventManager)](#eventmanagerwithlogging-concrete-subclass-of-eventmanager)
- [How to Use](#how-to-use)
- [File Handling](#file-handling)
- [Logging](#logging)
- [Error Handling](#error-handling)
- [Confluence Page](#confluence)

## Overview

This repository contains a Python implementation of an Event Management System. Users can perform various operations related to events and attendees through a command-line interface.

## Classes

### EventManager (Abstract Base Class)

- **Purpose**: Provides a basic structure for event management.
- **Methods**:
  - `list_events`: Lists all events.
  - `create_event`: Creates a new event.
  - `edit_event`: Edits an existing event.
  - `delete_event`: Deletes an event.
  - `add_attendee`: Adds an attendee to an event.
  - `list_attendees`: Lists attendees for a specific event.
  - `delete_attendee`: Deletes an attendee from an event.

### EventManagerWithLogging (Concrete Subclass of EventManager)

- **Purpose**: Adds logging functionality to EventManager.
- **Methods**:
  - `__init__`: Initializes the class with a specified filename and log file.
  - `abstract_property`: Concrete implementation of the abstract property.
  - `abstract_property.setter`: Concrete implementation of the abstract property setter.
  - `abstract_method`: Concrete implementation of the abstract method.
  - `_log`: Logs a message to the log file.
  - `_log_event_operation`: Logs an event operation.
  - `_log_attendee_operation`: Logs an attendee operation.
  - `_print_event_details`: Prints event details.

## How to Use

1. Run the script (`asmt.py`) in your Python environment.
   
    ![Snippet](https://github.com/CharuKes/Event-Management-System/blob/master/Data/git%20(1).JPG)
3. Choose an option from the menu (1 to 8) to perform the desired operation.
4. Follow the prompts to input information for creating, editing, or deleting events.

## File Handling

- Event data is stored in `event.json`.

## Logging

- Logging is performed using the `event_log.txt` file. Each operation is recorded, including events and attendees.

## Error Handling

- The program handles errors gracefully and prompts the user to enter valid input.

## Confluence
- [Confluence](https://charukesarwani.atlassian.net/l/cp/y1HAS70B)
