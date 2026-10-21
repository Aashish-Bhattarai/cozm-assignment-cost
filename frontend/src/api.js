// Every call to the backend lives here, so components never build URLs themselves.
// The Vite dev server proxies /api to Django (see vite.config.js).

const API_BASE = "/api";

const SERVER_DOWN_ERRORS = {
  __all__: ["Could not reach the server. Is the backend running?"],
};

// Returns { data } on success or { errors } on failure, both shaped for direct
// rendering: errors is the API's field-name -> messages object.
async function request(path, options) {
  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, options);
  } catch {
    return { errors: SERVER_DOWN_ERRORS };
  }

  let body;
  try {
    body = await response.json();
  } catch {
    // A non-JSON reply means the server answered but not with our API.
    return { errors: SERVER_DOWN_ERRORS };
  }

  if (!response.ok) {
    return { errors: body.errors ?? { __all__: ["The request failed."] } };
  }
  return { data: body };
}

export function fetchEstimate(inputs) {
  return request("/estimate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputs),
  });
}

export function fetchImmigration(sponsorSize) {
  return request(`/immigration?sponsor_size=${encodeURIComponent(sponsorSize)}`);
}
