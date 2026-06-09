import { NextResponse } from "next/server";
import { deleteNote, updateNote } from "@/lib/notes";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type NoteRouteContext = {
  params: Promise<{ id: string }>;
};

export async function PUT(request: Request, context: NoteRouteContext) {
  try {
    const { id } = await context.params;
    const body = await request.json();
    const note = await updateNote(id, body);

    if (!note) {
      return NextResponse.json({ error: "Note not found." }, { status: 404 });
    }

    return NextResponse.json({ note });
  } catch (error) {
    const message =
      error instanceof Error
        ? error.message
        : "Unable to update the note. Please try again.";

    return NextResponse.json({ error: message }, { status: 400 });
  }
}

export async function DELETE(_: Request, context: NoteRouteContext) {
  try {
    const { id } = await context.params;
    const deleted = await deleteNote(id);

    if (!deleted) {
      return NextResponse.json({ error: "Note not found." }, { status: 404 });
    }

    return NextResponse.json({ message: "Note deleted." });
  } catch {
    return NextResponse.json(
      { error: "Unable to delete the note. Please try again." },
      { status: 500 },
    );
  }
}
