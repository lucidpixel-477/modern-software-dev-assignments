"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import type { Note } from "@/types/note";

type NoteFormState = {
  title: string;
  content: string;
};

const emptyForm: NoteFormState = {
  title: "",
  content: "",
};

async function parseError(response: Response, fallback: string) {
  try {
    const data = await response.json();
    return typeof data.error === "string" ? data.error : fallback;
  } catch {
    return fallback;
  }
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export default function Home() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [createForm, setCreateForm] = useState<NoteFormState>(emptyForm);
  const [editForm, setEditForm] = useState<NoteFormState>(emptyForm);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  const sortedNotes = useMemo(
    () =>
      [...notes].sort(
        (a, b) =>
          new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime(),
      ),
    [notes],
  );

  useEffect(() => {
    let isMounted = true;

    fetch("/api/notes")
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(await parseError(response, "Unable to load notes."));
        }

        return response.json();
      })
      .then((data) => {
        if (isMounted) {
          setNotes(data.notes ?? []);
        }
      })
      .catch((loadError) => {
        if (isMounted) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : "Unable to load notes.",
          );
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  async function handleCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (createForm.title.trim().length === 0) {
      setError("Title is required and cannot be empty.");
      return;
    }

    setIsSaving(true);

    try {
      const response = await fetch("/api/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(createForm),
      });

      if (!response.ok) {
        throw new Error(await parseError(response, "Unable to create note."));
      }

      const data = await response.json();
      setNotes((currentNotes) => [data.note, ...currentNotes]);
      setCreateForm(emptyForm);
    } catch (createError) {
      setError(
        createError instanceof Error
          ? createError.message
          : "Unable to create note.",
      );
    } finally {
      setIsSaving(false);
    }
  }

  function startEditing(note: Note) {
    setEditingId(note.id);
    setEditForm({ title: note.title, content: note.content });
    setError("");
  }

  function cancelEditing() {
    setEditingId(null);
    setEditForm(emptyForm);
    setError("");
  }

  async function handleUpdate(noteId: string) {
    setError("");

    if (editForm.title.trim().length === 0) {
      setError("Title is required and cannot be empty.");
      return;
    }

    setIsSaving(true);

    try {
      const response = await fetch(`/api/notes/${noteId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editForm),
      });

      if (!response.ok) {
        throw new Error(await parseError(response, "Unable to update note."));
      }

      const data = await response.json();
      setNotes((currentNotes) =>
        currentNotes.map((note) =>
          note.id === noteId ? data.note : note,
        ),
      );
      cancelEditing();
    } catch (updateError) {
      setError(
        updateError instanceof Error
          ? updateError.message
          : "Unable to update note.",
      );
    } finally {
      setIsSaving(false);
    }
  }

  async function handleDelete(note: Note) {
    const confirmed = window.confirm(
      `Delete "${note.title}"? This action cannot be undone.`,
    );

    if (!confirmed) {
      return;
    }

    setError("");

    try {
      const response = await fetch(`/api/notes/${note.id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(await parseError(response, "Unable to delete note."));
      }

      setNotes((currentNotes) =>
        currentNotes.filter((currentNote) => currentNote.id !== note.id),
      );

      if (editingId === note.id) {
        cancelEditing();
      }
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Unable to delete note.",
      );
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f7fb] px-4 py-6 text-[#1e2430] sm:px-6 lg:px-8">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6">
        <header className="flex flex-col gap-2 border-b border-[#d9dee8] pb-5 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-[#5864a8]">
              JSON Notes
            </p>
            <h1 className="mt-1 text-3xl font-bold text-[#111827] sm:text-4xl">
              Notes Manager
            </h1>
          </div>
          <p className="max-w-xl text-sm leading-6 text-[#5f6878]">
            Create, edit, and keep notes in a local JSON file through Next.js
            API routes.
          </p>
        </header>

        {error ? (
          <div
            className="rounded-md border border-[#f1b8b8] bg-[#fff0f0] px-4 py-3 text-sm font-medium text-[#a32626]"
            role="alert"
          >
            {error}
          </div>
        ) : null}

        <section className="grid gap-6 lg:grid-cols-[minmax(280px,360px)_1fr]">
          <form
            className="flex flex-col gap-4 rounded-md border border-[#d9dee8] bg-white p-5 shadow-sm"
            onSubmit={handleCreate}
          >
            <div>
              <h2 className="text-xl font-semibold text-[#111827]">
                Create note
              </h2>
            </div>

            <label className="flex flex-col gap-2 text-sm font-medium text-[#394252]">
              Title
              <input
                className="rounded-md border border-[#cbd2df] px-3 py-2 text-base outline-none transition focus:border-[#5864a8] focus:ring-2 focus:ring-[#d8dcff]"
                value={createForm.title}
                onChange={(event) =>
                  setCreateForm((form) => ({
                    ...form,
                    title: event.target.value,
                  }))
                }
                placeholder="Meeting notes"
              />
            </label>

            <label className="flex flex-col gap-2 text-sm font-medium text-[#394252]">
              Content
              <textarea
                className="min-h-40 resize-y rounded-md border border-[#cbd2df] px-3 py-2 text-base outline-none transition focus:border-[#5864a8] focus:ring-2 focus:ring-[#d8dcff]"
                value={createForm.content}
                onChange={(event) =>
                  setCreateForm((form) => ({
                    ...form,
                    content: event.target.value,
                  }))
                }
                placeholder="Write the details here."
              />
            </label>

            <button
              className="rounded-md bg-[#263a8b] px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-[#1d2d70] disabled:cursor-not-allowed disabled:bg-[#8f98c6]"
              disabled={isSaving}
              type="submit"
            >
              {isSaving ? "Saving..." : "Create note"}
            </button>
          </form>

          <section className="flex flex-col gap-4">
            <div className="flex items-center justify-between gap-4">
              <h2 className="text-xl font-semibold text-[#111827]">
                All notes
              </h2>
              <span className="rounded-md border border-[#d9dee8] bg-white px-3 py-1 text-sm font-medium text-[#5f6878]">
                {notes.length} {notes.length === 1 ? "note" : "notes"}
              </span>
            </div>

            {isLoading ? (
              <div className="rounded-md border border-[#d9dee8] bg-white p-6 text-[#5f6878]">
                Loading notes...
              </div>
            ) : sortedNotes.length === 0 ? (
              <div className="rounded-md border border-dashed border-[#b8c0ce] bg-white p-8 text-center">
                <h3 className="text-lg font-semibold text-[#111827]">
                  No notes yet
                </h3>
                <p className="mt-2 text-sm text-[#5f6878]">
                  Create your first note with the form.
                </p>
              </div>
            ) : (
              <div className="grid gap-4">
                {sortedNotes.map((note) => {
                  const isEditing = editingId === note.id;

                  return (
                    <article
                      className="rounded-md border border-[#d9dee8] bg-white p-5 shadow-sm"
                      key={note.id}
                    >
                      {isEditing ? (
                        <div className="flex flex-col gap-4">
                          <label className="flex flex-col gap-2 text-sm font-medium text-[#394252]">
                            Title
                            <input
                              className="rounded-md border border-[#cbd2df] px-3 py-2 text-base outline-none transition focus:border-[#5864a8] focus:ring-2 focus:ring-[#d8dcff]"
                              value={editForm.title}
                              onChange={(event) =>
                                setEditForm((form) => ({
                                  ...form,
                                  title: event.target.value,
                                }))
                              }
                            />
                          </label>

                          <label className="flex flex-col gap-2 text-sm font-medium text-[#394252]">
                            Content
                            <textarea
                              className="min-h-32 resize-y rounded-md border border-[#cbd2df] px-3 py-2 text-base outline-none transition focus:border-[#5864a8] focus:ring-2 focus:ring-[#d8dcff]"
                              value={editForm.content}
                              onChange={(event) =>
                                setEditForm((form) => ({
                                  ...form,
                                  content: event.target.value,
                                }))
                              }
                            />
                          </label>

                          <div className="flex flex-wrap gap-2">
                            <button
                              className="rounded-md bg-[#263a8b] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[#1d2d70] disabled:cursor-not-allowed disabled:bg-[#8f98c6]"
                              disabled={isSaving}
                              onClick={() => handleUpdate(note.id)}
                              type="button"
                            >
                              Save
                            </button>
                            <button
                              className="rounded-md border border-[#b8c0ce] px-4 py-2 text-sm font-semibold text-[#394252] transition hover:bg-[#f0f3f8]"
                              onClick={cancelEditing}
                              type="button"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        <div className="flex flex-col gap-4">
                          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                            <div className="min-w-0">
                              <h3 className="break-words text-xl font-semibold text-[#111827]">
                                {note.title}
                              </h3>
                              <p className="mt-2 whitespace-pre-wrap break-words text-sm leading-6 text-[#394252]">
                                {note.content || "No content added."}
                              </p>
                            </div>
                            <div className="flex shrink-0 gap-2">
                              <button
                                className="rounded-md border border-[#b8c0ce] px-3 py-2 text-sm font-semibold text-[#394252] transition hover:bg-[#f0f3f8]"
                                onClick={() => startEditing(note)}
                                type="button"
                              >
                                Edit
                              </button>
                              <button
                                className="rounded-md border border-[#e7b3b3] px-3 py-2 text-sm font-semibold text-[#a32626] transition hover:bg-[#fff0f0]"
                                onClick={() => handleDelete(note)}
                                type="button"
                              >
                                Delete
                              </button>
                            </div>
                          </div>

                          <dl className="grid gap-2 border-t border-[#edf0f5] pt-3 text-xs text-[#687385] sm:grid-cols-2">
                            <div>
                              <dt className="font-semibold uppercase tracking-wide">
                                Created
                              </dt>
                              <dd>{formatDate(note.createdAt)}</dd>
                            </div>
                            <div>
                              <dt className="font-semibold uppercase tracking-wide">
                                Updated
                              </dt>
                              <dd>{formatDate(note.updatedAt)}</dd>
                            </div>
                          </dl>
                        </div>
                      )}
                    </article>
                  );
                })}
              </div>
            )}
          </section>
        </section>
      </div>
    </main>
  );
}
