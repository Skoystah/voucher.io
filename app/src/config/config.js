const API_URL = (window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1")
    ? "https://localhost:8000"
    : "https://voucher-io-881141325435.europe-west1.run.app";

export { API_URL };
