import json
import os
from datetime import datetime
from abc import ABC, abstractmethod
import logging

# Define custom exceptions for the Event Manager
class EventManagerException(Exception):
    def __init__(self, message="Event Manager Exception"):
        super().__init__(message)


class InvalidInputException(EventManagerException):
    def __init__(self, message="Invalid Input Exception"):
        super().__init__(message)

# Function to validate user input
def validate_input(prompt, validate_func):
    while True:
        user_input = input(prompt)
        if validate_func(user_input):
            return user_input
        else:
            print(f"Invalid input please enter valid input: {user_input}")

# Abstract base class for Event Manager
class AbstractEventManager(ABC):

    @abstractmethod
    def _load_events(self):
        pass

    @abstractmethod
    def _save_events(self, events):
        pass

    @abstractmethod
    def _print_event_details(self, event):
        pass

    @abstractmethod
    def list_events(self):
        pass

    @abstractmethod
    def create_event(self):
        pass

    @abstractmethod
    def edit_event(self):
        pass

    @abstractmethod
    def delete_event(self):
        pass

    @abstractmethod
    def add_attendee(self):
        pass

    @abstractmethod
    def list_attendees(self):
        pass

    @abstractmethod
    def delete_attendee(self):
        pass

# Concrete implementation of EventManager
class EventManager(AbstractEventManager):
    def __init__(self, filename):
        # Constructor for EventManager class
        self.filename = filename
        self._attendee_name = None

    @property
    def attendee_name(self):
        return self._attendee_name

    @attendee_name.setter
    def attendee_name(self, value):
        if isinstance(value, str):
            self._attendee_name = value
        else:
            raise ValueError("Attendee name must be a string")

    def _load_events(self):
        # Load events from a JSON file
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                # json.load reads JSON data from a file-like object and converts it into a Python object.
                events = json.load(file)
            return events
        else:
            return []

    def _save_events(self, events):
        # Save events to a JSON file
        with open(self.filename, 'w') as file:
            # json.dump takes a Python object and writes it to a file-like object in JSON format.
            json.dump(events, file, indent=2)

    def _print_event_details(self, event):
        # Print details of an event
        print(f'Event ID: {event.get("Event ID", 0)},')
        print(f'Event Name: "{event.get("Event Name", "")}",')
        print(f'Event Date: "{event.get("Event Date", "")}",')
        print(f'Event Location: "{event.get("Event Location", "")}",')
        print(f'Number of Attendees: {event.get("Number of Attendees", 0)},')
        print(f'Attendees: {event.get("Attendees", [])}\n')

    def list_events(self):
        # List all events
        events = self._load_events()

        if not events:
            print('There are no events. Press 2 to create a new event.')
        else:
            print("List the events in ascending order:\n")
            for event in sorted(events, key=lambda x: x.get('Event ID', 0)):
                self._print_event_details(event)

    def create_event(self):
        # Create a new event
        while True:
            try:
                events = self._load_events()

                event_id = input('Event ID: ')

                # Check if the entered event ID already exists
                if any(str(event.get('Event ID')) == event_id for event in events):
                    raise InvalidInputException(
                        f"Error: Event ID '{event_id}' already exists. Please choose another unique event ID.")
                if not event_id.isdigit():
                    raise InvalidInputException('Error: Event ID should be an integer')

                event_name = None

                while event_name is None or not event_name.isalpha():
                    event_name = input('Event Name: ')
                    if not event_name.isalpha():
                        print("Invalid input: Event name should only contain letters.")

                while True:
                    event_date = input('Event Date (YYYY-MM-DD): ')
                    try:
                        datetime.strptime(event_date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid input: Date format should be YYYY-MM-DD.")

                event_location = input('Event Location: ')

                number_of_attendees = validate_input('Number of Attendees: ', lambda x: x.isdigit())

                new_event = {
                    'Event ID': int(event_id),
                    'Event Name': event_name,
                    'Event Date': event_date,
                    'Event Location': event_location,
                    'Number of Attendees': int(number_of_attendees),
                    'Attendees': []
                }

                events.append(new_event)
                self._save_events(events)

                print('Event added')
                self._print_event_details(new_event)
                break
            except InvalidInputException as e:
                print(f'Invalid input: {e}. Please enter the correct value.')

    def edit_event(self):
        # Edit an existing event
        while True:
            try:
                events = self._load_events()

                event_id = input('Enter the Event ID to edit: ')

                editing_successful = False

                for event in events:
                    if str(event.get('Event ID')) == event_id:
                        event_name = input(f'Edit Event Name ({event["Event Name"]}): ')

                        while not event_name.isalpha():
                            print('Invalid Input: Event name should only contain letters.')
                            event_name = input(f'Edit Event Name ({event["Event Name"]}): ')

                        while True:
                            event_date = input(f'Edit Event Date ({event["Event Date"]}): ')
                            try:
                                datetime.strptime(event_date, "%Y-%m-%d")
                                break
                            except ValueError:
                                print("Invalid input: Date format should be YYYY-MM-DD.")

                        event_location = input(f'Edit Event Location ({event["Event Location"]}): ')

                        while True:
                            number_of_attendees = input(
                                f'Edit Number of Attendees ({event["Number of Attendees"]}): ')
                            try:
                                number_of_attendees = int(number_of_attendees)
                                break
                            except ValueError:
                                print("Invalid input: Number of attendees should be a valid integer.")

                        event.update({
                            'Event Name': event_name or event['Event Name'],
                            'Event Date': event_date or event['Event Date'],
                            'Event Location': event_location or event['Event Location'],

                            'Number of Attendees': number_of_attendees,
                            'Attendees': [] if number_of_attendees == 0 else event['Attendees']
                        })

                        self._save_events(events)
                        print('Event edited successfully.')
                        self._print_event_details(event)
                        editing_successful = True
                        break

                if editing_successful:
                    break
                else:
                    print('Event not found.')
            except InvalidInputException as e:
                print(f'Invalid input: {e}. Please enter the correct value.')

    def delete_event(self):
        # Delete an existing event
        events = self._load_events()

        user_input1 = validate_input('Enter the Event ID to delete: ', lambda x: x.isdigit())

        found = False  # Variable to track whether the event was found and deleted

        for event in events:
            if str(event.get('Event ID')) == user_input1:
                events.remove(event)
                self._save_events(events)
                print('Event deleted successfully.')
                self._print_event_details(event)
                found = True
                break

        if not found:
            print('Event not found.')

    def add_attendee(self):
        # Add an attendee to an event
        events = self._load_events()

        user_input1 = validate_input('Enter the Event ID to add an attendee: ', lambda x: x.isdigit())
        for event in events:
            if str(event.get('Event ID')) == user_input1:
                while True:
                    self.attendee_name = input('Enter Attendee Name: ')
                    if not self.attendee_name.isalpha():
                        print("Invalid input: Attendee name should only contain letters.")
                    else:
                        break

                event['Attendees'] = event.get('Attendees', []) + [self.attendee_name]
                event['Number of Attendees'] = len(event['Attendees'])  # Update the number of attendees
                self._save_events(events)
                print(f'Attendee "{self.attendee_name}" added to the event.')
                self._print_event_details(event)
                break
        else:
            print('Event not found.')

    def list_attendees(self):
        # List attendees of an event
        events = self._load_events()

        user_input1 = validate_input('Enter the Event ID to list attendees: ', lambda x: x.isdigit())
        for event in events:
            if str(event.get('Event ID')) == user_input1:
                attendees = event.get('Attendees', [])
                if not attendees:
                    print('There are no attendees for this event.')
                else:
                    print('List of Attendees:')
                    for attendee in attendees:
                        print(f'- {attendee}')
                break
        else:
            print('Event not found.')

    def delete_attendee(self):
        # Delete an attendee from an event
        events = self._load_events()

        user_input1 = validate_input('Enter the Event ID to delete an attendee: ', lambda x: x.isdigit())
        for event in events:
            if str(event.get('Event ID')) == user_input1:
                attendees = event.get('Attendees', [])
                if not attendees:
                    print('There are no attendees for this event..')
                else:
                    attendee_name = input('Enter the Attendee Name to delete: ')
                    if attendee_name in attendees:
                        attendees.remove(attendee_name)
                        event['Number of Attendees'] = len(attendees)  # Update the number of attendees
                        self._save_events(events)
                        print(f'Attendee "{attendee_name}" deleted from the event.')
                    else:
                        print(f'Attendee "{attendee_name}" not found for this event.')
                self._print_event_details(event)
                break
        else:
            print('Event not found.')


class EventManagerWithLogging(EventManager):
    def __init__(self, filename, log_file):
        # Constructor for EventManagerWithLogging class
        super().__init__(filename)
        self.log_file = log_file
        # Configure the logging system
        logging.basicConfig(filename=log_file, level=logging.INFO)

    def _log(self, message):
        # Log a message to the log file.
        logging.info(message)

    def _log_operation_closure(operation_type):
        # Closure for logging operations.
        def log_operation(func):
            def wrapper(*args, **kwargs):
                event_id = kwargs.get('event_id', '')
                attendee_name = kwargs.get('attendee_name', '')
                log_message = f'{operation_type} operation for event with ID {event_id}'

                if attendee_name:
                    log_message += f' and attendee {attendee_name}'

                args[0]._log(log_message)
                return func(*args, **kwargs)

            return wrapper

        return log_operation

    # decorator

    @_log_operation_closure('create')
    def create_event(self):
        super().create_event()

    @_log_operation_closure('edit')
    def edit_event(self):
        super().edit_event()

    @_log_operation_closure('delete')
    def delete_event(self):
        super().delete_event()

    @_log_operation_closure('add')
    def add_attendee(self):
        super().add_attendee()

    @_log_operation_closure('list')
    def list_attendees(self):
        super().list_attendees()

    @_log_operation_closure('delete')
    def delete_attendee(self):
        super().delete_attendee()

    def _log_event_operation(self, operation, event_id):
        # Log an event operation.
        self._log(f'{operation} event with ID {event_id}')

    def _log_attendee_operation(self, operation, event_id, attendee_name):
        # Log an attendee operation.
        self._log(f'{operation} attendee {attendee_name} for event with ID {event_id}')

    def _print_event_details(self, event):
        # Print event details and log them.
        super()._print_event_details(event)
        self._log(f'Details: {event}')


def main():
    while True:
        filename = 'event.json'
        log_file = 'event_log.txt'

        try:
            event_manager = EventManagerWithLogging(filename, log_file)

            while True:
                user_input = input('''1: List Event
2: Create Event
3: Edit Event
4: Delete Event
5: Add Attendee
6: List Attendees
7: Delete Attendee
8: Exit

Select one option: ''')

                try:
                    user_input = int(user_input)

                    if user_input == 1:
                        event_manager.list_events()

                    elif user_input == 2:
                        event_manager.create_event()

                    elif user_input == 3:
                        event_manager.edit_event()

                    elif user_input == 4:
                        event_manager.delete_event()

                    elif user_input == 5:
                        event_manager.add_attendee()

                    elif user_input == 6:
                        event_manager.list_attendees()

                    elif user_input == 7:
                        event_manager.delete_attendee()

                    elif user_input == 8:
                        print("Exiting the program.")
                        break

                    else:
                        raise InvalidInputException('Enter a number between 1 to 8')

                except ValueError:
                    print("Invalid Input Error: Enter a number between 1 to 8")

        except EventManagerException as e:
            print(f"Event Manager Error: {e}")


if __name__ == "__main__":
    main()