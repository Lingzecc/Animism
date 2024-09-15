  // 录音块
  let mediaRecorder;
  let audioChunks = [];
  let isRecording = false;


  const startRecording = async () => {
    isRecording = true;
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = event => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/webm; codecs=opus" });
      const audioFormData = new FormData();
      audioFormData.append('audioFile', audioBlob, 'recorded_audio.webm');

      await fetch('/upload/audio', {
        method: 'POST',
        body: audioFormData,
      }).then(response => response.blob())
        .then(blob => {
          const url = URL.createObjectURL(blob);
          const audio = document.getElementById('audio');
          audio.src = url;
          audio.play();
          // 调用 /mouthY 路由  
          fetch('/mouthY', {
            method: 'POST'
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              // 处理响应，如果需要的话  
              console.log('Successfully called /mouthY');
            })
            .catch(error => console.error('There was a problem with your fetch operation:', error));
        });
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


  const startOrStopRecording = async () => {
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  };

  // 绑定按钮点击事件  
  document.getElementById('recordButton').addEventListener('click', startOrStopRecording);
