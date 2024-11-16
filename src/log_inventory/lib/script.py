import json
import os

# Path for the JSON inventory file
INVENTORY_FILE = 'arduino_inventory.json'

def load_inventory():
    """Load existing inventory from JSON file."""
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_inventory(inventory):
    """Save inventory to JSON file."""
    with open(INVENTORY_FILE, 'w') as file:
        json.dump(inventory, file, indent=2)

def add_part(inventory):
    """Add a new part to the inventory."""
    part_name = input("Enter the part name: ").strip()
    if not part_name:
        print("Part name cannot be empty.")
        return

    # Initialize or update part details
    part_details = inventory.get(part_name, {})
    print(f"Enter details for '{part_name}' (leave blank to finish):")
    
    while True:
        key = input("Key: ").strip()
        if not key:
            break
        value = input(f"Value for '{key}': ").strip()
        part_details[key] = value
    
    inventory[part_name] = part_details
    print(f"Part '{part_name}' has been added/updated.")
    return inventory

def view_inventory(inventory):
    """Display current inventory."""
    if not inventory:
        print("Inventory is empty.")
    else:
        print("\nCurrent Inventory:")
        for part_name, details in inventory.items():
            print(f"\n{part_name}:")
            for key, value in details.items():
                print(f"  {key}: {value}")

def main():
    inventory = load_inventory()
    while True:
        print("\nArduino Inventory Manager")
        print("1. Add/Update Part")
        print("2. View Inventory")
        print("3. Exit")
        choice = input("Select an option: ").strip()

        if choice == '1':
            inventory = add_part(inventory)
            save_inventory(inventory)
        elif choice == '2':
            view_inventory(inventory)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
