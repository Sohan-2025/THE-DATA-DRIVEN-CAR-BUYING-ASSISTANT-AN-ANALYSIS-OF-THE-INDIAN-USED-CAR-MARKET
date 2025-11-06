# This is your new car-finding assistant!
# It will ask you questions and then search the 'data.csv' file to find cars that match.

import pandas as pd

def load_and_clean_data(filepath='data.csv'):
    """
    Loads the data and performs essential cleaning for our tool.
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print("Make sure it's in the same folder as this script!")
        return None
    
    # --- NEW CODE: Standardize string columns to match user input ---
    # This prevents mismatches like "Petrol" (user) vs "petrol" (data)
    # We will use .str.title() to make them all "Title Case"
    string_cols = ['Make', 'Fuel Type', 'Owner', 'Transmission', 'Location', 'Model']
    for col in string_cols:
        if col in df.columns: # Check if column exists
            # We convert to string first, then apply .str.title()
            df[col] = df[col].astype(str).str.title()
    # --- END OF NEW CODE ---
    
    # We now drop rows that are missing our new filter columns
    # 'Max Power' and 'Max Torque' have been removed from this list
    cols_to_check = [
        'Price', 'Kilometer', 'Make', 'Fuel Type', 
        'Model', 'Year', 'Owner', 'Transmission', 'Location', 'Seating Capacity'
    ]
    
    # We must also check for the string 'Nan' that .astype(str) creates
    # from empty cells, and replace it with a real "Not aNumber"
    # so that dropna() can find and remove it.
    df.replace('Nan', pd.NA, inplace=True) 
    
    df.dropna(subset=cols_to_check, inplace=True)
    
    # We also need to convert 'Year' to a number, just in case
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df.dropna(subset=['Year'], inplace=True) # Drop rows where Year wasn't a number
    df['Year'] = df['Year'].astype(int)
    
    return df

def get_user_criteria(df):
    """
    Asks the user for their requirements.
    We also add error handling for number inputs.
    """
    print("\n--- Welcome to the Advanced Car Finder ---")
    print("Please answer a few questions to find your perfect car.")
    
    criteria = {} # We'll store all answers in this dictionary

    # --- THIS LOGIC IS NEW ---
    # Get Target Price and create a +/- 15% range
    while True:
        try:
            target_price = float(input("What is your target budget? (e.g., 500000): "))
            if target_price <= 0:
                print("Please enter a positive number for the budget.")
                continue
                
            criteria['min_price'] = target_price * 0.85 # 15% below
            criteria['max_price'] = target_price * 1.15 # 15% above
            
            print(f"Great! I will search for cars between \u20B9{criteria['min_price']:,.0f} and \u20B9{criteria['max_price']:,.0f}.")
            break
        except ValueError:
            print("Oops! Please enter a number for the budget.")
    # --- END OF NEW LOGIC ---

    # Get Oldest Year (New Filter!)
    while True:
        try:
            # We ask for the *oldest* year they'll accept (e.g., 2018)
            criteria['min_year'] = int(input("What's the oldest model year you'll accept? (e.g., 2018): "))
            if 1980 < criteria['min_year'] <= 2025:
                break
            else:
                print("Please enter a reasonable year (e.g., 2015, 2020).")
        except ValueError:
            print("Oops! Please enter a 4-digit year (e.g., 2018).")

    # Get Fuel Type
    available_fuels = list(df['Fuel Type'].unique())
    print(f"Available fuel types: {available_fuels}")
    while True:
        fuel = input(f"What fuel type do you prefer? ").strip().title()
        if fuel in available_fuels:
            criteria['fuel'] = fuel
            break
        else:
            print(f"Sorry, that's not a valid option. Please choose from: {available_fuels}")

    # Get Max Kilometers
    while True:
        try:
            criteria['max_km'] = float(input("What is the maximum kilometers driven you'll accept? (e.g., 80000): "))
            break
        except ValueError:
            print("Oops! Please enter a number for the kilometers.")
    
    # Get Owner Type (New Filter!)
    available_owners = list(df['Owner'].unique())
    available_owners.append('Any') # Add 'Any' as an option
    print(f"Available owner types: {available_owners}")
    while True:
        owner = input(f"What owner type do you prefer? (Type 'Any' to skip): ").strip().title()
        if owner in available_owners:
            criteria['owner'] = owner
            break
        else:
            print(f"Sorry, that's not a valid option. Please choose from: {available_owners}")
            
    # Get Transmission Type (New Filter!)
    available_trans = list(df['Transmission'].unique())
    available_trans.append('Any') # Add 'Any' as an option
    print(f"Available transmission types: {available_trans}")
    while True:
        trans = input(f"Automatic or Manual? (Type 'Any' to skip): ").strip().title()
        if trans in available_trans:
            criteria['transmission'] = trans
            break
        else:
            print(f"Sorry, that's not a valid option. Please choose from: {available_trans}")

    # Get Preferred Make (Optional)
    criteria['make'] = input("Any preferred make? (e.g., Maruti, Honda, or press Enter to skip): ").strip().title()
    
    return criteria

def find_matching_cars(df, criteria):
    """
    Filters the DataFrame based on the user's criteria.
    """
    
    # Start with all cars
    results = df.copy()
    
    # --- THIS LOGIC IS NEW ---
    # Apply filters one by one
    # We now filter *between* the min and max price
    results = results[results['Price'] >= criteria['min_price']]
    results = results[results['Price'] <= criteria['max_price']]
    # --- END OF NEW LOGIC ---
    
    results = results[results['Year'] >= criteria['min_year']]
    results = results[results['Fuel Type'] == criteria['fuel']]
    results = results[results['Kilometer'] <= criteria['max_km']]
    
    # Apply filters *only if* the user didn't choose 'Any'
    if criteria['owner'] != 'Any':
        results = results[results['Owner'] == criteria['owner']]
        
    if criteria['transmission'] != 'Any':
        results = results[results['Transmission'] == criteria['transmission']]
    
    # Apply the 'Make' filter ONLY if the user entered one
    # Use .get() to avoid errors if 'make' key doesn't exist
    if criteria.get('make'): # This checks if the string is not empty
        results = results[results['Make'] == criteria['make']]
        
    return results

def print_results(matches):
    """
    A helper function to print the results neatly.
    """
    # Sort by Price (ascending) and use .copy() to avoid warnings
    display_matches = matches.sort_values(by='Price').copy()
    
    # Define which columns to show (original names)
    # 'Max Power' has been removed from this list
    cols_to_show = ['Make', 'Model', 'Year', 'Price', 'Kilometer', 'Seating Capacity', 'Fuel Type', 'Owner', 'Transmission', 'Location']
    
    # --- NEW: Rename column for multi-line display ---
    if 'Seating Capacity' in display_matches.columns and 'Seating Capacity' in cols_to_show:
        # The \n creates the newline in the header
        new_name = 'Seating Capacity' 
        
        # Rename the column in the DataFrame
        display_matches.rename(columns={'Seating Capacity': new_name}, inplace=True)
        
        # Update the 'cols_to_show' list to use the new name
        try:
            idx = cols_to_show.index('Seating Capacity')
            cols_to_show[idx] = new_name
        except ValueError:
            pass # Column not in list, so do nothing
    # --- END OF NEW CODE ---

    # --- FIX for formatting ---
    pd.set_option('display.width', 2000)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    
    # Print the results without the index number
    print(display_matches[cols_to_show].to_string(index=False))
    
    # Reset options back to default
    pd.reset_option('display.width')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.expand_frame_repr')

def main():
    """
    Main function to run the car finder.23
    Includes exact, flexible budget, and configuration fallback searches.
    """
    # Load the data first
    df = load_and_clean_data()
    
    # If data loading fails, df will be None, and we stop.
    if df is None:
        return # Exit the program

    # --- Start of the main loop ---
    while True: 
        # Get criteria from the user
        criteria = get_user_criteria(df)
        
        # Find cars that match (now searches in the +/- 25% range)
        matches = find_matching_cars(df, criteria)
        
        # --- 1. MATCHES FOUND IN RANGE ---
        if not matches.empty:
            print("\n-------------------------------------------")
            print(f"Success! We found {len(matches)} cars in your budget range.")
            print(f"Here are all {len(matches)} matches, sorted by price (lowest first):")
            print_results(matches)
        
        # --- 2. NO MATCHES FOUND IN RANGE ---
        else:
            print("\n-------------------------------------------")
            min_p = criteria.get('min_price', 0)
            max_p = criteria.get('max_price', 0)
            print(f"Sorry, no cars found in your budget range (\u20B9{min_p:,.0f} - \u20B9{max_p:,.0f}).")

            # --- 5. TRY CONFIGURATION SEARCH ---
            # This logic now runs immediately if no matches were found
            # AND the user specified a make.
            
            if criteria.get('make'): # Check if 'make' was a criteria
                print("\n...checking for other makes/models that match your other specs...")
                
                # Create new criteria *without* the 'make'
                config_criteria = criteria.copy()
                original_make = config_criteria.pop('make') # Remove the make
                
                # Search using original criteria (including the budget range), just without the make
                config_matches = find_matching_cars(df, config_criteria)
                
                if not config_matches.empty:
                    # --- 6. CONFIGURATION MATCH FOUND ---
                    print(f"\nWe couldn't find any '{original_make}' cars in your range,")
                    print(f"but we found {len(config_matches)} OTHER cars in your budget range that match:")
                    print_results(config_matches)
                else:
                    # --- 7. ALL SEARCHES FAILED ---
                    print(f"We also couldn't find any other brands matching your core requirements.")
                    print("We recommend starting a new search with broader criteria.")
            
            else: # This runs if no matches found AND no make was specified
                # This block runs if:
                # 1. Range search failed.
                # 2. User did NOT specify a make (so config search is pointless).
                print("Please try a new search with broader criteria (e.g., different year or fuel type).")

        # --- 8. RESTART LOOP ---
        print("\n-------------------------------------------")
        again = input("Do you want to start a new search? (yes/no): ").strip().lower()
        if again != 'yes' and again != 'y':
            break # Exit the 'while True' loop

    print("\nThank you for using the Car Finder Assistant! Goodbye.")

# Standard Python line to run the main() function
if __name__ == "__main__":
    main()