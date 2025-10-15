import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import Filters from "../components/Filters";
import ResultsTable from "../components/ResultsTable";

export default function Home() {
  const { data: productos } = useQuery({
    queryKey: ["productos"],
    queryFn: () => api<{ items: any[] }>("/api/productos"),
  });
  const { data: provincias } = useQuery({
    queryKey: ["provincias"],
    queryFn: () => api<{ items: any[] }>("/api/listas/provincias"),
  });

  const [producto, setProducto] = useState<string | undefined>();
  const [provincia, setProvincia] = useState<string | undefined>();

  const { data: search } = useQuery({
    queryKey: ["search", producto, provincia],
    queryFn: () =>
      api<{ items: any[] }>(
        `/api/search?${new URLSearchParams({
          ...(producto ? { producto } : {}),
          ...(provincia ? { provincia } : {}),
          orden: "precio",
          limit: "50",
        }).toString()}`
      ),
  });

  const items = search?.items ?? [];

  return (
    <div>
      <Filters
        productos={productos?.items || []}
        provincias={provincias?.items || []}
        producto={producto}
        setProducto={setProducto}
        provincia={provincia}
        setProvincia={setProvincia}
        count={items.length}
      />
      <ResultsTable items={items} />
    </div>
  );
}
