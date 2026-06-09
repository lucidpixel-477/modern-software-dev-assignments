import { useState } from 'react';
import { NotebookPen } from 'lucide-react';
import type { Note } from './types';
import { useNotes } from './useNotes';
import { NoteForm } from './NoteForm';
import { NoteList } from './NoteList';

export default function App() {
  const { notes, addNote, updateNote, deleteNote } = useNotes();
  const [editingNote, setEditingNote] = useState<Note | null>(null);

  const handleSave = (title: string, content: string) => {
    if (editingNote) {
      updateNote(editingNote.id, title, content);
      setEditingNote(null);
    } else {
      addNote(title, content);
    }
  };

  const handleEdit = (note: Note) => {
    setEditingNote(note);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCancel = () => {
    setEditingNote(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-3">
          <NotebookPen size={28} className="text-teal-600" />
          <h1 className="text-xl font-bold text-gray-900">Notes Manager</h1>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        <NoteForm note={editingNote} onSave={handleSave} onCancel={handleCancel} />
        <NoteList notes={notes} onEdit={handleEdit} onDelete={deleteNote} />
      </main>
    </div>
  );
}
