// Banco de dados — Supabase PostgreSQL
// Migrado de Neon → Supabase em 2026-06-25 (elimina dependência de compute hours)
import { createClient } from "@supabase/supabase-js";

function supabase() {
  const url = process.env.SUPABASE_URL!;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  return createClient(url, key, { auth: { persistSession: false } });
}

export async function inicializarTabela() {
  // Tabela criada via migration no Supabase — esta função é no-op em produção
}

export async function inserirApoiador(a: {
  id: string;
  nome: string;
  contato: string;
  email: string;
}) {
  const { error } = await supabase()
    .from("apoiadores_observatorio")
    .insert({ id: a.id, nome: a.nome, contato: a.contato, email: a.email });
  if (error) throw new Error(error.message);
}

export async function emailJaCadastrado(email: string): Promise<boolean> {
  const { data } = await supabase()
    .from("apoiadores_observatorio")
    .select("id")
    .eq("email", email)
    .limit(1);
  return (data?.length ?? 0) > 0;
}

export async function listarApoiadores() {
  const { data, error } = await supabase()
    .from("apoiadores_observatorio")
    .select("id, nome, contato, email, registrado_em")
    .order("registrado_em", { ascending: false });
  if (error) throw new Error(error.message);
  return (data ?? []).map((r) => ({ ...r, registradoEm: r.registrado_em }));
}
