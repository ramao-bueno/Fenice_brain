export default function BigStat({
  valor,
  rotulo,
  nota,
  tom = "default",
}: {
  valor: string;
  rotulo: string;
  nota?: string;
  tom?: "default" | "alerta";
}) {
  return (
    <div className="flex flex-col gap-1">
      <span
        className={`font-serif font-black leading-none text-5xl md:text-7xl ${
          tom === "alerta" ? "text-alerta" : "text-verde"
        }`}
      >
        {valor}
      </span>
      <span className="font-sans font-semibold text-base md:text-lg">{rotulo}</span>
      {nota && <span className="text-sm text-ink/60">{nota}</span>}
    </div>
  );
}
