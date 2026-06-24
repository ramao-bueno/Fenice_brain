import { NextRequest, NextResponse } from "next/server";
import {
  inicializarTabela,
  inserirApoiador,
  emailJaCadastrado,
  listarApoiadores,
} from "@/lib/db";

export type Apoiador = {
  id: string;
  nome: string;
  contato: string;
  email: string;
  registradoEm: string;
};

const TEM_DB = !!process.env.DATABASE_URL;

// ── Persistência local (desenvolvimento sem Neon) ─────────────────────────────
async function lerLocal(): Promise<Apoiador[]> {
  const { readFileSync } = await import("fs");
  const { join } = await import("path");
  try {
    return JSON.parse(
      readFileSync(join(process.cwd(), "cadastros", "apoiadores.json"), "utf-8")
    );
  } catch {
    return [];
  }
}

async function salvarLocal(lista: Apoiador[]) {
  const { writeFileSync, mkdirSync } = await import("fs");
  const { join } = await import("path");
  const pasta = join(process.cwd(), "cadastros");
  mkdirSync(pasta, { recursive: true });
  writeFileSync(
    join(pasta, "apoiadores.json"),
    JSON.stringify(lista, null, 2),
    "utf-8"
  );
}

// ── POST — cadastra apoiador ──────────────────────────────────────────────────
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { nome, contato, email } = body as Partial<Apoiador>;

    if (!nome?.trim() || !email?.trim()) {
      return NextResponse.json(
        { erro: "Nome e e-mail são obrigatórios." },
        { status: 400 }
      );
    }

    const novo: Apoiador = {
      id: crypto.randomUUID(),
      nome: nome.trim(),
      contato: (contato ?? "").trim(),
      email: email.trim().toLowerCase(),
      registradoEm: new Date().toISOString(),
    };

    if (TEM_DB) {
      await inicializarTabela();
      if (await emailJaCadastrado(novo.email)) {
        return NextResponse.json(
          { erro: "E-mail já cadastrado." },
          { status: 409 }
        );
      }
      await inserirApoiador(novo);
      return NextResponse.json({ ok: true, id: novo.id, modo: "neon" }, { status: 201 });
    }

    // Fallback: persiste localmente (dev sem DATABASE_URL)
    const lista = await lerLocal();
    if (lista.some((a) => a.email === novo.email)) {
      return NextResponse.json({ erro: "E-mail já cadastrado." }, { status: 409 });
    }
    lista.push(novo);
    await salvarLocal(lista);
    return NextResponse.json({ ok: true, id: novo.id, modo: "local" }, { status: 201 });
  } catch {
    return NextResponse.json({ erro: "Erro interno." }, { status: 500 });
  }
}

// ── GET — lista apoiadores ────────────────────────────────────────────────────
export async function GET() {
  if (TEM_DB) {
    await inicializarTabela();
    const lista = await listarApoiadores();
    return NextResponse.json({ total: lista.length, apoiadores: lista });
  }
  const lista = await lerLocal();
  return NextResponse.json({ total: lista.length, apoiadores: lista });
}
