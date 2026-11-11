"""Features 4, 5 and 6: admin and notifications.
OWNER: Jess.
"""

from helpers import ask_text, ask_number, ask_date, show_table
from models import Scholarship, LEVELS, ANY, format_date


def add_scholarship(db):
    print("\n- 4. ADD A SCHOLARSHIP (admin) -")
    name = ask_text("Scholarship name: ")
    provider = ask_text("Provider: ")
    country = ask_text("Country it is open to (or 'All Africa'): ")
    level_number = ask_number(
        "Level (1.Undergraduate 2.Masters 3.PhD 4.Any): ", 1, 4
    )
    level = LEVELS[level_number - 1] if level_number <= 3 else ANY
    field = ask_text("Field of study (or 'Any'): ")
    eligibility = ask_text("Eligibility notes: ")
    deadline = ask_date("Deadline (DD/MM/YYYY): ")
    link = ask_text("Official application link: ")

    scholarship = Scholarship(
        name, provider, country, level, field,
        eligibility, deadline, link
    )

    try:
        new_id = db.add_scholarship(scholarship)
    except ValueError as error:
        print(f"Not saved: {error}")
    else:
        db.add_notification(
            f"New scholarship added: '{name}' ({country}), "
            f"deadline {format_date(deadline)}.",
            "update"
        )
        print(f"Saved! Scholarship ID {new_id}.")

    print("Returning to the Main Menu...")


def view_notifications(db):
    print("\n- 5. NOTIFICATIONS -")
    notifications = db.get_notifications()

    if not notifications:
        print("You have no notifications.")
    else:
        for n in notifications:
            print(n.line())
        db.mark_all_read()
        print("All notifications are now marked as read.")

    print("Returning to the Main Menu...")


def closing_soon(db):
    print("\n- 6. SCHOLARSHIPS CLOSING IN THE NEXT 30 DAYS -")
    results = db.closing_within(30)

    if not results:
        print("No scholarships close in the next 30 days.")
    else:
        show_table(results)

    print("Returning to the Main Menu...")
