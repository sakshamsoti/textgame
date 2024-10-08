# Class to define each room in the game
class Room:
    def __init__(self, name, description, items, connections, locked=False, unlock_item=None):
        self.name = name
        self.description = description
        self.items = items  # List of items in the room
        self.connections = connections  # Dictionary to store room connections
        self.locked = locked  # If the room is locked
        self.unlock_item = unlock_item  # Item required to unlock this room

    def get_details(self):
        print(f"\nYou are in {self.name}.")
        print(self.description)
        if self.items:
            print(f"Items in the room: {', '.join(self.items)}")
        else:
            print("There are no items here.")

    def get_connections(self):
        return self.connections

    def unlock(self, item):
        if item == self.unlock_item:
            self.locked = False
            print(f"You used {item} to unlock the {self.name}!")
        else:
            print(f"You need {self.unlock_item} to unlock this room.")

# Class for the player
class Player:
    def __init__(self):
        self.inventory = []  # Inventory to store items collected
        self.current_room = None  # Player starts with no room

    def move(self, direction, rooms):
        if direction in self.current_room.connections:
            next_room_key = self.current_room.connections[direction]
            next_room = rooms[next_room_key]

            if next_room.locked:
                print(f"The {next_room.name} is locked! You need {next_room.unlock_item} to enter.")
            else:
                self.current_room = next_room
                print(f"\nMoving to {next_room.name}...")
                self.current_room.get_details()
        else:
            print("You can't go that way!")

    def pick_item(self, item):
        if item in self.current_room.items:
            self.inventory.append(item)
            self.current_room.items.remove(item)
            print(f"You picked up {item}.")
        else:
            print("That item is not here.")

    def use_item(self, item, rooms):
        if item in self.inventory:
            for room in rooms.values():
                if room.locked and room.unlock_item == item:
                    room.unlock(item)
        else:
            print(f"You don't have {item} in your inventory.")

    def show_inventory(self):
        print("Your inventory: ", ', '.join(self.inventory))

# Initialize the rooms
rooms = {
    'living_room': Room('Living Room', 'A cozy room with a sofa and a TV.', ['map'], {'north': 'kitchen', 'east': 'treasure_room'}),
    'kitchen': Room('Kitchen', 'A room with a refrigerator and a stove.', ['key'], {'south': 'living_room'}),
    'bedroom': Room('Bedroom', 'A quiet room with a bed and a wardrobe.', [], {'west': 'living_room'}),
    'treasure_room': Room('Treasure Room', 'A locked room containing a chest of treasure.', [], {}, locked=True, unlock_item='key')
}

# Set initial room for player
player = Player()
player.current_room = rooms['living_room']

# Game loop
def game_loop():
    while True:
        command = input("\nEnter a command (move [north/south/east/west], pick [item], use [item], inventory, or quit): ").lower().split()
        if command[0] == 'move':
            player.move(command[1], rooms)
        elif command[0] == 'pick':
            player.pick_item(command[1])
        elif command[0] == 'use':
            player.use_item(command[1], rooms)
        elif command[0] == 'inventory':
            player.show_inventory()
        elif command[0] == 'quit':
            print("Thanks for playing!")
            break
        else:
            print("Invalid command. Try again.")

# Start the game
player.current_room.get_details()
game_loop()