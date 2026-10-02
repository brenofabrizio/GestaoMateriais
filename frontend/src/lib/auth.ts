import type { SessionUser, SectorCode } from "@/lib/session";

export type ApiSession = SessionUser & { accessToken: string; refreshToken: string };

const sectorCodes: SectorCode[] = ["TI", "RH", "ADM", "COMPRAS"];

function getSector(code?: string | null): SectorCode {
  const normalized = (code ?? "").toUpperCase();
  return sectorCodes.includes(normalized as SectorCode) ? normalized as SectorCode : "ADM";
}

export async function loginWithApi(apiUrl: string, email: string, password: string): Promise<ApiSession> {
  const tokenResponse = await fetch(`${apiUrl.replace(/\/$/, "")}/auth/token/`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password }),
  });
  if (!tokenResponse.ok) throw new Error("E-mail ou senha inválidos.");
  const tokens = await tokenResponse.json() as { access: string; refresh: string };
  const userResponse = await fetch(`${apiUrl.replace(/\/$/, "")}/auth/me/`, { headers: { Authorization: `Bearer ${tokens.access}` } });
  if (!userResponse.ok) throw new Error("Não foi possível carregar o perfil do usuário.");
  const user = await userResponse.json() as { id: string; email: string; full_name: string; area?: { code?: string }; roles?: { name: string }[] };
  return { id: String(user.id), name: user.full_name, email: user.email, role: user.roles?.[0]?.name ?? "Usuário", sector: getSector(user.area?.code), accessToken: tokens.access, refreshToken: tokens.refresh };
}
