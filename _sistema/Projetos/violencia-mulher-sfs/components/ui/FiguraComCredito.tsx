import Image from "next/image";

export default function FiguraComCredito({
  src,
  alt,
  credito,
  className,
  ratio = "aspect-[16/9]",
}: {
  src: string;
  alt: string;
  credito: string;
  className?: string;
  ratio?: string;
}) {
  return (
    <figure className={className}>
      <div className={`relative w-full ${ratio} overflow-hidden rounded-xl`}>
        <Image src={src} alt={alt} fill className="object-cover" sizes="(max-width: 1024px) 100vw, 1024px" />
      </div>
      <figcaption className="text-xs text-ink/50 mt-2">{credito}</figcaption>
    </figure>
  );
}
