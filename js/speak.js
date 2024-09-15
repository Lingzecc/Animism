  // 音频播放块
  function speak() {
    const text = document.getElementById('text').value;
    fetch('/upload/tts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `text=${encodeURIComponent(text)}`
    })
      .then(response => response.blob())
      .then(blob => {
        const url = URL.createObjectURL(blob);
        const audio = document.getElementById('audio');
        audio.src = url;
        // audio.play();
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
  }
