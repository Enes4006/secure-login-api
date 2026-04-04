const API_URL = "http://127.0.0.1:8000";

// Kayıt İşlemi
async function register() {
    const username = document.getElementById('regUser').value;
    const password = document.getElementById('regPass').value;

    const response = await fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    showMessage(data.detail || data.message);
}

// Giriş İşlemi
async function login() {
    const username = document.getElementById('loginUser').value;
    const password = document.getElementById('loginPass').value;

    const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    
    if (data.access_token) {
        // Token'ı tarayıcı hafızasına (localStorage) kaydet
        localStorage.setItem('token', data.access_token);
        showMessage("Giriş Başarılı! Token kaydedildi.");
    } else {
        showMessage(data.detail || "Giriş başarısız.");
    }
}

// Korumalı Veriyi Getirme
async function getProtectedData() {
    const token = localStorage.getItem('token');

    if (!token) {
        showMessage("Hata: Önce giriş yapmalısınız!");
        return;
    }

    const response = await fetch(`${API_URL}/protected`, {
        method: 'GET',
        headers: { 
            'Authorization': `Bearer ${token}` // İşte can alıcı nokta burası!
        }
    });

    const data = await response.json();
    showMessage(data.message || data.detail);
}

function showMessage(msg) {
    document.getElementById('message').innerText = msg;
}