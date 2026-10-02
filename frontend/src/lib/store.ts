import seed from "@/data/seed.json";

export type AppData = typeof seed;
const STORAGE_KEY = "gestao-materiais:data:v1";

function cloneSeed(): AppData {
  return JSON.parse(JSON.stringify(seed)) as AppData;
}

export function loadData(): AppData {
  if (typeof window === "undefined") return cloneSeed();
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return cloneSeed();
    const parsed = JSON.parse(raw) as AppData;
    return parsed.schemaVersion === seed.schemaVersion ? parsed : cloneSeed();
  } catch {
    return cloneSeed();
  }
}

export function saveData(data: AppData): void {
  if (typeof window !== "undefined") window.localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

export function resetData(): AppData {
  const data = cloneSeed();
  saveData(data);
  return data;
}

export function createId(prefix: string): string {
  return `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}
