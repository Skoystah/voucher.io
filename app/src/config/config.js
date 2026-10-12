// console.log("hostname");
// console.log(window.location.hostname);
//
// const SERVER_IP = "192.168.178.20"
// const TAILSCALE_IP = "100.64.0.2"
// const SERVER_DOMAIN = "voucher.abisko.fyi"
// const GOOGLE_URL = "https://voucher-io-881141325435.europe-west1.run.app" 
//
// let API_URL
// if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
//     // ? "https://localhost:8000"
//     API_URL = "http://localhost:8000";
// } else if (window.location.hostname === SERVER_IP) {
//     // API_URL = `http://${SERVER_IP}:8000`;
//     API_URL = `https://${SERVER_DOMAIN}/api`;
// } else if (window.location.hostname === SERVER_DOMAIN) {
//     // API_URL = `http://${TAILSCALE_IP}:8000`;
//     API_URL = `https://${SERVER_DOMAIN}/api`;
// } else {
//     API_URL = GOOGLE_URL;
// }
//
// console.log(`API URL : ${API_URL}`);

const API_URL = "/api";
export { API_URL };
