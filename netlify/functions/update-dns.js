exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, body: "Invalid JSON" };
  }

  const { hostname, ip } = body;

  const ALLOWED_HOSTS = [
    "serverres.dyndns.org",
    "servercor.dyndns.org",
    "serverfor.dyndns.org",
    "serverpe.dyndns.org",
  ];

  if (!hostname || !ALLOWED_HOSTS.includes(hostname)) {
    return { statusCode: 400, body: "Hostname no válido" };
  }

  if (!ip || !/^\d{1,3}(\.\d{1,3}){3}$/.test(ip)) {
    return { statusCode: 400, body: "IP no válida" };
  }

  const user = process.env.DYNDNS_USER;
  const pass = process.env.DYNDNS_PASS;

  if (!user || !pass) {
    return { statusCode: 500, body: "Credenciales no configuradas" };
  }

  const credentials = Buffer.from(`${user}:${pass}`).toString("base64");
  const url = `https://members.dyndns.org/nic/update?hostname=${hostname}&myip=${ip}`;

  try {
    const response = await fetch(url, {
      headers: {
        Authorization: `Basic ${credentials}`,
        "User-Agent": "DynDNS-Updater/1.0 rennisdaniel@gmail.com",
      },
    });

    const text = await response.text();

    if (text.startsWith("good") || text.startsWith("nochg")) {
      return {
        statusCode: 200,
        body: JSON.stringify({ ok: true, response: text.trim() }),
      };
    } else {
      return {
        statusCode: 502,
        body: JSON.stringify({ ok: false, response: text.trim() }),
      };
    }
  } catch (err) {
    return { statusCode: 500, body: `Error: ${err.message}` };
  }
};
