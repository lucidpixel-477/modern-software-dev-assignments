import { StickyNote } from 'lucide-react';
import type { Note } from './types';
import { NoteCard } from './NoteCard';

interface NoteListProps {
  notes: Note[];
  onEdit: (note: Note) => void;
  onDelete: (id: string) => void;
}

export function NoteList({ notes, onEdit, onDelete }: NoteListProps) {
  if (notes.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-gray-400">
        <StickyNote size={48} strokeWidth={1.5} />
        <p className="mt-4 text-lg font-medium">No notes yet</p>
        <p className="mt-1 text-sm">Create your first note to get started.</p>
      </div>
    );
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {notes.map((note) => (
        <NoteCard key={note.id} note={note} onEdit={onEdit} onDelete={onDelete} />
      ))}
    </div>
  );
}
