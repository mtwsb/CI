import json
import os
import unittest

from main import NoteManager

class TestNoteManager(unittest.TestCase):
    def setUp(self):
        self.test_filename = 'test_notes.json'
        self.manager = NoteManager(filename=self.test_filename)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_initial_notes_empty(self):
        self.assertEqual(self.manager.notes, [])

    def test_add_single_note(self):
        self.manager.add_note("Test note 1")
        self.assertIn("Test note 1", self.manager.notes)

    def test_add_multiple_notes(self):
        self.manager.add_note("Test note 1")
        self.manager.add_note("Test note 2")
        self.assertIn("Test note 1", self.manager.notes)
        self.assertIn("Test note 2", self.manager.notes)

    def test_remove_note_valid(self):
        self.manager.add_note("Test note 1")
        self.manager.add_note("Test note 2")
        self.manager.remove_note(0)
        self.assertNotIn("Test note 1", self.manager.notes)
        self.assertIn("Test note 2", self.manager.notes)

    def test_remove_note_invalid(self):
        self.manager.add_note("Test note 1")
        self.manager.remove_note(5)  # Invalid index
        self.assertIn("Test note 1", self.manager.notes)

    def test_remove_note_empty_list(self):
        with patch('builtins.print') as mocked_print:
            self.manager.remove_note(0)  # Attempt to remove from empty list
            mocked_print.assert_called_once_with("Nieprawidłowy indeks.")

    def test_display_notes_empty(self):
        with patch('builtins.print') as mocked_print:
            self.manager.display_notes()
            mocked_print.assert_called_once_with("Brak notatek.")

    def test_display_notes(self):
        self.manager.add_note("Test note 1")
        self.manager.add_note("Test note 2")
        with patch('builtins.print') as mocked_print:
            self.manager.display_notes()
            self.assertIn(mocked_print.call_args_list[0][0][0], "0: Test note 1")
            self.assertIn(mocked_print.call_args_list[1][0][0], "1: Test note 2")

    def test_save_notes_to_file(self):
        self.manager.add_note("Test note 1")
        with open(self.test_filename, 'r') as f:
            notes = json.load(f)
        self.assertEqual(notes, ["Test note 1"])

    def test_load_notes_from_file(self):
        with open(self.test_filename, 'w') as f:
            json.dump(["Test note 1"], f)
        manager2 = NoteManager(filename=self.test_filename)
        self.assertIn("Test note 1", manager2.notes)

    def test_save_notes_creates_file(self):
        self.manager.add_note("Test note 1")
        self.assertTrue(os.path.exists(self.test_filename))

    def test_add_note_saves_to_file(self):
        self.manager.add_note("Test note 1")
        with open(self.test_filename, 'r') as f:
            notes = json.load(f)
        self.assertEqual(notes, ["Test note 1"])

    def test_remove_note_saves_to_file(self):
        self.manager.add_note("Test note 1")
        self.manager.remove_note(0)
        with open(self.test_filename, 'r') as f:
            notes = json.load(f)
        self.assertEqual(notes, [])

    def test_remove_note_display_message(self):
        self.manager.add_note("Test note 1")
        with patch('builtins.print') as mocked_print:
            self.manager.remove_note(0)
            mocked_print.assert_called_once_with("Usunięto notatkę: Test note 1")

    def test_add_empty_note(self):
        self.manager.add_note("")
        self.assertIn("", self.manager.notes)



if __name__ == "__main__":
    unittest.main()

