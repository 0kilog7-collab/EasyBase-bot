from flask import Flask, request, jsonify, render_template_string
import requests
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

# ============ КЛЮЧИ ============
SNUSBASE_KEY = "sb5029dec66mht55m78fx8bsw6tm8a"
OFDATA_KEY = "DiC9ALodH5T12BfR"

SNUSBASE_URL = "https://api.snusbase.com/data/search"
OFDATA_BASE = "https://api.ofdata.ru/v2"

# ============ HTML ШАБЛОН ============
HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clearance — Search</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0a0f;
            color: #e2ddf5;
            font-family: 'Courier New', monospace;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: #13101f;
            border: 1px solid #2e2550;
            border-radius: 20px;
            padding: 30px 35px;
            max-width: 700px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(124, 77, 220, 0.15);
        }
        .logo {
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, #b084f5, #7c4ddc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 6px;
        }
        .subtitle {
            text-align: center;
            color: #5c5280;
            font-size: 11px;
            letter-spacing: 2px;
            margin-bottom: 25px;
        }
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 16px;
        }
        .search-box input {
            flex: 1;
            padding: 14px 18px;
            border-radius: 12px;
            border: 1px solid #2e2550;
            background: #0a0a0f;
            color: #c4a5ff;
            font-size: 16px;
            outline: none;
            font-family: 'Courier New', monospace;
        }
        .search-box input:focus { border-color: #7c4ddc; }
        .search-box input::placeholder { color: #3d2d6e; }
        .search-box button {
            padding: 14px 28px;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, #7c4ddc, #b084f5);
            color: #fff;
            font-weight: 700;
            font-size: 16px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            transition: 0.2s;
        }
        .search-box button:hover { opacity: 0.8; }
        .filters {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 16px;
            justify-content: center;
        }
        .filters span {
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 11px;
            color: #5c5280;
            border: 1px solid #2e2550;
            cursor: pointer;
            transition: 0.3s;
            letter-spacing: 0.5px;
        }
        .filters span:hover { border-color: #7c4ddc; color: #b084f5; }
        .filters span.active {
            border-color: #7c4ddc;
            color: #b084f5;
            background: rgba(124, 77, 220, 0.12);
        }
        .result {
            background: #0a0a0f;
            border: 1px solid #1a1528;
            border-radius: 12px;
            padding: 18px;
            min-height: 80px;
            font-size: 13px;
            line-height: 1.7;
            color: #aaa;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 460px;
            overflow-y: auto;
        }
        .result .empty { color: #3d2d6e; text-align: center; padding: 20px 0; }
        .result .source { color: #b084f5; font-weight: 700; font-size: 11px; }
        .result .key { color: #b084f5; }
        .result .error { color: #ff4444; }
        .stats {
            display: flex;
            justify-content: space-between;
            margin-top: 14px;
            font-size: 11px;
            color: #3d2d6e;
        }
        .stats span { color: #5c5280; }
        .loading { color: #7c4ddc; animation: pulse 1s infinite; }
        @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #0d0d0d; }
        ::-webkit-scrollbar-thumb { background: #2e2550; border-radius: 2px; }
        @media (max-width: 520px) {
            .container { padding: 20px; }
            .search-box { flex-direction: column; }
            .logo { font-size: 24px; }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">⟡ CLEARANCE</div>
    <div class="subtitle">OSINT SEARCH</div>

    <div class="filters" id="filters">
        <span class="active" data-type="auto">auto</span>
        <span data-type="email">email</span>
        <span data-type="phone">phone</span>
        <span data-type="username">username</span>
        <span data-type="password">password</span>
        <span data-type="hash">hash</span>
        <span data-type="inn">inn</span>
        <span data-type="ogrn">ogrn</span>
        <span data-type="fio">fio</span>
    </div>

    <div class="search-box">
        <input id="q" type="text" placeholder="email / phone / username / inn / ogrn / fio" autofocus>
        <button id="go">go</button>
    </div>

    <div class="result" id="result"><div class="empty">⌕ enter query</div></div>
    <div class="stats"><span id="status">⏎ press enter</span><span id="time"></span></div>
</div>

<script>
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    const q = document.getElementById('q');
    const go = document.getElementById('go');
    const result = document.getElementById('result');
    const status = document.getElementById('status');
    const time = document.getElementById('time');
    let currentType = 'auto';

    document.querySelectorAll('#filters span').forEach(el => {
        el.addEventListener('click', function() {
            document.querySelectorAll('#filters span').forEach(s => s.classList.remove('active'));
            this.classList.add('active');
            currentType = this.dataset.type;
            status.textContent = '⌕ ' + (currentType === 'auto' ? 'autodetect' : currentType);
        });
    });

    function search() {
        const query = q.value.trim();
        if (!query) { result.innerHTML = '<div class="empty">⌕ enter query</div>'; return; }

        status.textContent = '⏳ searching...';
        result.innerHTML = '<div class="loading">⏳ loading...</div>';
        const start = Date.now();

        let url = '/search?query=' + encodeURIComponent(query);
        if (currentType !== 'auto') url += '&type=' + encodeURIComponent(currentType);

        fetch(url)
            .then(r => r.json())
            .then(data => {
                const elapsed = ((Date.now() - start) / 1000).toFixed(2);
                time.textContent = '⏱ ' + elapsed + 's';
                status.textContent = '✓ ' + data.sources?.length + ' sources';

                if (!data.found) {
                    result.innerHTML = '<div class="empty">∅ not found</div>';
                    return;
                }

                let html = '';
                data.sources.forEach(src => {
                    const name = src.source || 'unknown';
                    html += '<div><span class="source">⟡ ' + name + '</span>\n';
                    const d = src.data || {};
                    if (d.results) {
                        if (Array.isArray(d.results)) {
                            d.results.forEach(item => {
                                if (typeof item === 'object') {
                                    Object.entries(item).forEach(([k, v]) => {
                                        if (v) html += '<span class="key">' + k + '</span> ' + v + '\n';
                                    });
                                } else {
                                    html += item + '\n';
                                }
                            });
                        } else if (typeof d.results === 'object') {
                            Object.entries(d.results).forEach(([k, v]) => {
                                if (v) html += '<span class="key">' + k + '</span> ' + v + '\n';
                            });
                        }
                    }
                    if (d.username) html += '<span class="key">username</span> ' + d.username + '\n';
                    if (d.password) html += '<span class="key">password</span> ' + d.password + '\n';
                    if (d.name) html += '<span class="key">name</span> ' + d.name + '\n';
                    if (d.phone) html += '<span class="key">phone</span> ' + d.phone + '\n';
                    if (d.email) html += '<span class="key">email</span> ' + d.email + '\n';
                    html += '</div>\n';
                });
                result.innerHTML = html || '<div class="empty">∅ empty</div>';
            })
            .catch(err => {
                status.textContent = '✗ error';
                result.innerHTML = '<div class="error">✗ ' + err.message + '</div>';
            });
    }

    q.addEventListener('keydown', e => { if (e.key === 'Enter') search(); });
    go.addEventListener('click', search);
</script>
</body>
</html>
'''

# ============ ОПРЕДЕЛЕНИЕ ТИПА ============
def detect_type(query):
    q = str(query).strip()
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', q):
        return "email"
    if re.match(r'^[78][\d]{10}$', re.sub(r'[^\d]', '', q)):
        return "phone"
    if re.match(r'^[a-zA-Z0-9_]{3,}$', q):
        return "username"
    return "text"

# ============ SNUSBASE ============
def snusbase(query, search_type):
    try:
        headers = {"Content-Type": "application/json", "Auth": SNUSBASE_KEY}
        snus_types = {"email": "email", "phone": "phone", "username": "username", "password": "password", "hash": "hash"}
        payload = {
            "terms": [str(query).strip()],
            "types": [snus_types.get(search_type, "email")],
            "wildcard": False
        }
        r = requests.post(SNUSBASE_URL, headers=headers, json=payload, timeout=15)
        if r.status_code == 200:
            return {"source": "Snusbase", "data": r.json()}
        return {"source": "Snusbase", "error": r.status_code}
    except:
        return {"source": "Snusbase", "error": "timeout"}

# ============ OFDATA ============
def ofdata(query, search_type):
    q = str(query).strip()
    headers = {"User-Agent": "Mozilla/5.0"}
    
    if search_type == "inn":
        digits = re.sub(r'[^\d]', '', q)
        if len(digits) == 12:
            url = f"{OFDATA_BASE}/person?key={OFDATA_KEY}&inn={digits}"
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    return {"source": "OFDATA", "data": r.json()}
            except:
                pass
        elif len(digits) == 10:
            url = f"{OFDATA_BASE}/company?key={OFDATA_KEY}&inn={digits}"
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    return {"source": "OFDATA", "data": r.json()}
            except:
                pass
    elif search_type == "ogrn":
        digits = re.sub(r'[^\d]', '', q)
        if len(digits) >= 13:
            url = f"{OFDATA_BASE}/inspections?key={OFDATA_KEY}&ogrn={digits}"
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    return {"source": "OFDATA", "data": r.json()}
            except:
                pass
    elif search_type == "fio" or search_type == "text":
        url = f"{OFDATA_BASE}/search?key={OFDATA_KEY}&by=founder-name&obj=org&query={requests.utils.quote(q)}"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('meta', {}).get('status') == 'ok':
                    records = data.get('data', {}).get('Записи', data.get('data', {}))
                    if records:
                        return {"source": "OFDATA", "data": records}
        except:
            pass
    
    return {"source": "OFDATA", "error": "no_data"}

# ============ ОСНОВНОЙ ЭНДПОИНТ ============
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        query = data.get('query')
        search_type = data.get('type')
    else:
        query = request.args.get('query')
        search_type = request.args.get('type')
    
    if not query:
        return jsonify({"error": "Missing query"}), 400
    
    if not search_type or search_type == 'auto':
        search_type = detect_type(query)
    
    result = {"query": query, "type": search_type, "sources": []}
    
    # Snusbase — работает для email, phone, username, password, hash
    if search_type in ["email", "phone", "username", "password", "hash"]:
        sn = snusbase(query, search_type)
        if sn and sn.get("data"):
            result["sources"].append(sn)
    
    # OFDATA — работает для inn, ogrn, fio
    if search_type in ["inn", "ogrn", "fio", "text"]:
        of = ofdata(query, search_type)
        if of and of.get("data"):
            result["sources"].append(of)
    
    result["found"] = len([s for s in result["sources"] if "data" in s]) > 0
    return jsonify(result)

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
