
def search_by_country(db):
    print("\n- 1. SEARCH SCHOLARSHIPS BY COUNTRY -")
    country = ask_text("Enter a country (e.g. Rwanda): ")
    results = db.search_by_country(country)
    if not results:
        print(f"No scholarships found for '{country}'.")
    else:
        show_table(results)
        print(f"Found {len(results)} scholarship(s) (includes 'All Africa' ones).")
    print("Returning to the Main Menu...")



def check_eligibility(db):
    print("\n- 2. CHECK MY ELIGIBILITY -")
    options = " ".join(f"{i}.{name}" for i, name in enumerate(LEVELS, start=1))
    level_number = ask_number(f"Education level ({options}): ", 1, len(LEVELS))
    home_country = ask_text("Your home country: ")
    field = ask_text("Field of study (e.g. Engineering): ")

    profile = StudentProfile(home_country, LEVELS[level_number - 1], field)
    db.save_profile(profile)

    matches = [s for s in db.get_all() if s.matches(profile)]  # list comprehension
    if not matches:
        print("No open scholarships match your profile right now.")
    else:
        print(f"You may qualify for {len(matches)} scholarship(s):")
        show_table(matches)
        print("Use option 3 to see the full details of one.")
    print("Returning to the Main Menu...")



def view_details(db):
    print("\n- 3. VIEW SCHOLARSHIP DETAILS -")
    scholarship_id = ask_number("Enter scholarship ID: ", 1, 10**9,
                                "Invalid ID. Please type a whole number, e.g. 1.")
    scholarship = db.get_by_id(scholarship_id)
    if scholarship is None:
        print(f"Scholarship not found: no scholarship has ID {scholarship_id}.")
    else:
        print()
        print(scholarship.details_text())
    print("Returning to the Main Menu...")