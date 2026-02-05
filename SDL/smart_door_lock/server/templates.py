# Web UI Templates
# HTML templates for the Smart Door Lock system

HOME_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Smart Door Lock Server</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background: #1a1a2e;
            color: #eee;
        }
        h1 { color: #00d9ff; }
        h2 { color: #00d9ff; margin-top: 30px; }
        .status { color: #00ff88; font-weight: bold; font-size: 1.2em; }
        a { color: #00d9ff; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat-box {
            background: #16213e;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            flex: 1;
        }
        .stat-number { font-size: 2em; color: #00d9ff; }
        .app-btn {
            display: inline-block;
            background: linear-gradient(135deg, #00d9ff, #00ff88);
            color: #1a1a2e;
            padding: 15px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            font-size: 18px;
            margin-top: 20px;
        }
        .app-btn:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <h1>🔐 Smart Door Lock Server</h1>
    <p class="status">✓ Server is running</p>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-number">{{ face_count }}</div>
            <div>Registered Faces</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{{ log_count }}</div>
            <div>Access Logs</div>
        </div>
    </div>
    
    <a href="/app" class="app-btn">🚀 Open Face Recognition App</a>
    
    <h2>Quick Links</h2>
    <p>
        <a href="/app#register">📝 Register Face</a> | 
        <a href="/app#test">🔍 Test Recognition</a> | 
        <a href="/app#logs">📋 Access Logs</a>
    </p>
</body>
</html>
'''

REGISTER_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Register Face</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #1a1a2e; color: #eee; padding: 20px; }
        h1 { color: #00d9ff; text-align: center; }
        .container { max-width: 600px; margin: 0 auto; background: #16213e; padding: 30px; border-radius: 12px; }
        input[type="text"] { width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #0f3460; border-radius: 8px; background: #0f3460; color: #fff; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: linear-gradient(135deg, #00d9ff, #00ff88); color: #1a1a2e; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #00d9ff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Register Face</h1>
        <p style="text-align:center">Use the <a href="/app" style="color:#00d9ff">Full App</a> for webcam support</p>
        <input type="text" id="name" placeholder="Enter person's name">
        <input type="file" id="image" accept="image/*" style="color:#aaa;margin:15px 0">
        <button onclick="registerFace()">➕ Register Face</button>
        <div id="result" style="margin-top:20px;padding:15px;border-radius:8px;text-align:center"></div>
    </div>
    <a href="/" class="back-link">← Back to Dashboard</a>
    <script>
        async function registerFace() {
            const name = document.getElementById('name').value.trim();
            const file = document.getElementById('image').files[0];
            const result = document.getElementById('result');
            if (!name || !file) { result.innerHTML = '⚠️ Enter name and select image'; result.style.background = '#ff006633'; return; }
            const reader = new FileReader();
            reader.onload = async e => {
                const base64 = e.target.result.split(',')[1];
                const res = await fetch('/register', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({name, image: base64}) });
                const data = await res.json();
                result.style.background = data.success ? '#00ff8833' : '#ff006633';
                result.innerHTML = data.success ? '✓ ' + data.message : '✗ ' + data.error;
            };
            reader.readAsDataURL(file);
        }
    </script>
</body>
</html>
'''

# Main integrated application
APP_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Smart Door Lock - Face Recognition</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            color: #eee;
        }
        
        /* Header */
        header {
            background: rgba(0,0,0,0.3);
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(10px);
        }
        
        .logo { 
            font-size: 1.5em; 
            font-weight: bold;
            background: linear-gradient(135deg, #00d9ff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .status-dot {
            width: 10px; height: 10px;
            background: #00ff88;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Navigation Tabs */
        .tabs {
            display: flex;
            background: rgba(0,0,0,0.2);
            padding: 0 20px;
            overflow-x: auto;
        }
        
        .tab {
            padding: 15px 25px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
            white-space: nowrap;
        }
        
        .tab:hover { background: rgba(255,255,255,0.05); }
        .tab.active { 
            border-bottom-color: #00d9ff;
            background: rgba(0,217,255,0.1);
        }
        
        .tab-icon { margin-right: 8px; }
        
        /* Main Content */
        main {
            max-width: 1000px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        .panel { display: none; animation: fadeIn 0.3s; }
        .panel.active { display: block; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Cards */
        .card {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .card h2 {
            color: #00d9ff;
            margin-bottom: 20px;
            font-size: 1.3em;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(0,217,255,0.2), rgba(0,255,136,0.1));
            border-radius: 12px;
            padding: 25px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(135deg, #00d9ff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label { color: #aaa; margin-top: 5px; }
        
        /* Video Container */
        .video-container {
            position: relative;
            background: #000;
            border-radius: 12px;
            overflow: hidden;
            margin: 20px 0;
        }
        
        #webcam, #testWebcam {
            width: 100%;
            max-height: 400px;
            display: block;
            transform: scaleX(-1);
        }
        
        .video-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0,0,0,0.7);
            font-size: 1.2em;
        }
        
        .video-overlay.hidden { display: none; }
        
        /* Result Display */
        .result-box {
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            font-size: 1.3em;
            margin: 20px 0;
            transition: all 0.3s;
        }
        
        .result-box.authorized {
            background: linear-gradient(135deg, rgba(0,255,136,0.3), rgba(0,255,136,0.1));
            border: 2px solid #00ff88;
            color: #00ff88;
        }
        
        .result-box.denied {
            background: linear-gradient(135deg, rgba(255,71,87,0.3), rgba(255,71,87,0.1));
            border: 2px solid #ff4757;
            color: #ff4757;
        }
        
        .result-box.neutral {
            background: rgba(255,255,255,0.05);
            border: 2px solid rgba(255,255,255,0.2);
            color: #aaa;
        }
        
        .confidence-bar {
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            margin-top: 15px;
            overflow: hidden;
        }
        
        .confidence-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s;
        }
        
        /* Forms */
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            background: rgba(0,0,0,0.3);
            color: #fff;
            font-size: 16px;
            margin-bottom: 15px;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #00d9ff;
        }
        
        /* Buttons */
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #00d9ff, #00ff88);
            color: #1a1a2e;
        }
        
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(0,217,255,0.4); }
        
        .btn-danger {
            background: #ff4757;
            color: white;
        }
        
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: #fff;
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }
        
        .btn-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        /* Face List */
        .face-list { list-style: none; }
        
        .face-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            margin-bottom: 10px;
        }
        
        .face-name { font-weight: bold; font-size: 1.1em; }
        .face-date { color: #888; font-size: 0.9em; }
        
        /* Logs Table */
        .logs-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .logs-table th, .logs-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .logs-table th {
            background: rgba(0,0,0,0.3);
            color: #00d9ff;
        }
        
        .log-granted { color: #00ff88; }
        .log-denied { color: #ff4757; }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .empty-state-icon { font-size: 3em; margin-bottom: 15px; }
        
        /* Toast Notifications */
        .toast {
            position: fixed;
            bottom: 30px;
            right: 30px;
            padding: 15px 25px;
            border-radius: 10px;
            background: #16213e;
            color: #fff;
            box-shadow: 0 5px 30px rgba(0,0,0,0.5);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s;
            z-index: 1000;
        }
        
        .toast.show { transform: translateY(0); opacity: 1; }
        .toast.success { border-left: 4px solid #00ff88; }
        .toast.error { border-left: 4px solid #ff4757; }
        
        /* Admin Login Modal */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
        }
        .modal-overlay.show { opacity: 1; visibility: visible; }
        .modal {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-radius: 16px;
            padding: 30px;
            width: 90%;
            max-width: 400px;
            border: 1px solid rgba(255,255,255,0.1);
            transform: scale(0.9);
            transition: transform 0.3s;
        }
        .modal-overlay.show .modal { transform: scale(1); }
        .modal h3 { color: #00d9ff; margin-bottom: 20px; text-align: center; }
        .modal input {
            width: 100%;
            padding: 12px 15px;
            margin-bottom: 15px;
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            background: rgba(0,0,0,0.3);
            color: #fff;
            font-size: 16px;
        }
        .modal input:focus { outline: none; border-color: #00d9ff; }
        .modal-error { color: #ff4757; text-align: center; margin-bottom: 15px; display: none; }
        .admin-badge {
            background: linear-gradient(135deg, #00d9ff, #00ff88);
            color: #1a1a2e;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            cursor: pointer;
        }
        .admin-badge:hover { opacity: 0.9; }
        .login-btn {
            background: rgba(255,255,255,0.1);
            color: #00d9ff;
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid #00d9ff;
            cursor: pointer;
            font-size: 0.9em;
        }
        .login-btn:hover { background: rgba(0,217,255,0.1); }
        .admin-lock { color: #888; text-align: center; padding: 40px; }
        .admin-lock-icon { font-size: 3em; margin-bottom: 15px; }
        
        /* Responsive */
        @media (max-width: 600px) {
            .tabs { padding: 0; }
            .tab { padding: 12px 15px; font-size: 0.9em; }
            .tab-text { display: none; }
            .stat-number { font-size: 2em; }
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">🔐 Smart Door Lock</div>
        <div style="display:flex;align-items:center;gap:15px">
            <span><span class="status-dot"></span>Server Online</span>
            <span id="adminStatus"></span>
        </div>
    </header>
    
    <!-- Admin Login Modal -->
    <div id="loginModal" class="modal-overlay">
        <div class="modal">
            <h3>🔒 Admin Login</h3>
            <p style="text-align:center;color:#888;margin-bottom:20px;">Enter admin credentials to access this feature</p>
            <div id="loginError" class="modal-error">Invalid credentials</div>
            <input type="text" id="adminUser" placeholder="Username">
            <input type="password" id="adminPass" placeholder="Password">
            <button class="btn btn-primary" style="width:100%" onclick="doLogin()">Login</button>
            <button class="btn btn-secondary" style="width:100%;margin-top:10px" onclick="hideLoginModal()">Cancel</button>
        </div>
    </div>
    
    <nav class="tabs">
        <div class="tab active" data-tab="dashboard">
            <span class="tab-icon">📊</span><span class="tab-text">Dashboard</span>
        </div>
        <div class="tab" data-tab="register">
            <span class="tab-icon">📝</span><span class="tab-text">Register</span>
        </div>
        <div class="tab" data-tab="test">
            <span class="tab-icon">🔍</span><span class="tab-text">Test</span>
        </div>
        <div class="tab" data-tab="manage">
            <span class="tab-icon">👥</span><span class="tab-text">Manage</span>
        </div>
        <div class="tab" data-tab="logs">
            <span class="tab-icon">📋</span><span class="tab-text">Logs</span>
        </div>
    </nav>
    
    <main>
        <!-- Dashboard Panel -->
        <div id="dashboard" class="panel active">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="faceCount">0</div>
                    <div class="stat-label">Registered Faces</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="logCount">0</div>
                    <div class="stat-label">Access Logs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="todayCount">0</div>
                    <div class="stat-label">Today's Attempts</div>
                </div>
            </div>
            
            <div class="card">
                <h2>Quick Actions</h2>
                <div class="btn-group">
                    <button class="btn btn-primary" onclick="switchTab('register')">📝 Register Face</button>
                    <button class="btn btn-primary" onclick="switchTab('test')">🔍 Test Recognition</button>
                </div>
            </div>
            
            <div class="card">
                <h2>Recent Activity</h2>
                <div id="recentLogs"></div>
            </div>
        </div>
        
        <!-- Register Panel -->
        <div id="register" class="panel">
            <div class="card">
                <h2>Register New Face</h2>
                
                <input type="text" id="personName" placeholder="Enter person's name">
                
                <div class="video-container">
                    <video id="webcam" autoplay playsinline></video>
                    <div id="webcamOverlay" class="video-overlay">
                        <span>📷 Click "Start Camera" to begin</span>
                    </div>
                </div>
                
                <canvas id="captureCanvas" style="display:none"></canvas>
                
                <div class="btn-group">
                    <button id="startCamBtn" class="btn btn-secondary" onclick="startCamera('webcam')">📷 Start Camera</button>
                    <button id="captureBtn" class="btn btn-primary" onclick="captureAndRegister()" disabled>📸 Capture & Register</button>
                </div>
                
                <div style="margin-top: 20px; text-align: center; color: #888;">
                    — or upload an image —
                </div>
                
                <input type="file" id="uploadImage" accept="image/*" style="display:none" onchange="handleUpload(event)">
                <button class="btn btn-secondary" onclick="document.getElementById('uploadImage').click()" style="width:100%;margin-top:10px">
                    📁 Upload Image
                </button>
                
                <div id="registerResult" class="result-box neutral" style="display:none"></div>
            </div>
        </div>
        
        <!-- Test Panel -->
        <div id="test" class="panel">
            <div class="card">
                <h2>Test Face Recognition</h2>
                
                <div class="video-container">
                    <video id="testWebcam" autoplay playsinline></video>
                    <div id="testOverlay" class="video-overlay">
                        <span>📷 Click "Start Camera" to begin</span>
                    </div>
                </div>
                
                <canvas id="testCanvas" style="display:none"></canvas>
                
                <div id="testResult" class="result-box neutral">
                    Ready to scan
                </div>
                
                <div class="confidence-bar">
                    <div id="confidenceFill" class="confidence-fill" style="width: 0; background: #888;"></div>
                </div>
                
                <div class="btn-group" style="margin-top: 20px">
                    <button id="testStartBtn" class="btn btn-secondary" onclick="startCamera('testWebcam')">📷 Start Camera</button>
                    <button id="verifyBtn" class="btn btn-primary" onclick="verifyFace()" disabled>🔍 Verify Face</button>
                    <button id="continuousBtn" class="btn btn-secondary" onclick="toggleContinuous()" disabled>🔄 Continuous Scan</button>
                </div>
            </div>
        </div>
        
        <!-- Manage Panel -->
        <div id="manage" class="panel">
            <div class="card">
                <h2>Registered Faces</h2>
                <div id="facesList"></div>
            </div>
        </div>
        
        <!-- Logs Panel -->
        <div id="logs" class="panel">
            <div class="card">
                <h2>Access History</h2>
                <div id="logsContainer"></div>
            </div>
        </div>
    </main>
    
    <div id="toast" class="toast"></div>
    
    <script>
        // State
        let currentStream = null;
        let continuousMode = false;
        let continuousInterval = null;
        
        // Admin Auth State
        let adminCredentials = null; // { username, password }
        let pendingAdminAction = null; // Callback after successful login
        
        // Admin Auth Functions
        function isAdminLoggedIn() {
            return adminCredentials !== null;
        }
        
        function getAuthHeaders() {
            if (!adminCredentials) return {};
            const encoded = btoa(adminCredentials.username + ':' + adminCredentials.password);
            return { 'Authorization': 'Basic ' + encoded };
        }
        
        function showLoginModal(onSuccess) {
            pendingAdminAction = onSuccess;
            document.getElementById('loginError').style.display = 'none';
            document.getElementById('adminUser').value = '';
            document.getElementById('adminPass').value = '';
            document.getElementById('loginModal').classList.add('show');
            document.getElementById('adminUser').focus();
        }
        
        function hideLoginModal() {
            document.getElementById('loginModal').classList.remove('show');
            pendingAdminAction = null;
        }
        
        async function doLogin() {
            const username = document.getElementById('adminUser').value.trim();
            const password = document.getElementById('adminPass').value;
            
            if (!username || !password) {
                document.getElementById('loginError').textContent = 'Please enter credentials';
                document.getElementById('loginError').style.display = 'block';
                return;
            }
            
            // Test credentials with actual API call
            const encoded = btoa(username + ':' + password);
            try {
                const res = await fetch('/logs', {
                    headers: { 'Authorization': 'Basic ' + encoded }
                });
                
                if (res.ok) {
                    adminCredentials = { username, password };
                    hideLoginModal();
                    updateAdminStatus();
                    showToast('Logged in as admin', 'success');
                    
                    if (pendingAdminAction) {
                        pendingAdminAction();
                        pendingAdminAction = null;
                    }
                } else {
                    document.getElementById('loginError').textContent = 'Invalid credentials';
                    document.getElementById('loginError').style.display = 'block';
                }
            } catch (err) {
                document.getElementById('loginError').textContent = 'Connection error';
                document.getElementById('loginError').style.display = 'block';
            }
        }
        
        function logout() {
            adminCredentials = null;
            updateAdminStatus();
            showToast('Logged out', 'success');
            // Refresh current tab
            const activeTab = document.querySelector('.tab.active').dataset.tab;
            switchTab(activeTab);
        }
        
        function updateAdminStatus() {
            const statusEl = document.getElementById('adminStatus');
            if (isAdminLoggedIn()) {
                statusEl.innerHTML = '<span class="admin-badge" onclick="logout()">👤 Admin ✕</span>';
            } else {
                statusEl.innerHTML = '<button class="login-btn" onclick="showLoginModal()">🔑 Admin Login</button>';
            }
        }
        
        // Require admin for an action
        function requireAdmin(action) {
            if (isAdminLoggedIn()) {
                action();
            } else {
                showLoginModal(action);
            }
        }
        
        // Tab Navigation
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => switchTab(tab.dataset.tab));
        });
        
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
            document.getElementById(tabName).classList.add('active');
            
            // Load data for specific tabs
            if (tabName === 'manage') loadFaces();
            if (tabName === 'logs') {
                if (isAdminLoggedIn()) {
                    loadLogs();
                } else {
                    showAdminLockScreen('logsContainer', () => { loadLogs(); switchTab('logs'); });
                }
            }
            if (tabName === 'dashboard') loadDashboard();
        }
        
        // Handle hash navigation
        if (window.location.hash) {
            const tab = window.location.hash.slice(1);
            if (['dashboard', 'register', 'test', 'manage', 'logs'].includes(tab)) {
                switchTab(tab);
            }
        }
        
        // Camera Functions
        async function startCamera(videoId) {
            try {
                if (currentStream) {
                    currentStream.getTracks().forEach(t => t.stop());
                }
                
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { width: 640, height: 480, facingMode: 'user' } 
                });
                
                currentStream = stream;
                const video = document.getElementById(videoId);
                video.srcObject = stream;
                
                // Hide overlay
                const overlayId = videoId === 'webcam' ? 'webcamOverlay' : 'testOverlay';
                document.getElementById(overlayId).classList.add('hidden');
                
                // Enable buttons
                if (videoId === 'webcam') {
                    document.getElementById('captureBtn').disabled = false;
                    document.getElementById('startCamBtn').textContent = '🔄 Restart Camera';
                } else {
                    document.getElementById('verifyBtn').disabled = false;
                    document.getElementById('continuousBtn').disabled = false;
                    document.getElementById('testStartBtn').textContent = '🔄 Restart Camera';
                }
                
                showToast('Camera started', 'success');
            } catch (err) {
                showToast('Camera error: ' + err.message, 'error');
            }
        }
        
        // Capture and Register
        async function captureAndRegister() {
            const name = document.getElementById('personName').value.trim();
            if (!name) {
                showToast('Please enter a name', 'error');
                return;
            }
            
            const video = document.getElementById('webcam');
            const canvas = document.getElementById('captureCanvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            
            const base64 = canvas.toDataURL('image/jpeg').split(',')[1];
            await registerFace(name, base64);
        }
        
        // Handle Image Upload
        async function handleUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const name = document.getElementById('personName').value.trim();
            if (!name) {
                showToast('Please enter a name first', 'error');
                return;
            }
            
            const reader = new FileReader();
            reader.onload = async (e) => {
                const base64 = e.target.result.split(',')[1];
                await registerFace(name, base64);
            };
            reader.readAsDataURL(file);
        }
        
        // Register Face API
        async function registerFace(name, imageBase64) {
            const resultDiv = document.getElementById('registerResult');
            resultDiv.style.display = 'block';
            resultDiv.className = 'result-box neutral';
            resultDiv.textContent = 'Processing...';
            
            try {
                const res = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, image: imageBase64 })
                });
                
                const data = await res.json();
                
                if (data.success) {
                    resultDiv.className = 'result-box authorized';
                    resultDiv.innerHTML = '✓ ' + data.message;
                    document.getElementById('personName').value = '';
                    showToast('Face registered successfully!', 'success');
                    loadDashboard();
                } else {
                    resultDiv.className = 'result-box denied';
                    resultDiv.innerHTML = '✗ ' + data.error;
                    showToast(data.error, 'error');
                }
            } catch (err) {
                resultDiv.className = 'result-box denied';
                resultDiv.textContent = '✗ Error: ' + err.message;
                showToast('Registration failed', 'error');
            }
        }
        
        // Verify Face
        async function verifyFace() {
            const video = document.getElementById('testWebcam');
            const canvas = document.getElementById('testCanvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            
            const base64 = canvas.toDataURL('image/jpeg').split(',')[1];
            
            const resultDiv = document.getElementById('testResult');
            const confidenceFill = document.getElementById('confidenceFill');
            
            resultDiv.className = 'result-box neutral';
            resultDiv.textContent = 'Scanning...';
            
            try {
                const res = await fetch('/verify', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: base64 })
                });
                
                const data = await res.json();
                const confidence = (data.confidence || 0) * 100;
                
                confidenceFill.style.width = confidence + '%';
                
                if (data.authorized) {
                    resultDiv.className = 'result-box authorized';
                    resultDiv.innerHTML = `✓ AUTHORIZED<br><strong>${data.name}</strong><br>${confidence.toFixed(1)}% confidence`;
                    confidenceFill.style.background = '#00ff88';
                } else {
                    resultDiv.className = 'result-box denied';
                    resultDiv.innerHTML = `✗ DENIED<br>${data.name}<br>${confidence.toFixed(1)}% match`;
                    confidenceFill.style.background = '#ff4757';
                }
            } catch (err) {
                resultDiv.className = 'result-box denied';
                resultDiv.textContent = '✗ Error: ' + err.message;
            }
        }
        
        // Continuous Scanning
        function toggleContinuous() {
            const btn = document.getElementById('continuousBtn');
            
            if (continuousMode) {
                continuousMode = false;
                clearInterval(continuousInterval);
                btn.textContent = '🔄 Continuous Scan';
                btn.classList.remove('btn-danger');
                btn.classList.add('btn-secondary');
            } else {
                continuousMode = true;
                btn.textContent = '⏹ Stop Scanning';
                btn.classList.remove('btn-secondary');
                btn.classList.add('btn-danger');
                
                verifyFace();
                continuousInterval = setInterval(verifyFace, 2000);
            }
        }
        
        // Load Dashboard Data
        async function loadDashboard() {
            try {
                // Faces are public
                const facesRes = await fetch('/faces');
                const faces = await facesRes.json();
                document.getElementById('faceCount').textContent = faces.length;
                
                // Logs require admin - try if logged in
                if (isAdminLoggedIn()) {
                    const logsRes = await fetch('/logs', { headers: getAuthHeaders() });
                    if (logsRes.ok) {
                        const logs = await logsRes.json();
                        document.getElementById('logCount').textContent = logs.length;
                        
                        const today = new Date().toISOString().split('T')[0];
                        const todayLogs = logs.filter(l => l.timestamp && l.timestamp.startsWith(today));
                        document.getElementById('todayCount').textContent = todayLogs.length;
                        
                        // Recent logs
                        const recentDiv = document.getElementById('recentLogs');
                        if (logs.length === 0) {
                            recentDiv.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📋</div>No activity yet</div>';
                        } else {
                            recentDiv.innerHTML = logs.slice(0, 5).map(log => `
                                <div class="face-item">
                                    <div>
                                        <span class="${log.authorized ? 'log-granted' : 'log-denied'}">
                                            ${log.authorized ? '✓' : '✗'}
                                        </span>
                                        <strong>${log.name}</strong>
                                    </div>
                                    <div class="face-date">${formatTime(log.timestamp)}</div>
                                </div>
                            `).join('');
                        }
                    }
                } else {
                    // Not admin - show locked state
                    document.getElementById('logCount').textContent = '🔒';
                    document.getElementById('todayCount').textContent = '🔒';
                    document.getElementById('recentLogs').innerHTML = '<div class="admin-lock"><div class="admin-lock-icon">🔒</div>Admin login required<br><button class="btn btn-secondary" style="margin-top:15px" onclick="showLoginModal(loadDashboard)">Login to View</button></div>';
                }
            } catch (err) {
                console.error('Dashboard load error:', err);
            }
        }
        
        // Show admin lock screen for a container
        function showAdminLockScreen(containerId, onLogin) {
            const container = document.getElementById(containerId);
            container.innerHTML = '<div class="admin-lock"><div class="admin-lock-icon">🔒</div>Admin login required to view this section<br><button class="btn btn-primary" style="margin-top:15px" onclick="showLoginModal(arguments[0])">Login</button></div>';
            container.querySelector('button').onclick = () => showLoginModal(onLogin);
        }
        
        // Load Faces
        async function loadFaces() {
            try {
                const res = await fetch('/faces');
                const faces = await res.json();
                
                const container = document.getElementById('facesList');
                
                if (faces.length === 0) {
                    container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">👤</div>No faces registered yet</div>';
                } else {
                    container.innerHTML = faces.map(face => `
                        <div class="face-item">
                            <div>
                                <div class="face-name">${face.name}</div>
                                <div class="face-date">ID: ${face.id} | ${formatTime(face.registered_at)}</div>
                            </div>
                            <button class="btn btn-danger" onclick="deleteFace('${face.id}', '${face.name}')">🗑️ Delete</button>
                        </div>
                    `).join('');
                }
            } catch (err) {
                console.error('Load faces error:', err);
            }
        }
        
        // Delete Face (Admin only)
        function deleteFace(id, name) {
            requireAdmin(async () => {
                if (!confirm(`Delete ${name}?`)) return;
                
                try {
                    const res = await fetch('/faces/' + id, { 
                        method: 'DELETE',
                        headers: getAuthHeaders()
                    });
                    
                    if (res.ok) {
                        showToast(`Deleted ${name}`, 'success');
                        loadFaces();
                        loadDashboard();
                    } else if (res.status === 403) {
                        adminCredentials = null;
                        updateAdminStatus();
                        showToast('Session expired, please login again', 'error');
                    } else {
                        showToast('Delete failed', 'error');
                    }
                } catch (err) {
                    showToast('Delete failed: ' + err.message, 'error');
                }
            });
        }
        
        // Load Logs (Admin only)
        async function loadLogs() {
            if (!isAdminLoggedIn()) {
                showAdminLockScreen('logsContainer', () => { loadLogs(); });
                return;
            }
            
            try {
                const res = await fetch('/logs', { headers: getAuthHeaders() });
                
                if (res.status === 403) {
                    adminCredentials = null;
                    updateAdminStatus();
                    showAdminLockScreen('logsContainer', () => { loadLogs(); });
                    return;
                }
                
                const logs = await res.json();
                const container = document.getElementById('logsContainer');
                
                if (logs.length === 0) {
                    container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📋</div>No logs yet</div>';
                } else {
                    container.innerHTML = `
                        <table class="logs-table">
                            <thead>
                                <tr><th>Time</th><th>Status</th><th>Name</th><th>Confidence</th></tr>
                            </thead>
                            <tbody>
                                ${logs.map(log => `
                                    <tr>
                                        <td>${formatTime(log.timestamp)}</td>
                                        <td class="${log.authorized ? 'log-granted' : 'log-denied'}">
                                            ${log.authorized ? '✓ Granted' : '✗ Denied'}
                                        </td>
                                        <td>${log.name}</td>
                                        <td>${((log.confidence || 0) * 100).toFixed(1)}%</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    `;
                }
            } catch (err) {
                console.error('Load logs error:', err);
            }
        }
        
        // Utilities
        function formatTime(isoString) {
            if (!isoString) return 'Unknown';
            const date = new Date(isoString);
            return date.toLocaleString();
        }
        
        function showToast(message, type = 'success') {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = 'toast ' + type + ' show';
            
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }
        
        // Initial load
        updateAdminStatus();
        loadDashboard();
        
        // Handle Enter key in login modal
        document.getElementById('adminPass').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') doLogin();
        });
    </script>
</body>
</html>
'''
