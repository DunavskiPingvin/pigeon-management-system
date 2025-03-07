#!/bin/bash

# Initialize an empty array to store pigeons
pigeons=()

# Function to add a pigeon
add_pigeon() {
  read -p "Enter pigeon name: " name
  read -p "Enter pigeon breed: " breed
  read -p "Enter pigeon age: " age

  # Basic input validation (you can enhance this)
  if [[ ! "$age" =~ ^[0-9]+$ ]]; then
    echo "Invalid age. Please enter a number."
    return 1
  fi

  pigeons+=("name:$name breed:$breed age:$age")
  echo "Pigeon '$name' added."
}

# Function to list pigeons
list_pigeons() {
  if [[ ${#pigeons[@]} -eq 0 ]]; then
    echo "No pigeons in the system."
    return
  fi

  for p in "${pigeons[@]}"; do
    name="${p#*name:}"
    name="${name%%breed:*}"
    breed="${p#*breed:}"
    breed="${breed%%age:*}"
    age="${p#*age:}"
    echo "Name: $name, Breed: $breed, Age: $age"
  done
}

# Function to delete a pigeon
delete_pigeon() {
  read -p "Enter name of pigeon to delete: " name

  temp_pigeons=()
  found=false

  for p in "${pigeons[@]}"; do
    p_name="${p#*name:}"
    p_name="${p_name%%breed:*}"

    if [[ "$p_name" == "$name" ]]; then
      echo "Pigeon '$name' deleted."
      found=true
    else
       temp_pigeons+=("$p")
    fi
  done

  if ! $found; then
      echo "Pigeon '$name' not found."
  fi

  pigeons=("${temp_pigeons[@]}") #Update pigeons array

}


# Main loop
while true; do
  echo ""
  echo "Pigeon Manager"
  echo "1. Add Pigeon"
  echo "2. List Pigeons"
  echo "3. Delete Pigeon"
  echo "4. Exit"

  read -p "Enter your choice: " choice

  case "$choice" in
    1) add_pigeon ;;
    2) list_pigeons ;;
    3) delete_pigeon ;;
    4) break ;;  # Exit the loop
    *) echo "Invalid choice. Please try again." ;;
  esac
done

# After the loop finishes, you can access the 'pigeons' array.
# For example, to print the pigeons in a JSON-like format:

echo "["
  for i in "${!pigeons[@]}"; do
    p="${pigeons[$i]}"
    name="${p#*name:}"
    name="${name%%breed:*}"
    breed="${p#*breed:}"
    breed="${breed%%age:*}"
    age="${p#*age:}"
    echo "  {"
    echo "    \"name\": \"$name\","
    echo "    \"breed\": \"$breed\","
    echo "    \"age\": $age"
    if [[ "$i" -lt $(( ${#pigeons[@]} - 1 )) ]]; then  # Add comma unless it's the last element
      echo "  },"
    else
      echo "  }"
    fi
  done
echo "]"


# Or you can do other processing with the 'pigeons' array as needed.
