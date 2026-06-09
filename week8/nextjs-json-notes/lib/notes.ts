import { promises as fs } from "node:fs";
import path from "node:path";
import type { Note, NoteInput } from "@/types/note";

const dataDirectory = path.join(process.cwd(), "data");
const notesFilePath = path.join(dataDirectory, "notes.json");

async function ensureNotesFile() {
  await fs.mkdir(dataDirectory, { recursive: true });

  try {
    await fs.access(notesFilePath);
  } catch {
    await fs.writeFile(notesFilePath, "[]", "utf8");
  }
}

function validateTitle(title: unknown): string {
  if (typeof title !== "string" || title.trim().length === 0) {
    throw new Error("Title is required and cannot be empty.");
  }

  return title.trim();
}

function normalizeContent(content: unknown): string {
  return typeof content === "string" ? content : "";
}

export async function getNotes(): Promise<Note[]> {
  await ensureNotesFile();

  const contents = await fs.readFile(notesFilePath, "utf8");

  try {
    const notes = JSON.parse(contents);
    return Array.isArray(notes) ? notes : [];
  } catch {
    return [];
  }
}

export async function saveNotes(notes: Note[]) {
  await ensureNotesFile();
  await fs.writeFile(notesFilePath, JSON.stringify(notes, null, 2), "utf8");
}

export async function createNote(input: NoteInput): Promise<Note> {
  const notes = await getNotes();
  const now = new Date().toISOString();
  const note: Note = {
    id: crypto.randomUUID(),
    title: validateTitle(input.title),
    content: normalizeContent(input.content),
    createdAt: now,
    updatedAt: now,
  };

  notes.unshift(note);
  await saveNotes(notes);

  return note;
}

export async function updateNote(
  id: string,
  input: NoteInput,
): Promise<Note | null> {
  const notes = await getNotes();
  const noteIndex = notes.findIndex((note) => note.id === id);

  if (noteIndex === -1) {
    return null;
  }

  const existingNote = notes[noteIndex];
  const updatedNote: Note = {
    ...existingNote,
    title: validateTitle(input.title),
    content: normalizeContent(input.content),
    updatedAt: new Date().toISOString(),
  };

  notes[noteIndex] = updatedNote;
  await saveNotes(notes);

  return updatedNote;
}

export async function deleteNote(id: string): Promise<boolean> {
  const notes = await getNotes();
  const nextNotes = notes.filter((note) => note.id !== id);

  if (nextNotes.length === notes.length) {
    return false;
  }

  await saveNotes(nextNotes);
  return true;
}
