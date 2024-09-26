// 录音块
var mediaRecorder;
var audioChunks = [];
var isRecording = false;


const startRecording = async () => {
	isRecording = true;
	const stream = await navigator.mediaDevices.getUserMedia({
		audio: true
	});
	mediaRecorder = new MediaRecorder(stream);

	mediaRecorder.ondataavailable = event => {
		if (event.data.size > 0) {
			audioChunks.push(event.data);
		}
	};

	mediaRecorder.onstop = async () => {
		const audioBlob = new Blob(audioChunks, {
			type: "audio/webm; codecs=opus"
		});
		const audioFormData = new FormData();
		audioFormData.append('audioFile', audioBlob, 'recorded_audio.webm');

		await fetch('/upload/audio', {
				method: 'POST',
				body: audioFormData,
			}).then(response => {
				if (!response.ok) {
					throw new Error('Network response was not ok');
				}
				return response.blob();
			})
			.then(blob => {
				return new Promise((resolve, reject) => {
					const reader = new FileReader();
					reader.onload = function() {
						resolve(reader.result); // reader.result 是 ArrayBuffer  
					};
					reader.onerror = function(error) {
						reject(error);
					};
					reader.readAsArrayBuffer(blob);
				});
			})
			.then(arrayBuffer => {
				const audioContext = new(window.AudioContext || window.webkitAudioContext)();
				audioContext.decodeAudioData(arrayBuffer)
					.then(audioBuffer => {
						const source = audioContext.createBufferSource();
						source.buffer = audioBuffer;

						// 创建AnalyserNode  
						const analyser = audioContext.createAnalyser();
						analyser.fftSize = 2048;
						const bufferLength = analyser.frequencyBinCount;
						const dataArray = new Uint8Array(bufferLength);

						source.connect(analyser);
						analyser.connect(audioContext.destination);

						source.start();

						// 实时分析音频  
						function updateFrequency() {
							requestAnimationFrame(updateFrequency);
							analyser.getByteFrequencyData(dataArray);

							let maxValue = 0;

							// 遍历dataArray找到最大值  
							for (let i = 0; i < bufferLength; i++) {
								if (dataArray[i] > maxValue) {
									maxValue = dataArray[i];
								}
							}

							// 将平均频率映射到0到1的范围内  
							const frequencyRatio = maxValue / 255 * 0.65; // 假设255是最大频率值  
							window.setMouthOpenY(frequencyRatio);

						}

						updateFrequency();
					})
					.catch(error => console.error('Error decoding audio data:', error));
			})
			.catch(error => console.error('Error fetching audio:', error));
		// 清理资源  
		audioChunks = [];
		mediaRecorder.stream.getTracks().forEach(track => track.stop());
		mediaRecorder = null; // 可选：重置mediaRecorder为null  
		isRecording = false; // 更新录音状态  
	};

	mediaRecorder.start();
	console.log("录音开始");
};

const stopRecording = () => {
	mediaRecorder.stop();
	console.log("录音停止");
};
//点击开始录音并切换图片，点击结束录音并切换图片
let element = document.getElementById("recorder");
const startOrStopRecording = async () => {
	if (!isRecording) {
		element.src = "img/record_on.png";
		startRecording();

	} else {
		element.src = "img/record_off.png";
		stopRecording();
	}
};

// 绑定按钮点击事件  
document.getElementById('recordButton').addEventListener('click', startOrStopRecording);