let audioContext;
var audioElement;
let analyser;
let frequencyData;
let bufferLength = 2048;

// 初始化Web Audio API  
function initAudioContext() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048;
    frequencyData = new Uint8Array(analyser.frequencyBinCount);
 
    audioElement = document.querySelector('audio');
    let source = audioContext.createMediaElementSource(audioElement);
    source.connect(analyser);
    analyser.connect(audioContext.destination);

    // 开始分析  
    setInterval(function () {
        analyser.getByteFrequencyData(frequencyData);
        // 这里你可以处理 frequencyData 数组  
        // 示例：找到最大频率  
        let maxIndex = 0;
        let maxValue = frequencyData[0];
        for (let i = 1; i < frequencyData.length; i++) {
            if (frequencyData[i] > maxValue) {
                maxValue = frequencyData[i];
                maxIndex = i;
            }
        }
        let frequency = (maxIndex * (audioContext.sampleRate / 2)) / bufferLength;
        console.log('Max Frequency:', frequency);
    }, 7); // 每100ms更新一次  
}

// 确保在音频加载完成后调用 initAudioContext  
audioElement.addEventListener('loadedmetadata', initAudioContext);