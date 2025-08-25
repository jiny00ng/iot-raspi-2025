const tempCtx = document.getElementById('tempChart').getContext('2d');
const humiCtx = document.getElementById('humiChart').getContext('2d');
const alertDiv = document.getElementById('alert-message');

// 🌙 현재 다크모드 여부를 판단하는 함수
function isDarkMode() {
    return document.body.classList.contains("dark-mode");
}

// 🌙 다크모드에 따라 축/글자 색상 설정
function getChartOptions(yLabel) {
    const isDark = isDarkMode();
    const fontColor = isDark ? '#ffffff' : '#000000';

     return {
        scales: {
            y: {
                min: yLabel.includes('온도') ? 10 : 5,
                suggestedMax: yLabel.includes('온도') ? 45 : 40,
                ticks: { font: { size: 16 }, color: fontColor },
                title: { display: true, text: yLabel, font: { size: 18 }, color: fontColor }
            },
            x: {
                ticks: { font: { size: 14 }, color: fontColor },
                title: { display: true, text: '시간', font: { size: 16 }, color: fontColor }
            }
        },
        plugins: {
            legend: { labels: { font: { size: 18 }, color: fontColor } },
            tooltip: { bodyFont: { size: 16 }, titleFont: { size: 18 } }
        },
        animation: false
    };
}


// 🌡️ 온도 차트 생성
const tempChart = new Chart(tempCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: '온도 (°C)', data: [], borderColor: 'rgba(255,99,132,1)', backgroundColor: 'rgba(255,99,132,0.2)', tension: 0.4, fill: true, pointRadius: 3 }] },
    options: getChartOptions('온도 (°C)')
});

// 💧 습도 차트 생성
const humiChart = new Chart(humiCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: '습도 (%)', data: [], borderColor: 'rgba(54,162,235,1)', backgroundColor: 'rgba(54,162,235,0.2)', tension: 0.4, fill: true, pointRadius: 3 }] },
    options: getChartOptions('습도 (%)')
});

// 📥 센서 데이터 가져오기 + 팬 상태 표시
async function fetchSensorData() {
    try {
        const res = await fetch('/data');
        const data = await res.json();

        const times = data.map(d => d.time);
        const temps = data.map(d => d.temperature);
        const humis = data.map(d => d.humidity);

        tempChart.data.labels = times;
        tempChart.data.datasets[0].data = temps;
        tempChart.options = getChartOptions('온도 (°C)');
        tempChart.update();

        humiChart.data.labels = times;
        humiChart.data.datasets[0].data = humis;
        humiChart.options = getChartOptions('습도 (%)');
        humiChart.update();

        if (data.length) {
            const last = data[data.length - 1] || {};
            const isAlert = last.alert === 1; // last.alert가 정확히 1일 때만 true
            const isFanOn = last.fan === 1;   // last.fan이 정확히 1일 때만 true
            // 경보 메시지
            let msg = last.alert ? "⚠️ 온도 또는 습도 임계치 초과!" : "✅ 정상";
            // 팬 상태 추가
            msg += last.fan ? " 💨 팬 작동 중" : " 💨 팬 정지";
            alertDiv.textContent = msg;
            alertDiv.style.color = last.alert ? 'red' : 'green';
            console.log("Applied color:", alertDiv.style.color);

            // 콘솔 확인용
            console.log("Latest data:", last, "Alert:", isAlert, "Fan:", isFanOn);
        }
    } catch (error) {
        console.error('데이터 가져오기 실패:', error);
        alertDiv.textContent = "데이터 가져오기 실패";
        alertDiv.style.color = 'red';
    }
}

// ⏱️ 5초마다 데이터 자동 갱신
fetchSensorData();
setInterval(fetchSensorData, 5000);

// 🌙 다크모드 토글 시 차트 갱신 함수 (HTML에서 호출됨)
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("dark-mode", document.body.classList.contains("dark-mode"));

    // 차트 색상 갱신
    tempChart.options = getChartOptions('온도 (°C)');
    humiChart.options = getChartOptions('습도 (%)');
    tempChart.update();
    humiChart.update();
}
