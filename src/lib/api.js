const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

let authToken = localStorage.getItem("dna-token") || "";

function headers(extra = {}) {
  return {
    ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
    ...extra
  };
}

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: headers(options.headers)
    });
  } catch (error) {
    throw new Error(`Cannot reach API at ${API_BASE}. Make sure the FastAPI server is running.`);
  }

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : await response.text();

  if (!response.ok) {
    const detail = typeof payload === "string" ? payload : payload.detail || "Request failed";
    throw new Error(detail);
  }

  return payload;
}

export function setToken(token) {
  authToken = token || "";
  if (authToken) {
    localStorage.setItem("dna-token", authToken);
  } else {
    localStorage.removeItem("dna-token");
  }
}

export function getMediaUrl(path) {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return `${API_BASE}${path}`;
}

export const api = {
  get token() {
    return authToken;
  },
  login(credentials) {
    return request("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials)
    });
  },
  register(payload) {
    return request("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  logout() {
    return request("/api/auth/logout", { method: "POST" });
  },
  changePassword(payload) {
    return request("/api/auth/change-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  getMe() {
    return request("/api/users/me");
  },
  getUsers() {
    return request("/api/users");
  },
  getOtherUsers() {
    return request("/api/users/others");
  },
  encrypt(formData) {
    return request("/api/images/encrypt", {
      method: "POST",
      body: formData
    });
  },
  upload(formData) {
    return request("/api/images/upload", {
      method: "POST",
      body: formData
    });
  },
  getImages() {
    return request("/api/images");
  },
  getSent() {
    return request("/api/images/sent");
  },
  share(payload) {
    return request("/api/shares", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  getReceived() {
    return request("/api/shares/received");
  },
  decryptShare(shareId) {
    return request(`/api/shares/${shareId}/decrypt`, {
      method: "POST"
    });
  },
  getAnalytics(imageId) {
    return request(`/api/analytics/${imageId}`);
  },
  getActivity(limit = 50) {
    return request(`/api/activity?limit=${limit}`);
  }
};
