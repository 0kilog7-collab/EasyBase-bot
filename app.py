<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Easy API — Документация</title>
    
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
font-family:Inter,Segoe UI,sans-serif;
background:#f8fafc;
color:#0f172a;
padding:40px 20px;
line-height:1.6;
overflow-x:hidden;
position:relative;
}
body:before{
content:'';
position:fixed;
inset:-20%;
background:
radial-gradient(circle at 10% 20%,rgba(0,255,180,.30),transparent 30%),
radial-gradient(circle at 90% 10%,rgba(0,153,255,.25),transparent 30%),
radial-gradient(circle at 50% 80%,rgba(120,255,220,.25),transparent 35%);
filter:blur(90px);
animation:aurora 15s ease-in-out infinite alternate;
pointer-events:none;
}
@keyframes aurora{
from{transform:translateX(-5%) scale(1)}
to{transform:translateX(5%) scale(1.2)}
}
.container{max-width:1200px;margin:auto;position:relative;z-index:1}
.logo{
font-size:64px;
font-weight:900;
text-align:center;
background:linear-gradient(90deg,#00c9a7,#0099ff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-top:20px;
}
.sub{
text-align:center;
color:#64748b;
letter-spacing:4px;
margin-bottom:50px;
}
.section-title{
font-size:32px;
font-weight:800;
margin:35px 0 20px;
color:#0f172a;
border:none;
}
.endpoint{
background:rgba(255,255,255,.72);
backdrop-filter:blur(20px);
border:1px solid rgba(255,255,255,.9);
border-radius:24px;
padding:24px;
margin-bottom:18px;
box-shadow:0 12px 40px rgba(15,23,42,.08);
transition:.3s;
}
.endpoint:hover{
transform:translateY(-5px);
box-shadow:0 20px 50px rgba(15,23,42,.12);
}
.endpoint-path{
color:#0f172a;
font-size:18px;
font-weight:800;
word-break:break-all;
display:inline-block;
background:#0f172a;
color:#e2e8f0;
padding:10px 20px;
border-radius:12px;
font-family:'Courier New',monospace;
font-size:15px;
margin-top:8px;
width:100%;
overflow-x:auto;
white-space:pre-wrap;
}
.endpoint-desc,.param-desc,.footer,.sub{color:#64748b}
.endpoint-example{
background:#0f172a;
color:#e2e8f0;
border:none;
border-radius:16px;
padding:20px;
margin-top:12px;
font-family:'Courier New',monospace;
font-size:14px;
overflow-x:auto;
white-space:pre-wrap;
word-break:break-all;
}
.key{color:#38bdf8!important}
.str{color:#22c55e!important}
.val{color:#cbd5e1!important}
.badge{
padding:8px 14px;
border-radius:999px;
font-weight:700;
font-size:12px;
display:inline-block;
}
.badge-get{
background:#dcfce7;
color:#166534;
border:none;
}
.badge-post{
background:#fef3c7;
color:#92400e;
border:none;
}
.badge-auth{
background:#dbeafe;
color:#1d4ed8;
border:none;
}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.footer{
margin-top:50px;
text-align:center;
padding:30px;
}
.endpoint-header{
display:flex;
align-items:center;
gap:14px;
flex-wrap:wrap;
margin-bottom:8px;
}
.top-right{
position:fixed;
top:20px;
right:20px;
display:flex;
gap:12px;
z-index:100;
}
.btn-info{
padding:10px 22px;
border-radius:12px;
font-weight:700;
font-size:14px;
cursor:pointer;
border:none;
background:rgba(255,255,255,.85);
backdrop-filter:blur(12px);
color:#0f172a;
box-shadow:0 4px 16px rgba(15,23,42,.08);
transition:.3s;
}
.btn-info:hover{
transform:scale(1.04);
box-shadow:0 8px 30px rgba(15,23,42,.15);
}
.modal{
display:none;
position:fixed;
inset:0;
background:rgba(0,0,0,.4);
backdrop-filter:blur(6px);
z-index:200;
justify-content:center;
align-items:center;
}
.modal.active{display:flex}
.modal-content{
background:#fff;
border-radius:24px;
padding:40px;
max-width:600px;
width:90%;
max-height:80vh;
overflow-y:auto;
box-shadow:0 40px 80px rgba(0,0,0,.3);
}
.modal-content h2{font-size:28px;font-weight:800;margin-bottom:20px;color:#0f172a}
.modal-content p{color:#475569;margin-bottom:12px;font-size:16px;line-height:1.8}
.modal-content .stat{
display:flex;
justify-content:space-between;
padding:12px 0;
border-bottom:1px solid #e2e8f0;
}
.modal-content .stat:last-child{border-bottom:none}
.modal-content .stat-label{color:#64748b}
.modal-content .stat-value{font-weight:700;color:#0f172a}
.modal-close{
margin-top:24px;
padding:12px 28px;
background:#0f172a;
color:#fff;
border:none;
border-radius:12px;
font-weight:700;
cursor:pointer;
font-size:14px;
}
@media(max-width:700px){
.logo{font-size:40px}
.grid-2{grid-template-columns:1fr}
.endpoint-path{font-size:13px;padding:8px 14px}
.endpoint-example{font-size:12px}
.top-right{top:12px;right:12px;gap:8px}
.btn-info{padding:8px 16px;font-size:12px}
.modal-content{padding:24px}
}
</style>

</head>
<body>

<div class="top-right">
    <button class="btn-info" onclick="openModal('info')">Info</button>
    <button class="btn-info" onclick="openModal('stats')">Stats</button>
</div>

<div class="modal" id="infoModal">
    <div class="modal-content">
        <h2>About API</h2>
        <p><strong>Easy API</strong> is a universal OSINT gateway that combines multiple data sources in one request.</p>
        <p>All requests go through the single endpoint <code style="background:#f1f5f9;padding:2px 8px;border-radius:6px;">/search</code> with the <code style="background:#f1f5f9;padding:2px 8px;border-radius:6px;">api_key</code> parameter.</p>
        <p>Supported: phone number, email, password, INN, VK, TikTok, SNILS, IP, address, car, nickname, text.</p>
        <p style="margin-top:16px;color:#64748b;font-size:14px;">API key required for access. Contact the owner to obtain it.</p>
        <button class="modal-close" onclick="closeModal('info')">Close</button>
    </div>
</div>

<div class="modal" id="statsModal">
    <div class="modal-content">
        <h2>Statistics</h2>
        <div class="stat">
            <span class="stat-label">Records in database</span>
            <span class="stat-value">> 40 000 000 000</span>
        </div>
        <div class="stat">
            <span class="stat-label">Data sources</span>
            <span class="stat-value">6</span>
        </div>
        <div class="stat">
            <span class="stat-label">Total volume</span>
            <span class="stat-value">~500 TB</span>
        </div>
        <div class="stat">
            <span class="stat-label">Query types</span>
            <span class="stat-value">12</span>
        </div>
        <div class="stat">
            <span class="stat-label">Availability</span>
            <span class="stat-value" style="color:#22c55e;">24/7</span>
        </div>
        <button class="modal-close" onclick="closeModal('stats')">Close</button>
    </div>
</div>

<div class="container">

    <div class="logo">Easy API</div>
    <div class="sub">Documentation</div>

    <div class="section-title">General Information</div>
    <div class="endpoint">
        <div style="display:flex; gap:14px; flex-wrap:wrap; margin-bottom:6px;">
            <span><span class="badge badge-get">GET</span> <span class="badge badge-post">POST</span></span>
            <span><span class="badge badge-auth">API Key Required</span></span>
        </div>
        <div><span style="color:#64748b;">Base URL:</span> <span style="color:#0f172a; font-weight:700;">https://easyapi-3r7x.onrender.com</span></div>
        <div style="margin-top:6px; color:#64748b; font-size:13px;">
            All requests require <span style="color:#1d4ed8;">api_key</span> parameter.
        </div>
    </div>

    <div class="section-title">Search <small>/search</small></div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?phone={number}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">Phone number — automatically cleaned, queries DepSearch</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?phone=<span class="str">79277231370</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?email={email}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">Email — queries DepSearch + Snusbase</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?email=<span class="str">user@gmail.com</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?pass={password}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">Password — queries DepSearch + Snusbase (password type)</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?pass=<span class="str">qwerty123</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?inn={inn}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">INN — 10 digits (Legal entities/Banks via Ofdata); 12 digits (Individuals/IP via Ofdata); both also query DepSearch</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?inn=<span class="str">7707083893</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?vk={id/link}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">VK — ID or link, automatically converts to vkid format</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?vk=<span class="str">1</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?tiktok={nick/link}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">TikTok — nickname or link, automatically converts to tt format</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?tiktok=<span class="str">tt:username</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?snils={snils}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">SNILS — converts to snils format</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?snils=<span class="str">12345678901</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?ip={ip}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">IP address — converts to ip format</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?ip=<span class="str">8.8.8.8</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?address={address}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">Address — residence or registration address</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?address=<span class="str">addr:Moscow, Tverskaya, 10</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?auto={grz/vin}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">Auto — VIN code or license plate</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?auto=<span class="str">A123BC77</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?nick={nick}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">Nickname / Username</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?nick=<span class="str">nick:username</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="endpoint">
        <div class="endpoint-header">
            <span class="badge badge-get">GET</span>
            <span class="endpoint-path">/search?text={query}&amp;api_key={key}</span>
        </div>
        <div class="endpoint-desc">Any text query — FIO, company name — queries Ofdata + DepSearch</div>
        <div class="endpoint-example">
            <span class="key">curl</span> "<span class="val">https://easyapi-3r7x.onrender.com/search?text=<span class="str">Ivanov Ivan</span>&amp;api_key=<span class="str">YOUR_API_KEY</span></span>"
        </div>
    </div>

    <div class="section-title">Example Response</div>
    <div class="endpoint">
        <div class="endpoint-example" style="color:#e2e8f0;">
            {
            <span class="key">"query"</span>: <span class="str">"user@gmail.com"</span>,
            <span class="key">"type"</span>: <span class="str">"email"</span>,
            <span class="key">"found"</span>: <span style="color:#22c55e;">true</span>,
            <span class="key">"sources"</span>: [
            {
            <span class="key">"source"</span>: <span class="str">"DepSearch"</span>,
            <span class="key">"data"</span>: { <span class="key">"results"</span>: [...] }
            },
            {
            <span class="key">"source"</span>: <span class="str">"Snusbase"</span>,
            <span class="key">"data"</span>: { <span class="key">"results"</span>: [...] }
            }
            ]
            }
        </div>
    </div>

    <div class="section-title">Error Codes</div>
    <div class="grid-2">
        <div class="endpoint">
            <div style="color:#ef4444;font-weight:700;">401 Unauthorized</div>
            <div style="color:#64748b;font-size:13px;">Invalid or missing API key</div>
        </div>
        <div class="endpoint">
            <div style="color:#f59e0b;font-weight:700;">400 Bad Request</div>
            <div style="color:#64748b;font-size:13px;">Missing query parameter</div>
        </div>
        <div class="endpoint" style="grid-column: span 2;">
            <div style="color:#22c55e;font-weight:700;">200 OK</div>
            <div style="color:#64748b;font-size:13px;">Successful request (even if no data found)</div>
        </div>
    </div>

    <div class="footer">
        <span>Easy API Gateway</span> · <span>@y3Huk_iphone</span>
    </div>

</div>

<script>
function openModal(type){
    document.getElementById(type + 'Modal').classList.add('active');
}
function closeModal(type){
    document.getElementById(type + 'Modal').classList.remove('active');
}
window.onclick = function(e){
    if(e.target.classList.contains('modal')){
        e.target.classList.remove('active');
    }
}
</script>

</body>
</html>
