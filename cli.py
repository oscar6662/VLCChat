from controller import Controller
from keyboard import add_hotkey

class CLI():
    def __init__(self, r: Controller):
        self.r = r
        self.isAcceptingUserInput = False
        # Trigger read input on enter keypress
        add_hotkey("enter", self.prepare_for_user_input)

    def prepare_for_user_input(self):
        self.isAcceptingUserInput = True

    def event_loop(self):
        while True:
            # Check for received messages
            received_message = self.r.get_message()
            if received_message:
                print(received_message)
            
            if self.isAcceptingUserInput:
                # Read input from user
                input()
                message = input("> ")
                if len(message) <= 200:
                    # Send message
                    self.r.enqueue_message_for_sending(message)
                else:
                    print("Maximum length exceeded. Please send multiple messages.")
                self.isAcceptingUserInput = False

        