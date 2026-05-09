const quotes = [
    { en: "The only way to do great work is to love what you do.", ko: "위대한 일을 하는 유일한 방법은 당신이 하는 일을 사랑하는 것입니다." },
    { en: "Believe you can and you're halfway there.", ko: "할 수 있다고 믿으세요. 그러면 이미 절반은 온 것입니다." },
    { en: "Your time is limited, so don't waste it living someone else's life.", ko: "당신의 시간은 한정되어 있습니다. 다른 사람의 삶을 사느라 낭비하지 마세요." },
    { en: "Innovation distinguishes between a leader and a follower.", ko: "혁신이 리더와 추종자를 구분합니다." },
    { en: "Stay hungry, stay foolish.", ko: "늘 갈망하고, 늘 우직하게 나아가세요." },
    { en: "The best way to predict the future is to create it.", ko: "미래를 예측하는 가장 좋은 방법은 미래를 직접 만드는 것입니다." },
    { en: "Success is not final, failure is not fatal: it is the courage to continue that counts.", ko: "성공은 끝이 아니며 실패는 치명적이지 않습니다. 중요한 것은 계속하려는 용기입니다." },
    { en: "Don't be afraid to give up the good to go for the great.", ko: "더 위대한 것을 위해 좋은 것을 포기하는 것을 두려워하지 마세요." },
    { en: "I find that the harder I work, the more luck I seem to have.", ko: "열심히 일할수록 더 많은 행운이 따르는 것 같습니다." },
    { en: "Opportunities don't happen. You create them.", ko: "기회는 일어나는 것이 아니라 만드는 것입니다." },
    { en: "Try not to become a man of success, but rather try to become a man of value.", ko: "성공한 사람이 되기보다 가치 있는 사람이 되려고 노력하세요." },
    { en: "Great minds discuss ideas; average minds discuss events; small minds discuss people.", ko: "위대한 마음은 아이디어를 논하고, 평범한 마음은 사건을 논하며, 좁은 마음은 사람을 논합니다." },
    { en: "A person who never made a mistake never tried anything new.", ko: "실수를 한 번도 하지 않은 사람은 새로운 것을 시도해 본 적이 없는 사람입니다." },
    { en: "Happiness is not something readymade. It comes from your own actions.", ko: "행복은 이미 만들어져 있는 것이 아닙니다. 당신의 행동에서 비롯됩니다." },
    { en: "The only limit to our realization of tomorrow will be our doubts of today.", ko: "내일의 실현을 가로막는 유일한 장애물은 오늘의 의심입니다." },
    { en: "What you get by achieving your goals is not as important as what you become by achieving your goals.", ko: "목표를 달성해서 얻는 것보다 목표를 달성하며 어떤 사람이 되느지가 더 중요합니다." },
    { en: "If you want to live a happy life, tie it to a goal, not to people or things.", ko: "행복한 삶을 살고 싶다면 사람이나 사물이 아닌 목표에 삶을 묶으세요." },
    { en: "The power of imagination makes us infinite.", ko: "상상력의 힘은 우리를 무한하게 만듭니다." },
    { en: "It is during our darkest moments that we must focus to see the light.", ko: "가장 어두운 순간에 빛을 보기 위해 집중해야 합니다." },
    { en: "Dream big and dare to fail.", ko: "큰 꿈을 꾸고 기꺼이 실패에 도전하세요." }
];

function displayRandomQuote() {
    const quoteElement = document.getElementById('quote-en');
    const translationElement = document.getElementById('quote-ko');
    const randomIndex = Math.floor(Math.random() * quotes.length);
    const selectedQuote = quotes[randomIndex];

    quoteElement.textContent = selectedQuote.en;
    translationElement.textContent = selectedQuote.ko;
}

async function loadNaverNews() {
    const wrapper = document.getElementById('naver-news');
    try {
        const response = await fetch('./data/news.json');
        if (!response.ok) throw new Error('News data not found');
        const data = await response.json();
        
        let html = `<div class="news-list">`;
        data.news.forEach(item => {
            html += `
                <a href="${item.link}" class="news-item" target="_blank">
                    <span class="news-title">${item.title}</span>
                </a>`;
        });
        html += `</div><div class="news-footer">Last updated: ${data.last_updated}</div>`;
        wrapper.innerHTML = html;
    } catch (error) {
        wrapper.innerHTML = `<div class="error-msg">뉴스를 불러올 수 없습니다.</div>`;
    }
}

async function loadBizinfo() {
    const wrapper = document.getElementById('bizinfo-news');
    try {
        const response = await fetch('./data/bizinfo.json');
        if (!response.ok) throw new Error('Bizinfo data not found');
        const data = await response.json();
        
        let html = `<div class="news-list">`;
        data.items.forEach(item => {
            html += `
                <a href="${item.link}" class="news-item" target="_blank">
                    <span class="news-title">${item.title}</span>
                    <span class="news-meta">신청기간: ${item.period}</span>
                </a>`;
        });
        html += `</div><div class="news-footer">Last updated: ${data.last_updated}</div>`;
        wrapper.innerHTML = html;
    } catch (error) {
        wrapper.innerHTML = `<div class="error-msg">지원사업 정보를 불러올 수 없습니다.</div>`;
    }
}

async function loadWeather() {
    const wrapper = document.getElementById('weather-info');
    try {
        const response = await fetch('./data/weather.json');
        if (!response.ok) throw new Error('Weather data not found');
        const data = await response.json();
        
        // 날씨 코드별 이모지
        const emojis = {
            0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
            45: "🌫️", 48: "🌫️", 51: "🌦️", 53: "🌦️", 55: "🌦️",
            61: "🌧️", 63: "🌧️", 65: "🌊", 71: "❄️", 73: "❄️", 75: "☃️",
            95: "⚡"
        };
        const emoji = emojis[data.code] || "🌡️";
        
        wrapper.innerHTML = `
            <div class="weather-content">
                <div class="weather-main">
                    <span class="weather-emoji">${emoji}</span>
                    <div class="weather-temp">
                        <span class="temp-val">${data.temp}</span><span class="temp-unit">°C</span>
                    </div>
                </div>
                <div class="weather-desc">${data.description}</div>
                <div class="outfit-box">
                    <div class="outfit-label">오늘의 추천 코디</div>
                    <div class="outfit-text">${data.outfit}</div>
                </div>
            </div>
            <div class="news-footer">Last updated: ${data.last_updated}</div>
        `;
    } catch (error) {
        wrapper.innerHTML = `<div class="error-msg">날씨 정보를 불러올 수 없습니다.</div>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    displayRandomQuote();
    loadNaverNews();
    loadBizinfo();
    loadWeather();
});
