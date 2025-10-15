export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function api<T>(path: string, params?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { headers: { "Accept": "application/json" }, ...params });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}
