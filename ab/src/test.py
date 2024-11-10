import json
import os
import pytest
from main import NoteManager

@pytest.fixture
def note_manager(tmp_path):

    test_file = tmp_path / 'test_notes.json'
    manager = NoteManager(filename=test_file)
    return manager

def test_initial_notes_empty(note_manager):
    assert note_manager.notes == []

def test_add_single_note(note_manager):
    note_manager.add_note("Test note 1")
    assert "Test note 1" in note_manager.notes

def test_add_multiple_notes(note_manager):
    note_manager.add_note("Test note 1")
    note_manager.add_note("Test note 2")
    assert "Test note 1" in note_manager.notes
    assert "Test note 2" in note_manager.notes

def test_remove_note_valid(note_manager):
    note_manager.add_note("Test note 1")
    note_manager.add_note("Test note 2")
    note_manager.remove_note(0)
    assert "Test note 1" not in note_manager.notes
    assert "Test note 2" in note_manager.notes

def test_remove_note_invalid(note_manager):
    note_manager.add_note("Test note 1")
    note_manager.remove_note(5)  # Invalid index
    assert "Test note 1" in note_manager.notes

def test_remove_note_empty_list(note_manager, capsys):
    note_manager.remove_note(0)  # Attempt to remove from empty list
    captured = capsys.readouterr()
    assert captured.out.strip() == "Nieprawidłowy indeks."

def test_display_notes_empty(note_manager, capsys):
    note_manager.display_notes()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Brak notatek."

def test_display_notes(note_manager, capsys):
    note_manager.add_note("Test note 1")
    note_manager.add_note("Test note 2")
    note_manager.display_notes()
    captured = capsys.readouterr()
    output = captured.out.strip().split('\n')
    assert output[0] == "0: Test note 1"
    assert output[1] == "1: Test note 2"

def test_save_notes_to_file(note_manager):
    note_manager.add_note("Test note 1")
    with open(note_manager.filename, 'r') as f:
        notes = json.load(f)
    assert notes == ["Test note 1"]

def test_load_notes_from_file(note_manager, tmp_path):
    test_file = tmp_path / 'test_notes.json'
    with open(test_file, 'w') as f:
        json.dump(["Test note 1"], f)
    manager2 = NoteManager(filename=test_file)
    assert "Test note 1" in manager2.notes

def test_save_notes_creates_file(note_manager):
    note_manager.add_note("Test note 1")
    assert os.path.exists(note_manager.filename)

def test_add_note_saves_to_file(note_manager):
    note_manager.add_note("Test note 1")
    with open(note_manager.filename, 'r') as f:
        notes = json.load(f)
    assert notes == ["Test note 1"]

def test_remove_note_saves_to_file(note_manager):
    note_manager.add_note("Test note 1")
    note_manager.remove_note(0)
    with open(note_manager.filename, 'r') as f:
        notes = json.load(f)
    assert notes == []

def test_remove_note_display_message(note_manager, capsys):
    note_manager.add_note("Test note 1")
    note_manager.remove_note(0)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Usunięto notatkę: Test note 1"

def test_add_empty_note(note_manager):
    note_manager.add_note("")
    assert "" in note_manager.notes
