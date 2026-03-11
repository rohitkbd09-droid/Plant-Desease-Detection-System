/**
 * Advanced Mobile-First Plant Disease Detection System
 * Real-time camera capture, image analysis, weather integration
 */

const API_BASE = 'http://localhost:5000';
let currentUserId = localStorage.getItem('userId') || `user_${Date.now()}`;
let video;
let canvas;
let ctx;
let stream;
let lastScanResult = null;

function formatRecommendationLabel(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

function renderRecommendationValue(value) {
    if (value === null || value === undefined || value === '') {
        return '';
    }

    if (Array.isArray(value)) {
        return value.map((item) => `• ${item}`).join('<br>');
    }

    if (typeof value === 'object') {
        return Object.entries(value)
            .filter(([, nestedValue]) => nestedValue !== null && nestedValue !== undefined && nestedValue !== '')
            .map(([nestedKey, nestedValue]) => `<strong>${formatRecommendationLabel(nestedKey)}:</strong> ${renderRecommendationValue(nestedValue)}`)
            .join('<br>');
    }

    return String(value);
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupCamera();
    setupEventListeners();
    loadUserSettings();
    loadDashboard();
});

// ============= CAMERA FUNCTIONS =============

function setupCamera() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
}

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
            audio: false
        });

        video.srcObject = stream;
        video.style.display = 'block';

        document.getElementById('startCamera').style.display = 'none';
        document.getElementById('capturePhoto').style.display = 'inline-flex';
        document.getElementById('stopCamera').style.display = 'inline-flex';
        document.getElementById('uploadSection').style.display = 'none';

        showAlert('📷 Camera started successfully', 'success');
    } catch (error) {
        console.error('Error accessing camera:', error);
        showAlert('❌ Could not access camera: ' + error.message, 'error');
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        video.style.display = 'none';
        document.getElementById('startCamera').style.display = 'inline-flex';
        document.getElementById('capturePhoto').style.display = 'none';
        document.getElementById('stopCamera').style.display = 'none';
        document.getElementById('uploadSection').style.display = 'none';
    }
}

function capturePhoto() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Flip the image (mirror effect)
    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(video, 0, 0);

    // Stop camera
    stopCamera();
    video.style.display = 'none';

    // Show upload section
    document.getElementById('uploadSection').style.display = 'block';
    showAlert('✅ Photo captured! Ready for analysis.', 'success');
}

// ============= IMAGE ANALYSIS =============

async function analyzeImage() {
    try {
        const analyzeBtn = document.getElementById('analyzeImage');
        const spinner = analyzeBtn.querySelector('.spinner');

        // Validate inputs
        const cropType = document.getElementById('cropType').value;
        const fieldLocation = document.getElementById('fieldLocation').value;

        if (!fieldLocation) {
            showAlert('Please enter field location', 'warning');
            return;
        }

        // Show loading state
        spinner.style.display = 'inline-block';
        analyzeBtn.disabled = true;

        // Convert canvas to blob
        canvas.toBlob(async (blob) => {
            const formData = new FormData();
            formData.append('image', blob, 'capture.jpg');
            formData.append('user_id', currentUserId);
            formData.append('crop_type', cropType);
            formData.append('field_location', fieldLocation);

            // Try to get geolocation
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        formData.append('latitude', position.coords.latitude);
                        formData.append('longitude', position.coords.longitude);
                        sendAnalysisRequest(formData, analyzeBtn, spinner);
                    },
                    () => {
                        // Geolocation failed, proceed without it
                        sendAnalysisRequest(formData, analyzeBtn, spinner);
                    },
                    { timeout: 5000 }
                );
            } else {
                sendAnalysisRequest(formData, analyzeBtn, spinner);
            }
        }, 'image/jpeg', 0.9);
    } catch (error) {
        console.error('Error in analyzeImage:', error);
        showAlert('Error: ' + error.message, 'error');
    }
}

async function sendAnalysisRequest(formData, btn, spinner) {
    try {
        const response = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Analysis failed');

        const result = await response.json();
        lastScanResult = result;

        // Display results
        displayAnalysisResults(result);

        // Save to local storage
        let scans = JSON.parse(localStorage.getItem('scans') || '[]');
        scans.unshift(result);
        scans = scans.slice(0, 50); // Keep last 50
        localStorage.setItem('scans', JSON.stringify(scans));

        showAlert('✅ Analysis complete!', 'success');
        switchTab('results');
    } catch (error) {
        console.error('Error:', error);
        showAlert('❌ Analysis failed: ' + error.message, 'error');
    } finally {
        spinner.style.display = 'none';
        btn.disabled = false;
    }
}

function displayAnalysisResults(result) {
    const container = document.getElementById('resultsContainer');
    const diseaseClass = result.disease === 'Healthy' ? 'healthy' : 'disease-result';

    const severity = result.severity || 'unknown';
    const severityClass = `severity-${severity}`;
    const confidence = Math.round(result.confidence * 100);

    let html = `
        <div class="card ${diseaseClass}">
            <div class="card-title">
                ${result.disease === 'Healthy' ? '✅' : '⚠️'} ${result.disease}
            </div>
            <div class="card-subtitle">${result.timestamp || new Date().toLocaleString()}</div>
            
            <div class="result-item">
                <div class="result-label">Severity Level</div>
                <div class="result-value">
                    <span class="severity-badge ${severityClass}">${severity.toUpperCase()}</span>
                </div>
            </div>

            <div class="result-item">
                <div class="result-label">Confidence Score</div>
                <div class="result-value">${confidence}%</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${confidence}%"></div>
                </div>
            </div>
    `;

    if (result.affected_area_percent) {
        html += `
            <div class="result-item">
                <div class="result-label">Affected Area</div>
                <div class="result-value">${result.affected_area_percent.toFixed(1)}%</div>
            </div>
        `;
    }

    if (result.environmental_data && Object.keys(result.environmental_data).length > 0) {
        html += `
            <div class="result-item">
                <div class="result-label">Environmental Data</div>
                <div class="result-value">
                    Temperature: ${result.environmental_data.temperature}°C<br>
                    Humidity: ${result.environmental_data.humidity}%<br>
                    Weather: ${result.environmental_data.weather_condition}
                </div>
            </div>
        `;
    }

    const recommendationData = result.recommendation || result.recommendations;
    if (recommendationData) {
        html += `
            <div class="result-item" style="background: #F9F9F9; margin-top: 1rem;">
                <div class="result-label">📋 Recommendations</div>
                <div class="result-value">
        `;

        for (const [key, value] of Object.entries(recommendationData)) {
            const renderedValue = renderRecommendationValue(value);
            if (renderedValue) {
                html += `<strong>${formatRecommendationLabel(key)}:</strong> ${renderedValue}<br>`;
            }
        }

        html += `
                </div>
            </div>
        `;
    }

    if (Array.isArray(result.complete_treatment_process) && result.complete_treatment_process.length > 0) {
        html += `
            <div class="result-item" style="background: #FFF8E8; margin-top: 1rem;">
                <div class="result-label">Complete Treatment Process</div>
                <div class="result-value">
                    ${result.complete_treatment_process.map(step => `• ${step}`).join('<br>')}
                </div>
            </div>
        `;
    }

    html += `
            <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                <button class="btn btn-secondary btn-small" style="flex: 1;" onclick="downloadReport('${result.scan_id || 'report'}')">
                    📄 Download PDF
                </button>
                <button class="btn btn-secondary btn-small" style="flex: 1;" onclick="shareResults()">
                    📤 Share
                </button>
            </div>
        </div>
    `;

    container.innerHTML = html;
}

// ============= CALENDAR FUNCTIONS =============

async function loadCalendar() {
    try {
        const crop = document.getElementById('calendarCrop').value;
        const container = document.getElementById('calendarContainer');

        container.innerHTML = '<p style="text-align: center;">Loading calendar...</p>';

        const response = await fetch(`${API_BASE}/calendar/crop/${crop}`);
        if (!response.ok) throw new Error('Failed to load calendar');

        const data = await response.json();

        let html = `<h3 style="margin-top: 1.5rem; color: #2C5F2D;">📅 ${crop} Farming Calendar</h3>`;

        if (data.events && data.events.length > 0) {
            data.events.forEach(event => {
                html += `
                    <div class="calendar-event">
                        <div class="event-title">${event.event}</div>
                        <div class="event-date">Month ${event.month} (${event.duration} days)</div>
                        <div style="font-size: 0.9rem; margin-top: 0.5rem;">${event.details}</div>
                    </div>
                `;
            });
        }

        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading calendar:', error);
        showAlert('Error loading calendar: ' + error.message, 'error');
    }
}

// ============= WEATHER FUNCTIONS =============

async function getWeatherData() {
    try {
        const container = document.getElementById('weatherContainer');
        container.innerHTML = '<p style="text-align: center;">Getting location...</p>';

        if (!navigator.geolocation) {
            showAlert('Geolocation not supported', 'error');
            return;
        }

        navigator.geolocation.getCurrentPosition(async (position) => {
            const { latitude, longitude } = position.coords;

            const response = await fetch(`${API_BASE}/weather`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    latitude,
                    longitude,
                    disease: 'General',
                    crop_type: 'Rice'
                })
            });

            if (!response.ok) throw new Error('Weather data unavailable');

            const data = await response.json();
            displayWeatherData(data, latitude, longitude);
        }, (error) => {
            showAlert('Location access denied', 'error');
        });
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error: ' + error.message, 'error');
    }
}

function displayWeatherData(data, lat, lon) {
    const container = document.getElementById('weatherContainer');
    const weather = data.weather || {};
    const risk = data.disease_risk || {};

    let html = `
        <div class="card">
            <div class="card-title">🌍 Current Location</div>
            <div class="result-item">
                <div class="result-label">Coordinates</div>
                <div class="result-value">${lat.toFixed(2)}°, ${lon.toFixed(2)}°</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Region</div>
                <div class="result-value">${data.region_info?.region || 'Unknown'}</div>
            </div>
        </div>

        <div class="card weather-widget">
            <div class="card-title" style="color: white;">🌤️ Current Weather</div>
            ${weather ? `
                <div class="weather-item">
                    <span>Temperature</span>
                    <span><strong>${weather.temperature}°C</strong></span>
                </div>
                <div class="weather-item">
                    <span>Humidity</span>
                    <span><strong>${weather.humidity}%</strong></span>
                </div>
                <div class="weather-item">
                    <span>Condition</span>
                    <span><strong>${weather.weather}</strong></span>
                </div>
                <div class="weather-item">
                    <span>Wind Speed</span>
                    <span><strong>${weather.wind_speed} km/h</strong></span>
                </div>
            ` : '<p>Weather data unavailable</p>'}
        </div>
    `;

    if (risk && risk.risk_level) {
        const riskColor = risk.risk_level === 'high' ? '#FF6B6B' : risk.risk_level === 'moderate' ? '#FFA500' : '#4CAF50';
        html += `
            <div class="card" style="border-left-color: ${riskColor};">
                <div class="card-title">⚠️ Disease Risk Assessment</div>
                <div class="result-item">
                    <div class="result-label">Risk Level</div>
                    <div class="result-value" style="color: ${riskColor}; font-weight: bold;">
                        ${risk.risk_level.toUpperCase()}
                    </div>
                </div>
                <div class="result-item">
                    <div class="result-label">Risk Score</div>
                    <div class="result-value">${risk.risk_score || 0}/100</div>
                </div>
                ${risk.recommendations ? `
                    <div class="result-item">
                        <div class="result-label">Recommendations</div>
                        <div class="result-value">
                            ${risk.recommendations.map(r => `• ${r}`).join('<br>')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }

    container.innerHTML = html;
}

// ============= DASHBOARD =============

async function loadDashboard() {
    try {
        const container = document.getElementById('dashboardContainer');

        // Get local scan history
        let scans = JSON.parse(localStorage.getItem('scans') || '[]');

        if (scans.length === 0) {
            container.innerHTML = '<p style="text-align: center; margin: 2rem;">No scan data yet. Start scanning crops!</p>';
            return;
        }

        // Calculate statistics
        const totalScans = scans.length;
        const healthyCount = scans.filter(s => s.disease === 'Healthy').length;
        const diseaseCount = totalScans - healthyCount;

        // Disease frequency
        const diseaseCounts = {};
        scans.forEach(s => {
            diseaseCounts[s.disease] = (diseaseCounts[s.disease] || 0) + 1;
        });

        const mostCommon = Object.entries(diseaseCounts).sort((a, b) => b[1] - a[1])[0];

        let html = `
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-number">${totalScans}</div>
                    <div class="stat-label">Total Scans</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">${healthyCount}</div>
                    <div class="stat-label">Healthy</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">${diseaseCount}</div>
                    <div class="stat-label">Diseased</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">${diseaseCount > 0 ? (diseaseCount / totalScans * 100).toFixed(0) : 0}%</div>
                    <div class="stat-label">Disease Rate</div>
                </div>
            </div>

            <div class="card" style="margin-top: 1.5rem;">
                <div class="card-title">📊 Disease Distribution</div>
        `;

        for (const [disease, count] of Object.entries(diseaseCounts)) {
            const percentage = (count / totalScans * 100).toFixed(0);
            html += `
                <div class="result-item">
                    <div class="result-label">${disease}</div>
                    <div class="result-value">${count} scans (${percentage}%)</div>
                </div>
            `;
        }

        html += `</div>`;

        // Recent scans
        html += `
            <div class="card" style="margin-top: 1rem;">
                <div class="card-title">📋 Recent Scans</div>
        `;

        scans.slice(0, 5).forEach(scan => {
            const date = new Date(scan.timestamp).toLocaleDateString();
            const severity = scan.severity || 'unknown';
            html += `
                <div class="result-item">
                    <div class="result-label">${scan.disease}</div>
                    <div class="result-value">
                        ${date} • 
                        <span class="severity-badge severity-${severity}">${severity}</span>
                        ${Math.round(scan.confidence * 100)}%
                    </div>
                </div>
            `;
        });

        html += `</div>`;

        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// ============= SETTINGS =============

function saveSettings() {
    const settings = {
        farmerName: document.getElementById('farmerName').value,
        email: document.getElementById('farmerEmail').value,
        region: document.getElementById('region').value,
        language: document.getElementById('language').value,
        userId: currentUserId
    };

    localStorage.setItem('farmerSettings', JSON.stringify(settings));
    showAlert('✅ Settings saved successfully!', 'success');
}

function loadUserSettings() {
    const settings = JSON.parse(localStorage.getItem('farmerSettings') || '{}');

    if (settings.farmerName) document.getElementById('farmerName').value = settings.farmerName;
    if (settings.email) document.getElementById('farmerEmail').value = settings.email;
    if (settings.region) document.getElementById('region').value = settings.region;
    if (settings.language) document.getElementById('language').value = settings.language;
}

// ============= UTILITY FUNCTIONS =============

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.nav-btn, .nav-item').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const tabElement = document.getElementById(tabName);
    if (tabElement) {
        tabElement.classList.add('active');
    }

    // Update nav buttons
    document.querySelectorAll(`.nav-btn[data-tab="${tabName}"], .nav-item`).forEach(btn => {
        if ((btn.dataset && btn.dataset.tab === tabName) || btn.textContent.includes(tabName)) {
            btn.classList.add('active');
        }
    });

    // Reload dashboard when opening
    if (tabName === 'dashboard') {
        loadDashboard();
    }
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const header = document.querySelector('.header');
    header.parentNode.insertBefore(alertDiv, header.nextSibling);

    setTimeout(() => alertDiv.remove(), 4000);
}

async function downloadReport(scanId) {
    showAlert('Generating PDF...', 'info');
    // TODO: Implement PDF download from API
}

async function shareResults() {
    if (navigator.share && lastScanResult) {
        try {
            await navigator.share({
                title: 'Plant Disease Detection',
                text: `Disease: ${lastScanResult.disease}, Severity: ${lastScanResult.severity}`,
                url: window.location.href
            });
        } catch (error) {
            console.log('Share cancelled:', error);
        }
    } else {
        showAlert('Share feature not supported on this device', 'warning');
    }
}

// ============= EVENT LISTENERS =============

function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            switchTab(btn.dataset.tab);
        });
    });

    // Camera controls
    document.getElementById('startCamera').addEventListener('click', startCamera);
    document.getElementById('capturePhoto').addEventListener('click', capturePhoto);
    document.getElementById('stopCamera').addEventListener('click', stopCamera);
    document.getElementById('analyzeImage').addEventListener('click', analyzeImage);
}

