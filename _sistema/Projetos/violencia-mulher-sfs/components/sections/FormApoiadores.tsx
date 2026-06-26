"use client";
import { useState } from "react";

type Estado = "idle" | "enviando" | "ok" | "erro" | "duplicado";

export default function FormApoiadores() {
  const [estado, setEstado] = useState<Estado>("idle");
  const [dados, setDados] = useState({ nome: "", contato: "", email: "" });
  const [msg, setMsg] = useState("");

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setDados((d) => ({ ...d, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setEstado("enviando");

    try {
      const res = await fetch("/api/apoiadores", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
      });
      const json = await res.json();

      if (res.status === 409) {
        setMsg("Este e-mail já está cadastrado. Obrigado pelo seu apoio!");
        setEstado("duplicado");
      } else if (!res.ok) {
        setMsg(json.erro ?? "Ocorreu um erro. Tente novamente.");
        setEstado("erro");
      } else {
        setEstado("ok");
      }
    } catch {
      setMsg("Sem conexão. Verifique sua internet e tente novamente.");
      setEstado("erro");
    }
  }

  if (estado === "ok") {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-8 text-center">
        <div
          className="w-16 h-16 rounded-full flex items-center justify-center text-2xl shadow-lg font-bold"
          style={{ background: "#7dc242", color: "#001f0e" }}
        >
          ✓
        </div>
        <p className="text-white font-serif font-bold text-2xl">Obrigado, {dados.nome}!</p>
        <p className="text-white/70 text-sm max-w-xs leading-relaxed">
          Seu cadastro foi registrado com sucesso. Entraremos em contato em breve.
        </p>
        <button
          onClick={() => { setEstado("idle"); setDados({ nome: "", contato: "", email: "" }); }}
          className="mt-2 text-xs text-white/40 underline hover:text-white/70 transition-colors"
        >
          Cadastrar outro apoiador
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      {(
        [
          { label: "Nome completo",  name: "nome",    type: "text",  placeholder: "Seu nome" },
          { label: "Contato / Tel.", name: "contato", type: "tel",   placeholder: "(47) 9 0000-0000" },
          { label: "E-mail",         name: "email",   type: "email", placeholder: "voce@email.com" },
        ] as const
      ).map(({ label, name, type, placeholder }) => (
        <div key={name} className="flex flex-col gap-1">
          <label className="text-white/70 text-xs font-semibold uppercase tracking-widest">
            {label}
          </label>
          <input
            type={type}
            name={name}
            value={dados[name]}
            onChange={handleChange}
            placeholder={placeholder}
            required={name !== "contato"}
            className="rounded-xl px-4 py-3 text-base font-medium text-ink bg-white/95
                       placeholder:text-ink/40 border-2 border-transparent
                       focus:border-[#7dc242] focus:outline-none transition-colors"
          />
        </div>
      ))}

      {(estado === "erro" || estado === "duplicado") && (
        <p className="text-xs rounded-lg px-3 py-2"
          style={{ background: estado === "duplicado" ? "rgba(125,194,66,0.2)" : "rgba(178,58,72,0.3)", color: "#fff" }}>
          {msg}
        </p>
      )}

      <button
        type="submit"
        disabled={estado === "enviando"}
        className="mt-2 rounded-xl py-3 px-6 font-bold text-sm uppercase tracking-widest
                   transition-all active:scale-95 disabled:opacity-60"
        style={{ background: "#7dc242", color: "#001f0e" }}
      >
        {estado === "enviando" ? "Registrando…" : "Quero Apoiar →"}
      </button>
    </form>
  );
}
