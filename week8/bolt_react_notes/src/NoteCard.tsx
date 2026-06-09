import { Pencil, Trash2, Clock } from 'lucide-react';
import type { Note } from './types';

interface NoteCardProps {
  note: Note;
  onEdit: (note: Note) => void;
  onDelete: (id: string) => void;
}

function formatDate(iso: string) {
  const date = new Date(iso);
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function NoteCard({ note, onEdit, onDelete }: NoteCardProps) {
  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${note.title}"? This action cannot be undone.`)) {
      onDelete(note.id);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow group">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <h3 className="text-base font-semibold text-gray-900 truncate">{note.title}</h3>
          {note.content && (
            <p className="mt-2 text-sm text-gray-600 whitespace-pre-wrap line-clamp-4">{note.content}</p>
          )}
        </div>
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
          <button
            onClick={() => onEdit(note)}
            className="p-2 rounded-lg text-gray-400 hover:text-teal-600 hover:bg-teal-50 transition-colors"
            aria-label={`Edit ${note.title}`}
          >
            <Pencil size={16} />
          </button>
          <button
            onClick={handleDelete}
            className="p-2 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
            aria-label={`Delete ${note.title}`}
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>
      <div className="mt-3 flex items-center gap-4 text-xs text-gray-400">
        <span className="inline-flex items-center gap-1">
          <Clock size={12} />
          Created {formatDate(note.createdAt)}
        </span>
        {note.updatedAt !== note.createdAt && (
          <span className="inline-flex items-center gap-1">
            <Clock size={12} />
            Updated {formatDate(note.updatedAt)}
          </span>
        )}
      </div>
    </div>
  );
}
