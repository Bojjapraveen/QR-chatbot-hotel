from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__, static_url_path='/static')

# Database connection and query handling
def handle_query(query_type, search_value):
    """Handles multiple query types and returns formatted results."""
    
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    queries = {
        "food_menu": ('SELECT Item, Description, Price, "Dietary Options" FROM food_menu WHERE Availability LIKE ?', 
                      ["Item", "Description", "Price", "Dietary Options"]),
        "guest_services": ('SELECT Availability, "Extra Cost", Notes FROM guest_services WHERE Service LIKE ?', 
                           ["Availability", "Extra Cost", "Notes"]),
        "restaurant_timings": ('SELECT "Opening Time", "Closing Time", "Last Order" FROM restaurant_timings WHERE Meal LIKE ?', 
                               ["Opening Time", "Closing Time", "Last Order"]),
        "extra_services": ('SELECT Price, Availability, Notes FROM extra_services WHERE Service LIKE ?', 
                           ["Price", "Availability", "Notes"])
    }

    if query_type not in queries:
        return jsonify({"error": f"⚠️ Invalid query type: {query_type}"}), 400

    sql_query, column_names = queries[query_type]
    
    try:
        cursor.execute(sql_query, ('%' + search_value + '%',))
        results = cursor.fetchall()
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    if not results:
        return jsonify({"message": f"No records found for '{search_value}' in {query_type}."})

    # Format food_menu results into readable text
    if query_type == "food_menu":
        formatted_results = "\n".join(
            [f"- **{row[0]}** – {row[1]} (₹{row[2]}) | {row[3] if row[3] else 'No dietary info'}" for row in results]
        )
    else:
        formatted_results = [dict(zip(column_names, row)) for row in results]

    return jsonify({"results": formatted_results})

@app.route("/", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        query_type = request.form.get("query_type")
        search_value = request.form.get("search_value")
        
        if not query_type or not search_value:
            return jsonify({"error": "⚠️ Both query_type and search_value are required."}), 400
        
        response = handle_query(query_type, search_value)
        return response

    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug=True)