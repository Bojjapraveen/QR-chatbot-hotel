import sqlite3

def handle_query(query_type, search_value):
    """Handles multiple query types and returns results from the hotel database."""
    
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    queries = {
        "food_menu": 'SELECT Item, Description, Price, "Dietary Options" FROM food_menu WHERE Availability LIKE ?',
        "guest_services": 'SELECT Availability, "Extra Cost", Notes FROM guest_services WHERE Service LIKE ?',
        "restaurant_timings": 'SELECT "Opening Time", "Closing Time", "Last Order" FROM restaurant_timings WHERE Meal LIKE ?',
        "extra_services": 'SELECT Price, Availability, Notes FROM extra_services WHERE Service LIKE ?'
    }
    
    # Display the question in the terminal
    print(f"\n🔍 Guest Inquiry: {query_type} - {search_value}\n")
    
    if query_type in queries:
        cursor.execute(queries[query_type], ('%' + search_value + '%',))
        results = cursor.fetchall()
    else:
        results = "⚠️ Invalid query type."

    conn.close()
    
    return results if results else f"No records found for {search_value} in {query_type}."

# Example Usage
print(handle_query("food_menu", "Dinner"))  
print(handle_query("guest_services", "Early Check-In"))  
print(handle_query("restaurant_timings", "Breakfast"))  
print(handle_query("extra_services", "Spa Treatment"))  