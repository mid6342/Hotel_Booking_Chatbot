import csv
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from dateutil.parser import parse
from datetime import datetime

class ActionSaveDates(Action):
    def name(self) -> Text:
        return "action_save_dates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extracting the entities for check-in and check-out dates
        entities = tracker.latest_message['entities']
        check_in_date = None
        check_out_date = None

        for ent in entities:
            if ent['entity'] == 'time':
                if not check_in_date:
                    check_in_date = ent['value']
                else:
                    check_out_date = ent['value']

        # Parse and format the dates if they exist
        if check_in_date:
            check_in_date = parse(check_in_date).strftime('%Y-%m-%d')
        if check_out_date:
            check_out_date = parse(check_out_date).strftime('%Y-%m-%d')

        # Save the extracted entities into the slots
        slots = []
        if check_in_date:
            slots.append(SlotSet("check_in_date", check_in_date))
        if check_out_date:
            slots.append(SlotSet("check_out_date", check_out_date))

        # Create the response message
        if check_in_date and check_out_date:
            response_message = f"Thank you for providing your dates. I have your check-in scheduled for {check_in_date} and check-out for {check_out_date}. How many guests will be staying? (Note: We offer rooms that accommodate 1, 2, or 3 guests.)"            
            dispatcher.utter_message(text=response_message)
        else:
            # Ask again if dates were not extracted properly
            dispatcher.utter_message(template="utter_ask_dates")

        return slots
    
class ActionCheckAvailabilityAndSaveDetails(Action):
    def name(self) -> Text:
        return "action_check_availability_and_save_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extracting the entities for check-in and check-out dates and number_of_guests
        check_in_date = tracker.get_slot('check_in_date')
        check_out_date = tracker.get_slot('check_out_date')
        number_of_guests = next(tracker.get_latest_entity_values("number_of_guests"), None)
        
        if not check_in_date or not check_out_date:
            dispatcher.utter_message(text="I need to know the check-in and check-out dates to proceed.")
            return []
        
        # Convert the number_of_guests entity to an integer if possible
        if number_of_guests:
            try:
                number_of_guests = int(number_of_guests)
            except ValueError:
                dispatcher.utter_message(text="Please tell me how many guests there will be using a number.")
                return []
        else:
            dispatcher.utter_message(text="Please tell me the number of guests.")
            return []
        
        # Parse dates
        check_in_date = parse(check_in_date).date()
        check_out_date = parse(check_out_date).date()

        # Read the room data from the CSV file
        room_data = self.read_room_data()
        
        # Find available rooms
        available_rooms = self.find_available_rooms(room_data, check_in_date, check_out_date, number_of_guests)
        
        if available_rooms:
            # Inform user about the available room options
            dispatcher.utter_message(text = f"A room suitable for {number_of_guests} guest(s) is available from {check_in_date} to {check_out_date}. Would you like to secure your reservation now?")
            return [
                SlotSet("check_in_date", check_in_date.strftime('%Y-%m-%d')),
                SlotSet("check_out_date", check_out_date.strftime('%Y-%m-%d')),
                SlotSet("number_of_guests", number_of_guests),
            ]
        else:
            # Inform user that no rooms are available
            dispatcher.utter_message(text = "We regret to inform you that we do not have any available rooms for your specified dates and number of guests. May I assist you with any other queries?")
    
    def read_room_data(self):
        # Reads room data from a CSV file.
        with open('rooms.csv', mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    
    def find_available_rooms(self, room_data, check_in_date, check_out_date, number_of_guests):
        # Finds rooms based on the number of guests and the check-in and check-out dates.
        available_rooms = []
        for room in room_data:
            room_capacity = int(room['room_type'].split()[0])  # Assumes room_type like "1 person", "2 persons", etc.
            if room_capacity >= number_of_guests:
                available_from = datetime.strptime(room['available_from'], '%Y-%m-%d').date()
                available_until = datetime.strptime(room['available_until'], '%Y-%m-%d').date()
                if available_from <= check_in_date and available_until >= check_out_date:
                    available_rooms.append(room['room_type'])
        return list(set(available_rooms))  # Return unique room types
