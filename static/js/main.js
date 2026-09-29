// POLARIS Client Application Logic
// NCPOR Polar Science Outreach & Knowledge Repository

let polarMap = null;
let stationsData = [];
let currentSelectedStationId = 'bharati';
let currentAIGenerated = null;
let currentAIPlatform = 'twitter';
let currentChartInstance = null;
let currentModalDatasetId = null;

// Quiz State
let quizQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = {};

// Presets for AI Engine
const AI_PRESETS = {
    arctic_monsoon: {
        title: "Teleconnections between Arctic Amplification, Sea Ice Depletion, and Indian Summer Monsoon Extremes",
        station: "himadri",
        text: "Long-term atmospheric observations at Himadri station (Ny-Ålesund, 79°N) reveal that rapid depletion of Barents-Kara sea ice during winter weakens the circum-polar jet stream. This destabilization induces persistent atmospheric planetary wave trains that correlate with delayed withdrawal of the Indian Summer Monsoon and an increase in localized extreme precipitation events across north-central India."
    },
    ice_core_co2: {
        title: "150-Year Ice Core CO2 & Stable Isotope Chronology from Schirmacher Oasis",
        station: "maitri",
        text: "Continuous ice core drilling conducted at Maitri station in East Antarctica has successfully retrieved an uninterrupted 150-year paleo-environmental record. Geochemical analysis of entrapped atmospheric air bubbles shows an acceleration in atmospheric carbon dioxide concentrations from 288 ppm in the late 19th century to over 422 ppm in 2024, accompanied by systematic isotopic shifts indicating Southern Ocean thermal expansion."
    },
    himalayan_glacier: {
        title: "Decadal Cryospheric Mass Balance Loss in Western Himalayas (Chandra Basin)",
        station: "himansh",
        text: "Ten years of glaciological mass balance measurements at Himansh station (altitude 4,080m) in Spiti Valley demonstrate a cumulative specific mass deficit of -6.65 meters water equivalent on Chhota Shigri glacier. Geodetic ablation stake monitoring indicates an accelerating thinning rate in lower glacier ablation zones, underscoring urgent water security challenges for downstream Indus-Ganga basins."
    },
    antarctic_microbes: {
        title: "Novel Cold-Active Psychrophilic Enzymes Isolated from Antarctic Cyanobacterial Mats",
        station: "maitri",
        text: "Biological sampling of sub-glacial cyanobacterial mats near Lake Priyadarshini in Antarctica has led to the isolation of psychrophilic bacterial strains capable of thriving at sub-zero conditions. The isolated enzymes exhibit remarkable biocatalytic activity at 4°C, offering transformative breakthroughs for eco-friendly cold-wash industrial detergents and temperature-sensitive pharmaceutical synthesis."
    }
};

// ----------------- INITIALIZATION ----------------- //
document.addEventListener('DOMContentLoaded', () => {
    initStationsAndMap();
    loadExpeditions();
    loadRepository();
    loadMedia();
    loadDisseminations();
    loadQuiz();
    loadAdminMetrics();
});

// ----------------- TAB SWITCHING ----------------- //
function switchTab(tabId) {
    const tabs = ['explorer', 'repository', 'ai-engine', 'education', 'admin'];
    tabs.forEach(t => {
        const sec = document.getElementById(`tab-${t}`);
        const btn = document.getElementById(`tab-btn-${t}`);
        if (sec) sec.classList.add('hidden');
        if (btn) btn.classList.remove('active-tab');
    });

    const activeSec = document.getElementById(`tab-${tabId}`);
    const activeBtn = document.getElementById(`tab-btn-${tabId}`);
    if (activeSec) activeSec.classList.remove('hidden');
    if (activeBtn) activeBtn.classList.add('active-tab');

    // Invalidate Leaflet map size when switching back to explorer tab
    if (tabId === 'explorer' && polarMap) {
        setTimeout(() => polarMap.invalidateSize(), 200);
    }
}

// ----------------- LEAFLET POLAR MAP & STATIONS ----------------- //
async function initStationsAndMap() {
    try {
        const res = await fetch('/api/stations');
        stationsData = await res.json();

        // Update live telemetry ticker bar
        renderTelemetryTicker();

        // Initialize Leaflet Map
        const mapContainer = document.getElementById('polar-map');
        if (mapContainer && !polarMap) {
            polarMap = L.map('polar-map', {
                center: [10, 45],
                zoom: 2,
                minZoom: 1,
                maxZoom: 10
            });

            // High-Resolution Satellite & Polar Terrain Tiles (100% Free - NO API KEY REQUIRED)
            const satelliteTiles = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                attribution: 'Satellite &copy; Esri, USGS, NASA | NCPOR Polar Geodesy',
                maxZoom: 18
            }).addTo(polarMap);

            // Overlay for boundaries, station regions and country labels (Free - NO API KEY REQUIRED)
            L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
                maxZoom: 18,
                opacity: 0.85
            }).addTo(polarMap);

            // Add station markers
            stationsData.forEach(st => {
                let pinClass = 'pin-antarctica';
                let iconClass = 'fa-mountain-sun';

                if (st.region.includes('Arctic')) {
                    pinClass = 'pin-arctic';
                    iconClass = 'fa-compass';
                } else if (st.region.includes('Himalaya')) {
                    pinClass = 'pin-himalaya';
                    iconClass = 'fa-mountain';
                }

                const customIcon = L.divIcon({
                    className: 'custom-leaflet-marker',
                    html: `<div class="station-pin ${pinClass}" title="${st.name}"><i class="fa-solid ${iconClass}"></i></div>`,
                    iconSize: [32, 32],
                    iconAnchor: [16, 16]
                });

                const marker = L.marker([st.latitude, st.longitude], { icon: customIcon }).addTo(polarMap);
                
                marker.bindPopup(`
                    <div style="font-size: 12px; min-width: 180px;">
                        <b style="color: #38bdf8; font-size: 13px;">${st.name}</b><br>
                        <span style="color: #94a3b8;">${st.location}</span><br>
                        <div style="margin-top: 6px; padding-top: 4px; border-top: 1px solid #163860;">
                            <b>Temp:</b> ${st.current_temp_c}°C | <b>Wind:</b> ${st.wind_speed_knots} kt<br>
                            <b>Status:</b> <span style="color: #10b981;">${st.status}</span>
                        </div>
                    </div>
                `);

                marker.on('click', () => {
                    selectStation(st.id);
                });
            });

            // Select default station (Bharati)
            selectStation('bharati');
        }
    } catch (err) {
        console.error("Error loading stations:", err);
    }
}

function renderTelemetryTicker() {
    const bar = document.getElementById('telemetry-bar');
    const summarySpan = document.getElementById('telemetry-summary');
    if (!bar) return;

    let html = '';
    stationsData.forEach(st => {
        html += `
            <div class="flex items-center gap-3 bg-black/40 px-3 py-1 rounded-lg border border-slate-700/60 cursor-pointer hover:border-cyan-400" onclick="selectStation('${st.id}')">
                <span class="w-2 h-2 rounded-full ${st.status === 'Active' ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}"></span>
                <span class="text-white font-semibold">${st.name.split(' ')[0]}</span>
                <span class="text-cyan-300 font-mono">${st.current_temp_c}°C</span>
                <span class="text-slate-400">${st.wind_speed_knots} kt</span>
                <span class="text-slate-500">•</span>
                <span class="text-slate-300 truncate max-w-[130px]">${st.condition}</span>
            </div>
        `;
    });
    bar.innerHTML = html;

    if (summarySpan && stationsData.length > 0) {
        summarySpan.textContent = `All 4 Polar Stations Live | 43rd ISEA Wintering Active`;
    }
}

function selectStation(stationId) {
    currentSelectedStationId = stationId;
    const st = stationsData.find(s => s.id === stationId);
    if (!st) return;

    // Pan map to station
    if (polarMap) {
        polarMap.flyTo([st.latitude, st.longitude], 4, { duration: 1.5 });
    }

    // Populate Station Details Card
    document.getElementById('station-detail-tag').textContent = `${st.region.toUpperCase()} RESEARCH OUTPOST`;
    document.getElementById('station-detail-status').textContent = st.status;
    document.getElementById('station-detail-img').src = st.image_url;
    document.getElementById('station-detail-name').textContent = st.name;
    document.getElementById('station-detail-loc').textContent = st.location;
    document.getElementById('station-detail-coords').textContent = `${st.latitude.toFixed(2)}°, ${st.longitude.toFixed(2)}°`;
    document.getElementById('station-detail-temp').textContent = `${st.current_temp_c}°C`;
    document.getElementById('station-detail-wind').textContent = `${st.wind_speed_knots} knots`;
    document.getElementById('station-detail-personnel').textContent = `${st.active_personnel} Scientists`;
    document.getElementById('station-detail-elevation').textContent = `${st.elevation_m} m ASL`;
    document.getElementById('station-detail-disciplines').textContent = st.primary_disciplines;
    document.getElementById('station-detail-summary').textContent = st.summary;
}

// ----------------- EXPEDITIONS ----------------- //
async function loadExpeditions() {
    try {
        const res = await fetch('/api/expeditions');
        const data = await res.json();
        const container = document.getElementById('expeditions-container');
        if (!container) return;

        let html = '';
        data.forEach(exp => {
            html += `
                <div class="bg-[#051120] rounded-xl border border-slate-800 p-4 flex flex-col justify-between hover:border-cyan-500/40 transition-colors">
                    <div>
                        <div class="flex items-center justify-between text-xs mb-2">
                            <span class="px-2 py-0.5 rounded bg-cyan-950 border border-cyan-500/30 text-cyan-300 font-mono">${exp.code}</span>
                            <span class="text-slate-400 font-tech">${exp.season}</span>
                        </div>
                        <h4 class="text-sm font-tech font-bold text-white mb-1">${exp.title}</h4>
                        <p class="text-[11px] text-slate-400 mb-2"><b>Leader:</b> ${exp.leader}</p>
                        <p class="text-xs text-slate-300 line-clamp-3">${exp.milestones}</p>
                    </div>
                    <div class="mt-3 pt-2 border-t border-slate-800 flex items-center justify-between text-[11px]">
                        <span class="text-emerald-400 font-medium">${exp.status}</span>
                        <span class="text-slate-500">${exp.vessel}</span>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    } catch (err) {
        console.error("Error loading expeditions:", err);
    }
}

// ----------------- KNOWLEDGE REPOSITORY ----------------- //
let searchDebounceTimeout = null;
function debounceSearch() {
    clearTimeout(searchDebounceTimeout);
    searchDebounceTimeout = setTimeout(loadRepository, 300);
}

function filterRepositoryByStation(stationId) {
    switchTab('repository');
    const filter = document.getElementById('repo-station-filter');
    if (filter) {
        filter.value = stationId;
        loadRepository();
    }
}

async function loadRepository() {
    const search = document.getElementById('repo-search-input')?.value || '';
    const category = document.getElementById('repo-category-filter')?.value || 'all';
    const station = document.getElementById('repo-station-filter')?.value || 'all';

    try {
        const res = await fetch(`/api/repository?category=${category}&station=${station}&search=${encodeURIComponent(search)}`);
        const items = await res.json();
        const container = document.getElementById('repository-container');
        const countSpan = document.getElementById('repo-item-count');
        const dlSpan = document.getElementById('repo-download-count');

        if (countSpan) countSpan.textContent = items.length;
        if (dlSpan) {
            const totalDl = items.reduce((acc, curr) => acc + (curr.downloads_count || 0), 0);
            dlSpan.textContent = totalDl.toLocaleString();
        }

        if (!container) return;

        if (items.length === 0) {
            container.innerHTML = `
                <div class="col-span-full py-12 text-center text-slate-400">
                    <i class="fa-solid fa-folder-open text-3xl mb-2 text-slate-600 block"></i>
                    No repository items matched your filters.
                </div>
            `;
            return;
        }

        let html = '';
        items.forEach(item => {
            const catBadge = item.category === 'dataset' ? 
                '<span class="px-2 py-0.5 rounded bg-cyan-950 border border-cyan-500/40 text-cyan-300 text-[10px] font-semibold uppercase">Dataset</span>' :
                (item.category === 'report' ? 
                    '<span class="px-2 py-0.5 rounded bg-blue-950 border border-blue-500/40 text-blue-300 text-[10px] font-semibold uppercase">Field Report</span>' :
                    '<span class="px-2 py-0.5 rounded bg-purple-950 border border-purple-500/40 text-purple-300 text-[10px] font-semibold uppercase">Publication</span>'
                );

            const tagsHtml = item.tags.split(',').map(t => `<span class="text-[10px] bg-black/40 px-2 py-0.5 rounded border border-slate-700/60 text-slate-300">${t.trim()}</span>`).join(' ');

            html += `
                <div class="bg-[#051120] rounded-xl border border-slate-800 p-5 flex flex-col justify-between hover:border-cyan-500/40 transition-all shadow-md">
                    <div>
                        <div class="flex items-center justify-between gap-2 mb-2">
                            ${catBadge}
                            <span class="text-xs font-mono text-slate-400">${item.year} | ${item.station_id.toUpperCase()}</span>
                        </div>
                        <h4 class="text-sm sm:text-base font-tech font-bold text-white mb-1.5 leading-snug">${item.title}</h4>
                        <p class="text-xs text-cyan-300/80 mb-2">${item.discipline} • <span class="text-slate-400">${item.author}</span></p>
                        <p class="text-xs text-slate-300 line-clamp-3 leading-relaxed mb-3">${item.summary}</p>
                        <div class="flex flex-wrap gap-1 mb-3">${tagsHtml}</div>
                    </div>

                    <div class="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                        <div class="text-slate-400 text-[11px]">
                            <span><i class="fa-solid fa-download text-slate-500"></i> ${item.downloads_count}</span>
                            <span class="mx-1">•</span>
                            <span>${item.file_size}</span>
                        </div>
                        <div class="flex items-center gap-2">
                            ${item.has_chart ? `
                                <button onclick="openChartModal('${item.id}')" class="px-2.5 py-1 rounded bg-cyan-900/60 hover:bg-cyan-800 text-cyan-200 border border-cyan-500/30 text-xs font-medium flex items-center gap-1">
                                    <i class="fa-solid fa-chart-line"></i> Visualize
                                </button>
                            ` : ''}
                            <button onclick="sendToAIEngine('${item.id}', \`${encodeURIComponent(item.title)}\`, \`${encodeURIComponent(item.summary)}\`, '${item.station_id}')" class="px-2.5 py-1 rounded bg-purple-900/60 hover:bg-purple-800 text-purple-200 border border-purple-500/30 text-xs font-medium flex items-center gap-1">
                                <i class="fa-solid fa-wand-magic-sparkles"></i> AI Outreach
                            </button>
                            <a href="/api/repository/download/${item.id}" target="_blank" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-white text-xs font-medium flex items-center gap-1">
                                <i class="fa-solid fa-file-arrow-down"></i> Download
                            </a>
                        </div>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    } catch (err) {
        console.error("Error loading repository:", err);
    }
}

// ----------------- IN-BROWSER CHART VISUALIZER ----------------- //
async function openChartModal(itemId) {
    currentModalDatasetId = itemId;
    try {
        const res = await fetch(`/api/repository/${itemId}`);
        const item = await res.json();

        document.getElementById('chart-modal-category').textContent = item.discipline;
        document.getElementById('chart-modal-title').textContent = item.title;
        document.getElementById('chart-modal-doi').textContent = `DOI: ${item.doi || 'NCPOR-DATA-' + item.id} | Author: ${item.author}`;
        document.getElementById('chart-modal-source').textContent = `Archived at: ${item.station_id.toUpperCase()} Base | Downloads: ${item.downloads_count}`;

        const modal = document.getElementById('chart-modal');
        modal.classList.remove('hidden');

        // Render Chart.js
        if (item.chart_data) {
            renderChart(item.chart_data);
        }
    } catch (err) {
        console.error("Error loading chart data:", err);
    }
}

function closeChartModal() {
    const modal = document.getElementById('chart-modal');
    modal.classList.add('hidden');
    if (currentChartInstance) {
        currentChartInstance.destroy();
        currentChartInstance = null;
    }
}

function renderChart(chartData) {
    const ctx = document.getElementById('dataset-chart-canvas').getContext('2d');
    if (currentChartInstance) {
        currentChartInstance.destroy();
    }

    currentChartInstance = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
                },
                tooltip: {
                    backgroundColor: '#0a1d37',
                    titleColor: '#38bdf8',
                    bodyColor: '#f1f5f9',
                    borderColor: '#0284c7',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#64748b', font: { family: 'Rajdhani', size: 12 } }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#64748b', font: { family: 'Rajdhani', size: 12 } }
                }
            }
        }
    });
}

function downloadCurrentDataset() {
    if (currentModalDatasetId) {
        window.open(`/api/repository/download/${currentModalDatasetId}`, '_blank');
    }
}

function triggerAIFromDatasetModal() {
    const title = document.getElementById('chart-modal-title').textContent;
    const summary = document.getElementById('chart-modal-doi').textContent;
    closeChartModal();
    sendToAIEngine(currentModalDatasetId, encodeURIComponent(title), encodeURIComponent(summary), 'bharati');
}

// ----------------- MULTIMEDIA GALLERY ----------------- //
async function loadMedia(filter = 'all') {
    try {
        let url = '/api/media';
        if (filter !== 'all') {
            if (['bharati', 'maitri', 'himadri', 'himansh'].includes(filter)) {
                url += `?station=${filter}`;
            } else {
                url += `?category=${filter}`;
            }
        }
        const res = await fetch(url);
        const data = await res.json();
        const container = document.getElementById('media-container');
        if (!container) return;

        let html = '';
        data.forEach(med => {
            html += `
                <div class="group relative rounded-xl overflow-hidden border border-slate-800 bg-[#051120] shadow-lg">
                    <img src="${med.media_url}" alt="${med.title}" class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent p-4 flex flex-col justify-end">
                        <span class="text-[10px] text-cyan-300 font-mono mb-1 uppercase tracking-wider">${med.station_id} Base • ${med.date_taken}</span>
                        <h4 class="text-xs font-semibold text-white leading-tight">${med.title}</h4>
                        <p class="text-[11px] text-slate-300 line-clamp-2 mt-1">${med.caption}</p>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    } catch (err) {
        console.error("Error loading media:", err);
    }
}

function filterMedia(type) {
    loadMedia(type);
}

// ----------------- AI MEDIA & CONTENT DISSEMINATION ENGINE ----------------- //
function loadPresetText() {
    const picker = document.getElementById('ai-preset-picker');
    const selected = picker.value;
    if (!selected || !AI_PRESETS[selected]) return;

    const preset = AI_PRESETS[selected];
    document.getElementById('ai-input-title').value = preset.title;
    document.getElementById('ai-input-text').value = preset.text;
    document.getElementById('ai-input-station').value = preset.station;
}

function sendToAIEngine(id, encodedTitle, encodedText, station) {
    switchTab('ai-engine');
    document.getElementById('ai-input-title').value = decodeURIComponent(encodedTitle);
    document.getElementById('ai-input-text').value = decodeURIComponent(encodedText);
    document.getElementById('ai-input-station').value = station || 'bharati';
    triggerAIGeneration(id);
}

async function triggerAIGeneration(sourceId = 'custom-user') {
    const title = document.getElementById('ai-input-title').value.trim();
    const text = document.getElementById('ai-input-text').value.trim();
    const station = document.getElementById('ai-input-station').value;
    const btn = document.getElementById('ai-generate-btn');

    if (!title && !text) {
        alert("Please provide either a research title or field text to generate content.");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Synthesizing Polar Dispatches...`;

    try {
        const res = await fetch('/api/generate-content', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                source_id: sourceId,
                title: title,
                text: text,
                station: station
            })
        });

        currentAIGenerated = await res.json();
        document.getElementById('ai-hashtags-preview').textContent = currentAIGenerated.hashtags;
        renderCurrentAIOutput();
        loadDisseminations();
    } catch (err) {
        console.error("Error generating content:", err);
        alert("Failed to generate content: " + err.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-sparkles"></i> Synthesize Multi-Platform Outreach Content`;
    }
}

function switchAIPlatform(platform) {
    currentAIPlatform = platform;
    document.querySelectorAll('.ai-platform-tab').forEach(b => b.classList.remove('active-platform'));
    const btn = document.getElementById(`ai-tab-${platform}`);
    if (btn) btn.classList.add('active-platform');
    renderCurrentAIOutput();
}

function renderCurrentAIOutput() {
    const container = document.getElementById('ai-output-container');
    if (!currentAIGenerated || !currentAIGenerated.outputs) {
        container.textContent = "Select a preset or enter research details and click Synthesize.";
        return;
    }

    const content = currentAIGenerated.outputs[currentAIPlatform] || "No content generated for this platform.";
    container.textContent = content;
}

function copyCurrentAICopy() {
    const container = document.getElementById('ai-output-container');
    const text = container.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const btnText = document.getElementById('copy-btn-text');
        btnText.textContent = "Copied!";
        setTimeout(() => { btnText.textContent = "Copy"; }, 2000);
    });
}

async function publishToQueue() {
    if (!currentAIGenerated) {
        alert("Please generate content first.");
        return;
    }
    alert("Outreach dispatch successfully approved and queued for MoES & NCPOR official broadcast!");
    loadDisseminations();
}

async function loadDisseminations() {
    try {
        const res = await fetch('/api/disseminations');
        const items = await res.json();
        const container = document.getElementById('disseminations-list');
        if (!container) return;

        let html = '';
        items.forEach(d => {
            const platformIcon = d.platform === 'twitter' ? '<i class="fa-brands fa-x-twitter text-slate-300"></i>' :
                (d.platform === 'linkedin' ? '<i class="fa-brands fa-linkedin text-blue-400"></i>' :
                (d.platform === 'instagram' ? '<i class="fa-brands fa-instagram text-pink-400"></i>' :
                (d.platform === 'press_release' ? '<i class="fa-solid fa-newspaper text-amber-400"></i>' :
                '<i class="fa-solid fa-graduation-cap text-emerald-400"></i>')));

            html += `
                <div class="bg-[#051120] rounded-xl border border-slate-800 p-4 text-xs flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="flex items-center gap-1.5 font-semibold text-white uppercase text-[10px]">
                                ${platformIcon} ${d.platform.replace('_', ' ')}
                            </span>
                            <span class="px-2 py-0.5 rounded text-[10px] ${d.status === 'published' ? 'bg-emerald-950 text-emerald-300 border border-emerald-500/30' : 'bg-amber-950 text-amber-300 border border-amber-500/30'}">
                                ${d.status}
                            </span>
                        </div>
                        <h4 class="font-bold text-slate-200 mb-1 line-clamp-1">${d.source_title}</h4>
                        <p class="text-slate-400 line-clamp-3 leading-relaxed mb-2 font-mono text-[11px]">${d.content}</p>
                    </div>
                    <div class="pt-2 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-500">
                        <span><i class="fa-solid fa-eye"></i> ${d.clicks || 120} views</span>
                        <span>${d.created_at || 'Just now'}</span>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    } catch (err) {
        console.error("Error loading disseminations:", err);
    }
}

function triggerTeleconnectionTweet() {
    switchTab('ai-engine');
    document.getElementById('ai-preset-picker').value = 'arctic_monsoon';
    loadPresetText();
    triggerAIGeneration();
}

// ----------------- SMART EDUCATION QUIZ ----------------- //
async function loadQuiz() {
    try {
        const res = await fetch('/api/quiz');
        quizQuestions = await res.json();
        currentQuestionIndex = 0;
        userAnswers = {};
        renderQuizQuestion();
    } catch (err) {
        console.error("Error loading quiz:", err);
    }
}

function renderQuizQuestion() {
    if (quizQuestions.length === 0) return;
    const q = quizQuestions[currentQuestionIndex];

    document.getElementById('quiz-progress-text').textContent = `Question ${currentQuestionIndex + 1} of ${quizQuestions.length}`;
    document.getElementById('quiz-question-title').textContent = q.question;

    const optContainer = document.getElementById('quiz-options-container');
    const feedbackBox = document.getElementById('quiz-feedback-box');
    feedbackBox.classList.add('hidden');

    let html = '';
    q.options.forEach((opt, idx) => {
        const isSelected = userAnswers[q.id] === idx;
        html += `
            <button onclick="selectQuizOption(${q.id}, ${idx})" class="w-full text-left p-3 rounded-lg border ${isSelected ? 'border-cyan-400 bg-cyan-950/40 text-cyan-200' : 'border-slate-800 bg-[#051120] text-slate-300 hover:border-slate-700'} text-xs flex items-center gap-3 transition-colors">
                <span class="w-6 h-6 rounded-full border border-slate-700 flex items-center justify-center font-mono text-[11px] ${isSelected ? 'bg-cyan-500 text-black font-bold' : ''}">
                    ${String.fromCharCode(65 + idx)}
                </span>
                <span>${opt}</span>
            </button>
        `;
    });
    optContainer.innerHTML = html;

    const nextBtn = document.getElementById('quiz-next-btn');
    if (currentQuestionIndex === quizQuestions.length - 1) {
        nextBtn.innerHTML = `<span>Submit & Get Certificate</span> <i class="fa-solid fa-award"></i>`;
    } else {
        nextBtn.innerHTML = `<span>Next Question</span> <i class="fa-solid fa-arrow-right"></i>`;
    }
}

function selectQuizOption(questionId, optionIndex) {
    userAnswers[questionId] = optionIndex;
    renderQuizQuestion();
}

async function nextQuizQuestion() {
    const q = quizQuestions[currentQuestionIndex];
    if (userAnswers[q.id] === undefined) {
        alert("Please select an answer before continuing.");
        return;
    }

    if (currentQuestionIndex < quizQuestions.length - 1) {
        currentQuestionIndex++;
        renderQuizQuestion();
    } else {
        // Submit quiz
        const studentName = prompt("Enter your name for the official MoES-NCPOR Young Polar Explorer Certificate:", "Young Polar Scientist") || "Young Polar Scientist";
        try {
            const res = await fetch('/api/quiz/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: studentName,
                    answers: userAnswers
                })
            });
            const result = await res.json();

            // Trigger confetti
            if (typeof confetti === 'function') {
                confetti({
                    particleCount: 100,
                    spread: 70,
                    origin: { y: 0.6 }
                });
            }

            // Display certificate modal
            document.getElementById('cert-student-name').textContent = result.certificate.name;
            document.getElementById('cert-score-text').textContent = `${result.percentage}% (${result.score}/${result.total} Correct)`;
            document.getElementById('cert-badge-text').textContent = result.certificate.badge;
            document.getElementById('cert-id-text').textContent = result.certificate.id;
            document.getElementById('cert-date-text').textContent = result.certificate.date;

            document.getElementById('certificate-modal').classList.remove('hidden');
        } catch (err) {
            console.error("Error submitting quiz:", err);
        }
    }
}

function resetQuiz() {
    userAnswers = {};
    currentQuestionIndex = 0;
    renderQuizQuestion();
}

function closeCertificateModal() {
    document.getElementById('certificate-modal').classList.add('hidden');
}

// Interactive Albedo Simulator
function updateAlbedoSim(val) {
    const reflected = parseInt(val);
    const absorbed = 100 - reflected;

    document.getElementById('albedo-ice-percent').textContent = `${reflected}%`;
    document.getElementById('albedo-reflected').textContent = `${reflected}%`;
    document.getElementById('albedo-absorbed').textContent = `${absorbed}%`;

    const expText = document.getElementById('albedo-explanation');
    if (reflected > 70) {
        expText.textContent = "High snow and sea-ice cover reflects over 80% of solar radiation, stabilizing polar temperatures and planetary currents.";
    } else if (reflected > 40) {
        expText.textContent = "Moderate melting exposes darker ocean and tundra, accelerating absorption of heat (albedo feedback loop).";
    } else {
        expText.textContent = "Critical Arctic/Antarctic ice depletion: 70%+ of solar energy is absorbed by dark open water, driving rapid planetary warming!";
    }
}

// ----------------- RESEARCHER / ADMIN CONSOLE ----------------- //
async function loadAdminMetrics() {
    try {
        const res = await fetch('/api/analytics');
        const data = await res.json();
        const grid = document.getElementById('admin-metrics-grid');
        if (!grid) return;

        grid.innerHTML = `
            <div class="bg-[#051120] p-4 rounded-xl border border-slate-800">
                <span class="text-slate-400 text-xs block">Active Polar Bases</span>
                <b class="text-xl font-tech text-white">${data.active_stations}</b>
                <span class="text-[10px] text-emerald-400 block mt-1">Antarctica, Arctic, Himalayas</span>
            </div>
            <div class="bg-[#051120] p-4 rounded-xl border border-slate-800">
                <span class="text-slate-400 text-xs block">Archived Datasets</span>
                <b class="text-xl font-tech text-cyan-300">${data.datasets_count}</b>
                <span class="text-[10px] text-slate-500 block mt-1">NetCDF / CSV / GeoTIFF</span>
            </div>
            <div class="bg-[#051120] p-4 rounded-xl border border-slate-800">
                <span class="text-slate-400 text-xs block">Scientific Publications</span>
                <b class="text-xl font-tech text-purple-300">${data.publications_count + data.reports_count}</b>
                <span class="text-[10px] text-slate-500 block mt-1">Peer-reviewed & Reports</span>
            </div>
            <div class="bg-[#051120] p-4 rounded-xl border border-slate-800">
                <span class="text-slate-400 text-xs block">Total Outreach Downloads</span>
                <b class="text-xl font-tech text-emerald-300">${data.total_downloads.toLocaleString()}</b>
                <span class="text-[10px] text-emerald-400 block mt-1">Global researchers & students</span>
            </div>
        `;
    } catch (err) {
        console.error("Error loading metrics:", err);
    }
}

// Upload Artifact Modal handlers
function openUploadModal() {
    document.getElementById('upload-modal').classList.remove('hidden');
}

function closeUploadModal() {
    document.getElementById('upload-modal').classList.add('hidden');
}

async function handleArtifactUpload(event) {
    event.preventDefault();
    const btn = document.getElementById('upload-submit-btn');
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Archiving...`;

    const title = document.getElementById('upload-title').value;
    const category = document.getElementById('upload-category').value;
    const station = document.getElementById('upload-station').value;
    const discipline = document.getElementById('upload-discipline').value;
    const author = document.getElementById('upload-author').value;
    const summary = document.getElementById('upload-summary').value;

    try {
        const res = await fetch('/api/upload', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                category: category,
                station_id: station,
                discipline: discipline,
                author: author,
                summary: summary
            })
        });

        const data = await res.json();
        closeUploadModal();
        alert(`Artifact archived successfully with DOI: ${data.doi}! AI Social Media drafts have been generated.`);
        
        // Refresh views and jump to AI tab to show results
        loadRepository();
        loadAdminMetrics();
        currentAIGenerated = data.ai_content;
        switchTab('ai-engine');
        renderCurrentAIOutput();
    } catch (err) {
        alert("Upload error: " + err.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-check"></i> Deposit & Generate Outreach`;
    }
}

// ----------------- ASK A POLAR SCIENTIST (DR. HIMAVANI) CHATBOT ----------------- //
let chatHistory = [];
let voiceSpeechEnabled = false;

function toggleChatDrawer() {
    const drawer = document.getElementById('chat-drawer');
    const isHidden = drawer.classList.contains('hidden');
    if (isHidden) {
        drawer.classList.remove('hidden');
        document.getElementById('chat-input-field')?.focus();
    } else {
        drawer.classList.add('hidden');
    }
}

function openChatDrawer() {
    const drawer = document.getElementById('chat-drawer');
    drawer.classList.remove('hidden');
    document.getElementById('chat-input-field')?.focus();
}

function toggleVoiceSpeech() {
    voiceSpeechEnabled = !voiceSpeechEnabled;
    const btn = document.getElementById('voice-toggle-btn');
    const icon = document.getElementById('voice-icon');
    if (voiceSpeechEnabled) {
        btn.classList.add('text-cyan-400', 'bg-cyan-950/60');
        icon.className = 'fa-solid fa-volume-high text-cyan-400 animate-pulse';
        speakText("Voice response enabled. I am listening!");
    } else {
        btn.classList.remove('text-cyan-400', 'bg-cyan-950/60');
        icon.className = 'fa-solid fa-volume-xmark text-slate-400';
        if (window.speechSynthesis) window.speechSynthesis.cancel();
    }
}

function speakText(text) {
    if (!voiceSpeechEnabled || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    // Clean emojis and markdown formatting for speech
    const cleanText = text.replace(/[*#_~`]/g, '').replace(/[^\x00-\x7F]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
}

function handleSendChatMessage(event) {
    event.preventDefault();
    const input = document.getElementById('chat-input-field');
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    sendChatMessage(text);
}

function sendQuickQuestion(questionText) {
    sendChatMessage(questionText);
}

async function sendChatMessage(text) {
    const container = document.getElementById('chat-messages-container');
    const sendBtn = document.getElementById('chat-send-btn');

    // Append User Bubble
    appendChatBubble("You", text, true);

    // Append Typing Indicator
    const typingId = 'typing-' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.id = typingId;
    typingDiv.className = 'flex items-start gap-2';
    typingDiv.innerHTML = `
        <div class="w-6 h-6 rounded-lg bg-blue-500/20 border border-blue-400/40 flex items-center justify-center text-blue-300 text-[10px] shrink-0 mt-0.5">
            <i class="fa-solid fa-building-columns"></i>
        </div>
        <div class="bg-[#0f172a] border border-slate-700 rounded-xl p-3 text-slate-400 text-xs italic flex items-center gap-1.5 shadow">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce"></span>
            <span class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce [animation-delay:0.2s]"></span>
            <span class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce [animation-delay:0.4s]"></span>
            <span class="ml-1 text-[11px]">Consulting NCPOR Polar Research Database...</span>
        </div>
    `;
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;

    sendBtn.disabled = true;

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                history: chatHistory
            })
        });

        const data = await res.json();
        // Remove typing indicator
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();

        // Append Bot Bubble
        appendChatBubble(data.speaker, data.reply, false);

        // Update suggestions bar if available
        if (data.suggested_questions && data.suggested_questions.length > 0) {
            renderChatSuggestions(data.suggested_questions);
        }

        // Voice Read-Aloud
        if (voiceSpeechEnabled) {
            speakText(data.reply);
        }

        // Record history
        chatHistory.push({ role: 'user', content: text });
        chatHistory.push({ role: 'assistant', content: data.reply });

    } catch (err) {
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();
        appendChatBubble("NCPOR Information Desk", "The inquiry service is temporarily reconnecting to the polar observation database. Please retry momentarily.", false);
    } finally {
        sendBtn.disabled = false;
        container.scrollTop = container.scrollHeight;
    }
}

function appendChatBubble(sender, text, isUser) {
    const container = document.getElementById('chat-messages-container');
    const div = document.createElement('div');
    div.className = isUser ? 'flex items-start justify-end gap-2' : 'flex items-start gap-2';

    if (isUser) {
        div.innerHTML = `
            <div class="bg-blue-600 rounded-xl rounded-tr-none p-3 text-white max-w-[85%] shadow-sm text-xs">
                ${text}
            </div>
            <div class="w-6 h-6 rounded-lg bg-slate-700 border border-slate-600 flex items-center justify-center text-slate-300 text-[10px] shrink-0 mt-0.5">
                <i class="fa-solid fa-user"></i>
            </div>
        `;
    } else {
        div.innerHTML = `
            <div class="w-6 h-6 rounded-lg bg-blue-900/50 border border-blue-500/40 flex items-center justify-center text-blue-300 text-[10px] shrink-0 mt-0.5">
                <i class="fa-solid fa-building-columns"></i>
            </div>
            <div class="bg-[#0f172a] border border-slate-700/80 rounded-xl rounded-tl-none p-3 text-slate-200 max-w-[85%] shadow-sm leading-relaxed text-xs">
                ${text}
            </div>
        `;
    }

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function renderChatSuggestions(suggestions) {
    const bar = document.getElementById('chat-suggestions-bar');
    if (!bar) return;
    let html = '';
    suggestions.slice(0, 4).forEach(q => {
        html += `
            <button onclick="sendQuickQuestion(\`${q.replace(/`/g, '\\`')}\`)" class="whitespace-nowrap px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 hover:text-white shrink-0 transition-colors text-[11px]">
                ${q}
            </button>
        `;
    });
    bar.innerHTML = html;
}

