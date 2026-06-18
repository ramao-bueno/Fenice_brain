export default function Callout({ children }: { children: React.ReactNode }) {
  return (
    <aside className="border-l-4 border-verde bg-verde-tint/60 px-5 py-4 text-sm md:text-base text-ink/80 rounded-r-lg">
      {children}
    </aside>
  );
}
