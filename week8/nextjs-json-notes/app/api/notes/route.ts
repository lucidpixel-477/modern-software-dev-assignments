import { NextResponse } from "next/server";
import { createNote, getNotes } from "@/lib/notes";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const notes = await getNotes();
    return NextResponse.json({ notes });
  } catch {
    return NextResponse.json(
      { error: "Unable to load notes." },
      { status: 500 },
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const note = await createNote(body);

    return NextResponse.json({ note }, { status: 201 });
  } catch (error) {
    const message =
      error instanceof Error
        ? error.message
        : "Unable to create the note. Please try again.";

    return NextResponse.json({ error: message }, { status: 400 });
  }
}
