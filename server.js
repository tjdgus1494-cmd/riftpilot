"use strict";

const http = require("http");
const https = require("https");
const fs = require("fs");
const path = require("path");
const { URL } = require("url");

const PORT = Number(process.env.PORT || 5177);
const HOST = process.env.HOST || "127.0.0.1";
const ROOT = __dirname;
const LIVE_URL = "https://127.0.0.1:2999/liveclientdata/allgamedata";
const REPLAY_PLAYBACK_URL = "https://127.0.0.1:2999/replay/playback";
const REPLAY_GAME_URL = "https://127.0.0.1:2999/replay/game";
const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml"
};

let ddragonCache = null;

function sendJson(res, status, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Content-Length": Buffer.byteLength(body)
  });
  res.end(body);
}

function requestJson(target, options = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(target);
    const client = url.protocol === "https:" ? https : http;
    const body = options.body ? JSON.stringify(options.body) : "";
    const headers = {
      "Accept": "application/json",
      "User-Agent": "local-lol-item-recommender"
    };
    if (body) {
      headers["Content-Type"] = "application/json";
      headers["Content-Length"] = Buffer.byteLength(body);
    }

    const req = client.request(
      url,
      {
        method: options.method || "GET",
        agent: options.agent,
        timeout: options.timeout || 5000,
        headers
      },
      (response) => {
        const chunks = [];
        response.on("data", (chunk) => chunks.push(chunk));
        response.on("end", () => {
          const text = Buffer.concat(chunks).toString("utf8");
          if (response.statusCode < 200 || response.statusCode >= 300) {
            reject(new Error(`HTTP ${response.statusCode}: ${text.slice(0, 180)}`));
            return;
          }
          if (!text.trim()) {
            resolve({});
            return;
          }
          try {
            resolve(JSON.parse(text));
          } catch (error) {
            reject(new Error(`JSON parse failed: ${error.message}`));
          }
        });
      }
    );

    req.on("timeout", () => {
      req.destroy(new Error("request timed out"));
    });
    req.on("error", reject);
    if (body) req.write(body);
    req.end();
  });
}

function readRequestBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (chunk) => chunks.push(chunk));
    req.on("end", () => {
      const text = Buffer.concat(chunks).toString("utf8");
      if (!text.trim()) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(text));
      } catch (error) {
        reject(new Error(`Request JSON parse failed: ${error.message}`));
      }
    });
    req.on("error", reject);
  });
}

async function loadDataDragon(locale) {
  const now = Date.now();
  if (ddragonCache && ddragonCache.locale === locale && now - ddragonCache.loadedAt < 6 * 60 * 60 * 1000) {
    return ddragonCache.payload;
  }

  const versions = await requestJson("https://ddragon.leagueoflegends.com/api/versions.json", { timeout: 7000 });
  const version = versions[0];
  const base = `https://ddragon.leagueoflegends.com/cdn/${version}/data/${locale}`;
  const [items, champions] = await Promise.all([
    requestJson(`${base}/item.json`, { timeout: 7000 }),
    requestJson(`${base}/champion.json`, { timeout: 7000 })
  ]);

  ddragonCache = {
    locale,
    loadedAt: now,
    payload: { ok: true, version, locale, items, champions }
  };
  return ddragonCache.payload;
}

async function handleApi(req, res, pathname) {
  if (pathname === "/api/health") {
    sendJson(res, 200, { ok: true, liveUrl: LIVE_URL, time: new Date().toISOString() });
    return;
  }

  if (pathname === "/api/live") {
    try {
      const agent = new https.Agent({ rejectUnauthorized: false });
      const data = await requestJson(LIVE_URL, { agent, timeout: 3200 });
      sendJson(res, 200, { ok: true, data });
    } catch (error) {
      sendJson(res, 503, {
        ok: false,
        message: "League Client live data is unavailable",
        detail: error.message
      });
    }
    return;
  }

  if (pathname === "/api/replay") {
    const agent = new https.Agent({ rejectUnauthorized: false });
    const payload = { ok: false, replay: null, game: null, live: null, errors: {} };

    try {
      payload.replay = await requestJson(REPLAY_PLAYBACK_URL, { agent, timeout: 2500 });
      payload.ok = true;
    } catch (error) {
      payload.errors.replay = error.message;
    }

    try {
      payload.game = await requestJson(REPLAY_GAME_URL, { agent, timeout: 2500 });
      payload.ok = true;
    } catch (error) {
      payload.errors.game = error.message;
    }

    try {
      payload.live = await requestJson(LIVE_URL, { agent, timeout: 2500 });
      payload.ok = true;
    } catch (error) {
      payload.errors.live = error.message;
    }

    sendJson(res, payload.ok ? 200 : 503, {
      ...payload,
      message: payload.ok ? "League client data reachable" : "Replay API and live data are unavailable"
    });
    return;
  }

  if (pathname === "/api/replay/playback") {
    if (req.method !== "POST") {
      sendJson(res, 405, { ok: false, message: "POST required" });
      return;
    }

    try {
      const body = await readRequestBody(req);
      const agent = new https.Agent({ rejectUnauthorized: false });
      const data = await requestJson(REPLAY_PLAYBACK_URL, {
        method: "POST",
        body,
        agent,
        timeout: 2500
      });
      sendJson(res, 200, { ok: true, data });
    } catch (error) {
      sendJson(res, 503, {
        ok: false,
        message: "Replay playback control failed",
        detail: error.message
      });
    }
    return;
  }

  if (pathname === "/api/ddragon") {
    try {
      const requestUrl = new URL(req.url, `http://${req.headers.host}`);
      const locale = requestUrl.searchParams.get("locale") || "ko_KR";
      const data = await loadDataDragon(locale);
      sendJson(res, 200, data);
    } catch (error) {
      sendJson(res, 502, {
        ok: false,
        message: "Data Dragon could not be loaded",
        detail: error.message
      });
    }
    return;
  }

  sendJson(res, 404, { ok: false, message: "Unknown API route" });
}

function serveStatic(res, pathname) {
  const requested = pathname === "/" ? "/index.html" : pathname;
  const normalized = path.normalize(decodeURIComponent(requested)).replace(/^(\.\.[/\\])+/, "");
  const filePath = path.join(ROOT, normalized);
  const resolved = path.resolve(filePath);

  if (!resolved.startsWith(ROOT)) {
    res.writeHead(403, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Forbidden");
    return;
  }

  fs.readFile(resolved, (error, data) => {
    if (error) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("Not found");
      return;
    }
    const ext = path.extname(resolved).toLowerCase();
    res.writeHead(200, {
      "Content-Type": MIME[ext] || "application/octet-stream",
      "Cache-Control": "no-store"
    });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const requestUrl = new URL(req.url, `http://${req.headers.host}`);
  if (requestUrl.pathname.startsWith("/api/")) {
    handleApi(req, res, requestUrl.pathname);
    return;
  }
  serveStatic(res, requestUrl.pathname);
});

server.listen(PORT, HOST, () => {
  console.log(`LoL item recommender running at http://${HOST}:${PORT}/`);
});
