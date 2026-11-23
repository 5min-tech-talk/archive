# [Weekly 5-Min Tech Talk] Web Deployment Series, Part 1: How My Code Reaches an https:// URL

<table>
  <tbody><tr><td><b>Presenter</b></td><td>Olivia Lee</td></tr></tbody>
  <tbody><tr><td><b>Date</b></td><td>2026-11-04</td></tr></tbody>
  <tbody><tr><td><b>Keywords</b></td><td>SSH, pm2, DNS, nginx, Reverse Proxy, HTTPS, Certbot</td></tr></tbody>
  <tbody><tr><td><b>Series</b></td><td>Web Deployment, Step by Step — Part 1 of 2</td></tr></tbody>
</table>

---

## TL;DR
Deployment means connecting two paths: **① running my code on a server**, and **② letting users find that code through a domain**.
This note walks through both paths using a real task: deploying a Next.js admin page to a new domain.

## Why This Topic
- "What does it take to serve my Next.js page on a new domain?"
- Where it came from: I deployed a Next.js admin page to a new server and domain for the first time. I could follow the steps, but I didn't have the big picture of *why* each step was needed.

## Core Concepts
- **Server:** Just a computer somewhere else. You connect to it over SSH.
- **Build vs. Run:** Building produces the output; running keeps it alive. If you use Next.js server features (SSR), a Node process must keep running after the build. Static builds (Flutter web, static Next.js) only need their files served.
- **DNS:** The map that turns a domain name into a server IP.
- **nginx (reverse proxy):** The front desk. When one server hosts several services, it looks at the requested domain and decides where to send the request.
- **HTTPS / TLS certificate:** Lets the server prove "I really am this domain" and encrypts traffic between the browser and the server.

## Deep Dive

```text
① My code → running on the server
   GitHub → git clone → npm ci → build → run with pm2

② User → domain → my code
   admin.example.com → DNS (A record) → server IP → nginx (443, HTTPS) → Next.js process
```

1. **SSH in and fetch the code:** `git clone` → `npm ci` → `npm run build`
2. **Run it:** pm2 starts the Node process and keeps it alive (a process manager).
3. **Connect DNS:** Add an A record with your DNS provider so the domain points to the server IP.
4. **Route with nginx:** The same server runs Django, Flutter web, and Next.js. nginx routes each request by domain.
5. **Enable HTTPS:** Issue a certificate with Certbot and serve it on port 443.

## In Practice

```nginx
server_name admin.example.com;
location / {
    proxy_pass http://127.0.0.1:<APP_PORT>;
}
```

- "Requests for this domain go to the Next.js process on this same machine."
- `127.0.0.1` is the server itself; `<APP_PORT>` is the port Next.js listens on.

## Key Takeaways
- Deployments got stuck more often because of **environment differences** than because of code.
  - The server's Node version didn't match, so I had to align the build environment.
  - npm dependency conflicts showed up.
  - The new domain had to be added to Google OAuth's *Authorized JavaScript origins* before login worked.
- **`127.0.0.1` in nginx doesn't make the app private.** `next start` listens on all interfaces (`0.0.0.0`) by default, so port 3000 can be reachable from outside unless a firewall blocks it. To keep it internal, start it with `-H 127.0.0.1`.
- **On a shared server,** don't edit existing nginx configs. Add a new one, validate it with `nginx -t`, then reload.
- A checklist for any new service: pick a server → deploy the code → run it (or place static files) → connect DNS → add an nginx rule → enable HTTPS.

## Discussion
- Can we stop SSH-ing in to repeat `pull → build → restart` by hand? → **Part 2 (CI/CD)**
- How does the request path change for servers behind Cloudflare? → **Part 2**

## Glossary
- **SSH:** A protocol for securely connecting to a remote server.
- **pm2:** A process manager that runs Node apps in the background and restarts them if they crash.
- **A record:** A DNS record that maps a domain to an IPv4 address.
- **Reverse proxy:** A server that receives client requests and forwards them to the right internal service.
- **Certbot:** A tool that issues and renews Let's Encrypt certificates automatically.

## References
- [Next.js — Deploying (Self-hosting)](https://nextjs.org/docs/app/getting-started/deploying)
- [PM2 Quick Start](https://pm2.keymetrics.io/docs/usage/quick-start/)
- [nginx — Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Certbot](https://certbot.eff.org/)

---
➡️ Next: [Part 2 — Safer Requests, Automated Deploys](./20261112_web_deployment_part2_cloudflare_tunnel_and_cicd.md)
