import { neon, type NeonQueryFunction } from "@neondatabase/serverless";

let _sql: NeonQueryFunction<false, false> | null = null;

function sql() {
  if (!_sql) _sql = neon(process.env.DATABASE_URL!);
  return _sql;
}

export async function inicializarTabela() {
  await sql()`
    CREATE TABLE IF NOT EXISTS apoiadores (
      id          TEXT PRIMARY KEY,
      nome        TEXT NOT NULL,
      contato     TEXT NOT NULL DEFAULT '',
      email       TEXT NOT NULL UNIQUE,
      registrado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
  `;
}

export async function inserirApoiador(a: {
  id: string;
  nome: string;
  contato: string;
  email: string;
}) {
  await sql()`
    INSERT INTO apoiadores (id, nome, contato, email)
    VALUES (${a.id}, ${a.nome}, ${a.contato}, ${a.email})
  `;
}

export async function emailJaCadastrado(email: string): Promise<boolean> {
  const rows = await sql()`
    SELECT 1 FROM apoiadores WHERE email = ${email} LIMIT 1
  `;
  return rows.length > 0;
}

export async function listarApoiadores() {
  return sql()`
    SELECT id, nome, contato, email, registrado_em AS "registradoEm"
    FROM apoiadores
    ORDER BY registrado_em DESC
  `;
}
