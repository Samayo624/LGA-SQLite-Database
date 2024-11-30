import sqlite3
import time as t

# Because i used the sqlite3 module, i converted the database from phpMyAdmin SQL Dump to an SQLite-compatible format.


# 1 Create a page to display the result for any individual polling unit on a web page. Note that the Database you have been given only contains LGA's in Delta State (state id: 25).

# Function that gets all Polling units ids.
def get_all_polling_unit_ids():
    conn = sqlite3.connect(r"bincom_test.sqlite")
    cursor = conn.cursor()

    query = """
    SELECT polling_unit_uniqueid
    FROM announced_pu_results;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    polling_unit_ids = []
    seen_ids = set()

    for row in results:
        poll_id = row[0]
        if poll_id not in seen_ids:
            polling_unit_ids.append(poll_id)
            seen_ids.add(poll_id)

    print("Polling Unit IDs:", polling_unit_ids)
    conn.close()
    return polling_unit_ids


# Function that prints the results of a unique polling id.


def get_polling_unit_results(polling_unit_id):
    conn = sqlite3.connect(r"bincom_test.sqlite")
    cursor = conn.cursor()

    query = """
    SELECT party_abbreviation, party_score
    FROM announced_pu_results
    WHERE polling_unit_uniqueid = ?;
    """
    cursor.execute(query, (polling_unit_id,))
    results = cursor.fetchall()

    if results:
        print(f"Results for Polling Unit {polling_unit_id}:")
        for row in results:
            print(f"Party: {row[0]}, Score: {row[1]}")
    else:
        print(f"No results found for Polling Unit {polling_unit_id}.")

    conn.close()


# 2 Create a page to display the summed total result of all the polling units under any particular local government.


def get_total_polling_units_per_lga():
    conn = sqlite3.connect(r"bincom_test.sqlite")
    cursor = conn.cursor()

    query = """
    SELECT lga_id, COUNT(*) AS total_polling_units
    FROM polling_unit
    GROUP BY lga_id;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    print("Total Polling Units per LGA:")
    for row in results:
        print(f"LGA ID: {row[0]}, Total Polling Units: {row[1]}")

    conn.close()


# 3 Create a page to be used to store results for ALL parties for a new polling unit.
def add_new_polling_unit(polling_unit_data, party_results):
    conn = sqlite3.connect("bincom_test.sqlite")
    cursor = conn.cursor()

    polling_unit_query = """
    INSERT INTO polling_unit (uniqueid, ward_id, lga_id, polling_unit_name)
    VALUES (?, ?, ?, ?);
    """
    cursor.execute(polling_unit_query, polling_unit_data)

    party_results_query = """
    INSERT INTO announced_pu_results (polling_unit_uniqueid, party_abbreviation, party_score)
    VALUES (?, ?, ?);
    """
    cursor.executemany(party_results_query, party_results)

    conn.commit()
    print("New polling unit and results added successfully!")
    conn.close()


polling_unit_data = (
    1234,
    1,
    2,
    "New Polling Unit"
)

party_results = [
    (1234, 'PDP', 500),
    (1234, 'DPP', 300),
    (1234, 'ACN', 200),
    (1234, 'PPA', 150),
]

# i created functions to solve the questions given to me,
# then i used an if statement to display the solutions as options available to the user
# then the while statement to keep the code running after an option has been selected
# so as to reselect another option.
# i used the time module to display the code after certain seconds for readability.
while True:
    print('Welcome, please select an option. \nOption1: Create a page to display the result for any individual polling unit on a web page. Note that the Database you have been given only contains LGAs in Delta State (state id: 25).\nOption2: Create a page to display the summed total result of all the polling units under any particular local government.\nOption3: Create a page to be used to store results for ALL parties for a new polling unit.')
    user_Selection = input('Select  an option: ')

    if user_Selection == '1':
        unique_polling_unit_ids = get_all_polling_unit_ids()
        polling_unit_id = input("Enter Polling Unit ID: ")
        get_polling_unit_results(polling_unit_id)
    elif user_Selection == '2':
        print("Getting Total Polling Units per LGA:")
        t.sleep(2)
        get_total_polling_units_per_lga()
    elif user_Selection == '3':
        add_new_polling_unit(polling_unit_data, party_results)
    else:
        print('Invalid Option Selected')
    t.sleep(10)
