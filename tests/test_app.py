import os
import sys
import unittest
from datetime import date, timedelta

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from database import Database
from models import Scholarship, StudentProfile


def make(name, country="Rwanda", level="Undergraduate",
         field="Engineering", days=10):
    return Scholarship(
        name, "Prov", country, level, field, "notes",
        date.today() + timedelta(days=days),
        "https://example.org"
    )


class AppTests(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.db.create_tables()

    def test_search_includes_all_africa(self):
        self.db.add_scholarship(make("A"))
        self.db.add_scholarship(make("B", country="All Africa"))
        self.db.add_scholarship(make("C", country="Kenya"))
        names = [
            s.name for s in self.db.search_by_country("  rwanda ")
        ]
        self.assertEqual(sorted(names), ["A", "B"])

    def test_duplicate_rejected(self):
        self.db.add_scholarship(make("A"))
        with self.assertRaises(ValueError):
            self.db.add_scholarship(make("A"))

    def test_eligibility(self):
        p = StudentProfile("Rwanda", "Undergraduate", "engineering")
        self.assertTrue(make("A").matches(p))
        self.assertFalse(make("B", level="PhD").matches(p))
        self.assertTrue(make("C", level="Any", field="Any").matches(p))
        self.assertFalse(make("D", days=-3).matches(p))

    def test_reminders_not_duplicated(self):
        self.db.add_scholarship(make("Soon", days=3))
        self.db.add_scholarship(make("Later", days=40))
        self.assertEqual(self.db.create_deadline_reminders(7), 1)
        self.assertEqual(self.db.create_deadline_reminders(7), 0)
        self.assertEqual(self.db.count_unread(), 1)


if __name__ == "__main__":
    unittest.main()
