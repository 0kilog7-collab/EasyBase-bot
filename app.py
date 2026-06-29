<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Router — Зеркала ботов</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: #0a0a0f;
            color: #e0e0e0;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            max-width: 700px;
            width: 100%;
            background: linear-gradient(145deg, #12121a, #0d0d14);
            border-radius: 28px;
            padding: 40px 32px;
            border: 1px solid #2a2a3a;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
            position: relative;
            overflow: hidden;
        }
        .container::before {
            content: '';
            position: absolute;
            top: -80px;
            right: -80px;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(100, 60, 200, 0.08) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }
        .logo {
            font-size: 28px;
            font-weight: 700;
            letter-spacing: 2px;
            background: linear-gradient(135deg, #b084f5, #7c4ddc, #4f2e95);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .sub {
            color: #6b5f8a;
            font-size: 13px;
            letter-spacing: 1px;
            margin-bottom: 32px;
            border-left: 2px solid #3d2d6e;
            padding-left: 16px;
        }
        .mirror-list {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .mirror-item {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid #2a2a3a;
            border-radius: 16px;
            padding: 18px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.25s ease;
            backdrop-filter: blur(4px);
        }
        .mirror-item:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: #4a3a7a;
            transform: translateX(6px);
        }
        .mirror-info {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .mirror-name {
            font-weight: 600;
            font-size: 15px;
            color: #d4c8f0;
        }
        .mirror-status {
            font-size: 12px;
            color: #6b5f8a;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #22c55e;
            animation: pulse-dot 2s ease-in-out infinite;
        }
        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }
        .mirror-link {
            background: linear-gradient(135deg, #3d2d6e, #2a1f4a);
            color: #d4c8f0;
            text-decoration: none;
            padding: 8px 20px;
            border-radius: 30px;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s ease;
            border: 1px solid #4a3a7a;
            white-space: nowrap;
        }
        .mirror-link:hover {
            background: linear-gradient(135deg, #5c3d9e, #3d2d6e);
            border-color: #7c4ddc;
            box-shadow: 0 0 20px rgba(124, 77, 220, 0.25);
            transform: scale(1.03);
        }
        .footer {
            margin-top: 36px;
            padding-top: 20px;
            border-top: 1px solid #1e1e2e;
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #4a3f6a;
        }
        .status-text {
            color: #22c55e;
        }
        @media (max-width: 600px) {
            .container { padding: 28px 18px; }
            .mirror-item { flex-direction: column; align-items: stretch; gap: 12px; }
            .mirror-link { text-align: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">◈ ROUTER</div>
        <div class="sub">актуальные зеркала бота</div>

        <div class="mirror-list">
            <div class="mirror-item">
                <div class="mirror-info">
                    <div class="mirror-name">Основное зеркало</div>
                    <div class="mirror-status"><span class="status-dot"></span> работает</div>
                </div>
                <a href="https://t.me/probivkaweqst_bot" target="_blank" class="mirror-link">@probivkaweqst_bot</a>
            </div>
            <div class="mirror-item">
                <div class="mirror-info">
                    <div class="mirror-name">Резервное зеркало</div>
                    <div class="mirror-status"><span class="status-dot"></span> работает</div>
                </div>
                <a href="https://t.me/Doduhekrkfjddj_bot" target="_blank" class="mirror-link">@Doduhekrkfjddj_bot</a>
            </div>
        </div>

        <div class="footer">
            <span>Router OSINT</span>
            <span class="status-text">● все системы работают</span>
        </div>
    </div>
</body>
</html>
