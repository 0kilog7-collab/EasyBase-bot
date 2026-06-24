from flask import Flask, render_template_string

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Easy API вЂ” Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Inter,Segoe UI,sans-serif;background:#f8fafc;color:#0f172a;padding:40px 20px;line-height:1.6;overflow-x:hidden;position:relative}
        body:before{content:'';position:fixed;inset:-20%;background:radial-gradient(circle at 10% 20%,rgba(0,255,180,.30),transparent 30%),radial-gradient(circle at 90% 10%,rgba(0,153,255,.25),transparent 30%),radial-gradient(circle at 50% 80%,rgba(120,255,220,.25),transparent 35%);filter:blur(90px);animation:aurora 15s ease-in-out infinite alternate;pointer-events:none}
        @keyframes aurora{from{transform:translateX(-5%) scale(1)}to{transform:translateX(5%) scale(1.2)}}
        .container{max-width:1200px;margin:auto;position:relative;z-index:1}
        .logo{font-size:64px;font-weight:900;text-align:center;background:linear-gradient(90deg,#00c9a7,#0099ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-top:20px}
        .sub{text-align:center;color:#64748b;letter-spacing:4px;margin-bottom:50px}
        .section-title{font-size:32px;font-weight:800;margin:35px 0 20px;color:#0f172a;border:none}
        .endpoint{background:rgba(255,255,255,.72);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.9);border-radius:24px;padding:24px;margin-bottom:18px;box-shadow:0 12px 40px rgba(15,23,42,.08);transition:.3s}
        .endpoint:hover{transform:translateY(-5px);box-shadow:0 20px 50px rgba(15,23,42,.12)}
        .endpoint-path{color:#0f172a;font-size:18px;font-weight:800;word-break:break-all;display:inline-block;background:#0f172a;color:#e2e8f0;padding:10px 20px;border-radius:12px;font-family:'Courier New',monospace;font-size:15px;margin-top:8px;width:100%;overflow-x:auto;white-space:pre-wrap}
        .endpoint-desc,.param-desc,.footer,.sub{color:#64748b}
        .endpoint-example{background:#0f172a;color:#e2e8f0;border:none;border-radius:16px;padding:20px;margin-top:12px;font-family:'Courier New',monospace;font-size:14px;overflow-x:auto;white-space:pre-wrap;word-break:break-all}
        .key{color:#38bdf8!important}.str{color:#22c55e!important}.val{color:#cbd5e1!important}
        .badge{padding:8px 14px;border-radius:999px;font-weight:700;font-size:12px;display:inline-block}
        .badge-get{background:#dcfce7;color:#166534;border:none}
        .badge-post{background:#fef3c7;color:#92400e;border:none}
        .badge-auth{background:#dbeafe;color:#1d4ed8;border:none}
        .grid-2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
        .footer{margin-top:50px;text-align:center;padding:30px}
        .endpoint-header{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:8px}
        .top-right{position:fixed;top:20px;right:20px;display:flex;gap:12px;z-index:100}
        .btn-info{padding:10px 22px;border-radius:12px;font-weight:700;font-size:14px;cursor:pointer;border:none;background:rgba(255,255,255,.85);backdrop-filter:blur(12px);color:#0f172a;box-shadow:0 4px 16px rgba(15,23,42,.08);transition:.3s}
        .btn-info:hover{transform:scale(1.04);box-shadow:0 8px 30px rgba(15,23,42,.15)}
        .modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.4);backdrop-filter:blur(6px);z-index:200;justify-content:center;align-items:center}
        .modal.active{display:flex}
        .modal-content{background:#fff;border-radius:24px;padding:40px;max-width:600px;width:90%;max-height:80vh;overflow-y:auto;box-shadow:0 40px 80px rgba(0,0,0,.3)}
        .modal-content h2{font-size:28px;font-weight:800;margin-bottom:20px;color:#0f172a}
        .modal-content p{color:#475569;margin-bottom:12px;font-size:16px;line-height:1.8}
        .modal-content .stat{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid #e2e8f0}
        .modal-content .stat:last-child{border-bottom:none}
        .modal-content .stat-label{color:#64748b}
        .modal-content .stat-value{font-weight:700;color:#0f172a}
        .modal-close{margin-top:24px;padding:12px 28px;background:#0f172a;color:#fff;border:none;border-radius:12px;font-weight:700;cursor:pointer;font-size:14px}
        @media(max-width:700px){.logo{font-size:40px}.grid-2{grid-template-columns:1fr}.endpoint-path{font-size:13px;padding:8px 14px}.endpoint-example{font-size:12px}.top-right{top:12px;right:12px;gap:8px}.btn-info{padding:8px 16px;font-size:12px}.modal-content{padding:24px}}
    </style>
    <script>
        function openModal(t){document.getElementById(t+'Modal').classList.add('active')}
        function closeModal(t){document.getElementById(t+'Modal').classList.remove('active')}
        window.onclick=function(e){if(e.target.classList.contains('modal')){e.target.classList.remove('active')}}
    </script>
</head>
<body>
<div class="top-right">
    <button class="btn-info" onclick="openModal('info')">РРЅС„Рѕ</button>
    <button class="btn-info" onclick="openModal('stats')">РЎС‚Р°С‚РёСЃС‚РёРєР°</button>
</div>

<div class="modal" id="infoModal">
    <div class="modal-content">
        <h2>РћР± API</h2>
        <p><strong>Easy API</strong> вЂ” СѓРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ OSINT-С€Р»СЋР·, РѕР±СЉРµРґРёРЅСЏСЋС‰РёР№ РЅРµСЃРєРѕР»СЊРєРѕ РёСЃС‚РѕС‡РЅРёРєРѕРІ РґР°РЅРЅС‹С… РІ РѕРґРЅРѕРј Р·Р°РїСЂРѕСЃРµ.</p>
        <p>Р’СЃРµ Р·Р°РїСЂРѕСЃС‹ РїСЂРѕС…РѕРґСЏС‚ С‡РµСЂРµР· РµРґРёРЅС‹Р№ СЌРЅРґРїРѕРёРЅС‚ <code style="background:#f1f5f9;padding:2px 8px;border-radius:6px;">/search</code> СЃ РїР°СЂР°РјРµС‚СЂРѕРј <code style="background:#f1f5f9;padding:2px 8px;border-radius:6px;">api_key</code>.</p>
        <p>РџРѕРґРґРµСЂР¶РёРІР°РµРјС‹Рµ С‚РёРїС‹: РЅРѕРјРµСЂ С‚РµР»РµС„РѕРЅР°, email, РїР°СЂРѕР»СЊ, РРќРќ, VK, IP, Р¤РРћ, С‚РµРєСЃС‚.</p>
        <p style="margin-top:16px;color:#64748b;font-size:14px;">Р”Р»СЏ РґРѕСЃС‚СѓРїР° С‚СЂРµР±СѓРµС‚СЃСЏ API-РєР»СЋС‡. РџРѕР»СѓС‡РёС‚СЊ РјРѕР¶РЅРѕ Сѓ РІР»Р°РґРµР»СЊС†Р°.</p>
        <button class="modal-close" onclick="closeModal('info')">Р—Р°РєСЂС‹С‚СЊ</button>
    </div>
</div>

<div class="modal" id="statsModal">
    <div class="modal-content">
        <h2>РЎС‚Р°С‚РёСЃС‚РёРєР°</h2>
        <div class="stat"><span class="stat-label">Р—Р°РїРёСЃРµР№ РІ Р±Р°Р·Рµ</span><span class="stat-value">> 40 000 000 000</span></div>
        <div class="stat"><span class="stat-label">РСЃС‚РѕС‡РЅРёРєРѕРІ РґР°РЅРЅС‹С…</span><span class="stat-value">6</span></div>
        <div class="stat"><span class="stat-label">РћР±С‰РёР№ РѕР±СЉС‘Рј</span><span class="stat-value">~500 РўР‘</span></div>
        <div class="stat"><span class="stat-label">РўРёРїРѕРІ Р·Р°РїСЂРѕСЃРѕРІ</span><span class="stat-value">8</span></div>
        <div class="stat"><span class="stat-label">Р”РѕСЃС‚СѓРїРЅРѕСЃС‚СЊ</span><span class="stat-value" style="color:#22c55e;">24/7</span></div>
        <button class="modal-close" onclick="closeModal('stats')">Р—Р°РєСЂС‹С‚СЊ</button>
    </div>
</div>

<div class="container">
    <div class="logo">Easy API</div>
    <div class="sub">Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ</div>

    <div class="section-title">РћР±С‰Р°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ</div>
    <div class="endpoint">
        <div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:6px;">
            <span><span class="badge badge-get">GET</span> <span class="badge badge-post">POST</span></span>
            <span><span class="badge badge-auth">РўСЂРµР±СѓРµС‚СЃСЏ API-РєР»СЋС‡</span></span>
        </div>
        <div><span style="color:#64748b;">Р‘Р°Р·РѕРІС‹Р№ URL:</span> <span style="color:#0f172a;font-weight:700;">https://easyapi-3r7x.onrender.com</span></div>
        <div style="margin-top:6px;color:#64748b;font-size:13px;">Р’СЃРµ Р·Р°РїСЂРѕСЃС‹ С‚СЂРµР±СѓСЋС‚ РїР°СЂР°РјРµС‚СЂ <span style="color:#1d4ed8;">api_key</span>.</div>
    </div>

    <div class="section-title">РџРѕРёСЃРє <small>/search</small></div>

    <div class="endpoint">
        <div class="endpoint-header"><span class="badge badge-get">GET</span><span class="endpoint-path">/search?phone={РЅРѕРјРµСЂ}&amp;api_key={РєР»СЋС‡}</span></div>
        <div class="endpoint-desc">phone вЂ” РќРѕРјРµСЂ С‚РµР»РµС„РѕРЅР°</div>
        <div class="endpoint-example"><span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?phone=<span class="str">79277231370</span>&amp;api_key=<span class="str">Р’РђРЁ_РљР›Р®Р§</span></span>"</div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header"><span class="badge badge-get">GET</span><span class="endpoint-path">/search?email={РїРѕС‡С‚Р°}&amp;api_key={РєР»СЋС‡}</span></div>
        <div class="endpoint-desc">email вЂ” Р­Р»РµРєС‚СЂРѕРЅРЅР°СЏ РїРѕС‡С‚Р°</div>
        <div class="endpoint-example"><span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?email=<span class="str">user@gmail.com</span>&amp;api_key=<span class="str">Р’РђРЁ_РљР›Р®Р§</span></span>"</div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header"><span class="badge badge-get">GET</span><span class="endpoint-path">/search?pass={РїР°СЂРѕР»СЊ}&amp;api_key={РєР»СЋС‡}</span></div>
        <div class="endpoint-desc">pass вЂ” РџР°СЂРѕР»СЊ</div>
        <div class="endpoint-example"><span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?pass=<span class="str">qwerty123</span>&amp;api_key=<span class="str">Р’РђРЁ_РљР›Р®Р§</span></span>"</div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header"><span class="badge badge-get">GET</span><span class="endpoint-path">/search?inn={РёРЅРЅ}&amp;api_key={РєР»СЋС‡}</span></div>
        <div class="endpoint-desc">inn вЂ” РРќРќ (10 С†РёС„СЂ вЂ” Р®СЂР»РёС†Р°/Р‘Р°РЅРєРё; 12 С†РёС„СЂ вЂ” Р¤РёР·Р»РёС†Р°/РРџ)</div>
        <div class="endpoint-example"><span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?inn=<span class="str">7707083893</span>&amp;api_key=<span class="str">Р’РђРЁ_РљР›Р®Р§</span></span>"</div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header"><span class="badge badge-get">GET</span><span class="endpoint-path">/search?vkid={id/СЃСЃС‹Р»РєР°}&amp;api_key={РєР»СЋС‡}</span></div>
        <div class="endpoint-desc">vkid вЂ” РЎСЃС‹Р»РєР° РёР»Рё ID Р’РљРѕРЅС‚Р°РєС‚Рµ</div>
        <div class="endpoint-example"><span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?vkid=<span class="str">1</span>&amp;api_key=<span class="str">Р’РђРЁ_РљР›Р®Р§</span></span>"</div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header"><span class="badge badge-get">GET</span><span class="endpoint-path">/search?ip={ip}&amp;api_key={РєР»СЋС‡}</span></div>
        <div class="endpoint-desc">ip вЂ” IP-Р°РґСЂРµСЃ</div>
        <div class="endpoint-example"><span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?ip=<span class="str">8.8.8.8</span>&amp;api_key=<span class="str">Р’РђРЁ_РљР›Р®Р§</span></span>"</div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header"><span class="badge badge-get">GET</span><span class="endpoint-path">/search?fio={С„РёРѕ}&amp;api_key={РєР»СЋС‡}</span></div>
        <div class="endpoint-desc">fio вЂ” Р¤РРћ</div>
        <div class="endpoint-example"><span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?fio=<span class="str">РРІР°РЅРѕРІ РРІР°РЅ РРІР°РЅРѕРІРёС‡</span>&amp;api_key=<span class="str">Р’РђРЁ_РљР›Р®Р§</span></span>"</div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header"><span class="badge badge-get">GET</span><span class="endpoint-path">/search?text={Р·Р°РїСЂРѕСЃ}&amp;api_key={РєР»СЋС‡}</span></div>
        <div class="endpoint-desc">text вЂ” Р›СЋР±РѕР№ С‚РµРєСЃС‚РѕРІС‹Р№ Р·Р°РїСЂРѕСЃ (Р¤РРћ, РЅР°Р·РІР°РЅРёРµ РєРѕРјРїР°РЅРёРё вЂ” РѕРїСЂР°С€РёРІР°РµС‚ РіР»РѕР±Р°Р»СЊРЅС‹Р№ РїРѕРёСЃРє)</div>
        <div class="endpoint-example"><span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?text=<span class="str">РРІР°РЅРѕРІ РРІР°РЅ</span>&amp;api_key=<span class="str">Р’РђРЁ_РљР›Р®Р§</span></span>"</div>
    </div>

    <div class="section-title">РџСЂРёРјРµСЂ РѕС‚РІРµС‚Р°</div>
    <div class="endpoint">
        <div class="endpoint-example" style="color:#e2e8f0;">
            {<span class="key">"query"</span>: <span class="str">"user@gmail.com"</span>, <span class="key">"type"</span>: <span class="str">"email"</span>, <span class="key">"found"</span>: <span style="color:#22c55e;">true</span>, <span class="key">"sources"</span>: [{<span class="key">"source"</span>: <span class="str">"DepSearch"</span>, <span class="key">"data"</span>: {<span class="key">"results"</span>: [...]}}]}
        </div>
    </div>

    <div class="section-title">РљРѕРґС‹ РѕС€РёР±РѕРє</div>
    <div class="grid-2">
        <div class="endpoint"><div style="color:#ef4444;font-weight:700;">401 РќРµ Р°РІС‚РѕСЂРёР·РѕРІР°РЅ</div><div style="color:#64748b;font-size:13px;">РќРµРІРµСЂРЅС‹Р№ РёР»Рё РѕС‚СЃСѓС‚СЃС‚РІСѓСЋС‰РёР№ API-РєР»СЋС‡</div></div>
        <div class="endpoint"><div style="color:#f59e0b;font-weight:700;">400 РќРµРІРµСЂРЅС‹Р№ Р·Р°РїСЂРѕСЃ</div><div style="color:#64748b;font-size:13px;">РћС‚СЃСѓС‚СЃС‚РІСѓРµС‚ РїР°СЂР°РјРµС‚СЂ Р·Р°РїСЂРѕСЃР°</div></div>
        <div class="endpoint" style="grid-column:span 2;"><div style="color:#22c55e;font-weight:700;">200 OK</div><div style="color:#64748b;font-size:13px;">РЈСЃРїРµС€РЅС‹Р№ Р·Р°РїСЂРѕСЃ (РґР°Р¶Рµ РµСЃР»Рё РґР°РЅРЅС‹Рµ РЅРµ РЅР°Р№РґРµРЅС‹)</div></div>
    </div>

    <div class="footer"><span>Easy API Gateway</span> В· <span>@y3Huk_iphone</span></div>
</div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
