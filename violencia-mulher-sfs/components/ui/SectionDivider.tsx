export default function SectionDivider({
  id,
  titulo,
  kicker,
}: {
  id: string;
  titulo: string;
  kicker?: string;
}) {
  return (
    <div id={id} className="scroll-mt-20 pt-16 md:pt-24">
      {kicker && (
        <p className="font-sans uppercase tracking-widest text-xs text-verde font-semibold mb-2">
          {kicker}
        </p>
      )}
      <h2 className="font-serif font-black text-3xl md:text-5xl leading-tight">{titulo}</h2>
    </div>
  );
}
