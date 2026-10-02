export type SectorCode = "TI" | "RH" | "ADM" | "COMPRAS";
export type SessionUser = { id: string; name: string; email: string; role: string; sector: SectorCode; accessToken?: string; refreshToken?: string };
