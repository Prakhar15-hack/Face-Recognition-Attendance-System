const express = require('express');
const fs = require('fs');
const { exec } = require('child_process');
const jwt = require('jsonwebtoken'); // NAYA: Security Token ke liye
const cors = require('cors');        // NAYA: Frontend connection ke liye

const app = express();
app.use(express.json()); // JSON data read karne ke liye
app.use(cors()); 

const PORT = 3000;

// 🔐 TERA SECRET KEY (Ye kisi ko nahi pata hona chahiye)
const SECRET_KEY = "PrakharCyberSec_2026_UoA"; 

// 🛡️ FUNCTION: Audit Log File Create/Update karna
function logAudit(ip, status, usernameAttempt) {
    const now = new Date();
    const dateStr = now.toLocaleDateString('en-GB');
    const timeStr = now.toLocaleTimeString('en-GB');
    
    const logEntry = `${dateStr},${timeStr},${ip},${usernameAttempt},${status}\n`;
    
    if (!fs.existsSync('Audit_Log.csv')) {
        fs.writeFileSync('Audit_Log.csv', 'Date,Time,IP_Address,Username,Status\n');
    }
    fs.appendFileSync('Audit_Log.csv', logEntry);
}

// 🚀 ROUTE 1: Admin Login Endpoint
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    const clientIP = req.headers['x-forwarded-for'] || req.socket.remoteAddress;

    // Admin Credentials
    if (username === 'admin' && password === 'prakhar@123') {
        const token = jwt.sign({ role: 'admin', user: username }, SECRET_KEY, { expiresIn: '1h' });
        logAudit(clientIP, "SUCCESS", username);
        res.json({ success: true, token: token, message: "Welcome Admin!" });
    } else {
        logAudit(clientIP, "FAILED_ATTEMPT", username);
        res.status(401).json({ success: false, message: "Invalid Credentials!" });
    }
});

// 🛡️ MIDDLEWARE: Token Verify Karna
const verifyToken = (req, res, next) => {
    const bearerHeader = req.headers['authorization'];
    if (typeof bearerHeader !== 'undefined') {
        const token = bearerHeader.split(' ')[1];
        jwt.verify(token, SECRET_KEY, (err, decoded) => {
            if (err) return res.status(403).json({ message: "Token Expired or Tampered!" });
            req.user = decoded; 
            next();
        });
    } else {
        res.status(403).json({ message: "Access Denied! No Token." });
    }
};

// ==========================================
// TERE PURANE ROUTES (Ab Secured hain)
// ==========================================

// 🚀 SECURED ROUTE: Ab bina Token ke koi data nahi dekh payega! (Notice: verifyToken add kiya hai)
app.get('/get-attendance', verifyToken, (req, res) => {
    const file_path = 'Attendance_Log.csv';
    
    if (fs.existsSync(file_path)) {
        const data = fs.readFileSync(file_path, 'utf8');
        const lines = data.split('\n');
        
        let results = [];
        for(let i=1; i<lines.length; i++) {
            const cols = lines[i].split(',');
            if(cols.length >= 5) {
                results.push({
                    Name: cols[1],
                    Course: cols[2],
                    Date: cols[3],
                    Time: cols[4]
                });
            }
        }
        res.json(results.reverse());
    } else {
        res.json([]);
    }
});

app.use(express.static('public'));

// 🚀 CAMERA TRIGGER ROUTE (Ye khula rakha hai taaki students attendance laga sakein)
app.get('/start-attendance', (req, res) => {
    console.log("[INFO] Camera button clicked! Starting live_attendance.py...");
    exec('python live_attendance.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return;
        }
        console.log(`[STDOUT]\n${stdout}`);
    });
    res.send("Camera Started");
});

app.listen(PORT, () => {
    console.log(`[INFO] Server running on http://localhost:${PORT}`);
    console.log(`[SECURE] `);
});