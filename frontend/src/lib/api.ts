export const API_BASE = "/api/v1";

export const fetcher = (url: string) => fetch(url).then((res) => res.json());
