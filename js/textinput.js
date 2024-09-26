function speak() {
	const text = document.getElementById('textarea').value;
	document.getElementById('textarea').value = '';
	fetch('/upload/tts', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: `text=${encodeURIComponent(text)}`
		})
		.then(response => {
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
}