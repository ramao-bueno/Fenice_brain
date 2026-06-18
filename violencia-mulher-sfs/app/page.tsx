import Abertura from "@/components/sections/Abertura";
import Problema from "@/components/sections/Problema";
import Numeros from "@/components/sections/Numeros";
import Recortes from "@/components/sections/Recortes";
import Propostas from "@/components/sections/Propostas";
import Metodologia from "@/components/sections/Metodologia";
import Creditos from "@/components/sections/Creditos";

export default function Home() {
  return (
    <main>
      <Abertura />
      <div className="max-w-5xl mx-auto px-4">
        <Problema />
        <Numeros />
        <Recortes />
        <Propostas />
        <Metodologia />
      </div>
      <Creditos />
    </main>
  );
}
