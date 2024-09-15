

// 皮套块
  // 将 PIXI 暴露到 window 上，这样插件就可以通过 window.PIXI.Ticker 来自动更新模型
  window.PIXI = PIXI;
  const live2d = PIXI.live2d;
  (async function main() {
    const app = new PIXI.Application({
      view: document.getElementById("canvas"),
      autoStart: true,
      resizeTo: window,
      backgroundColor: 0x333333
    });
    // 皮套路径
    const models = await Promise.all([
      live2d.Live2DModel.from("assets/ariu/ariu.model3.json")
    ]);

    models.forEach((model) => {
      app.stage.addChild(model);
      const scaleX = (window.innerWidth * 1) / model.width;
      const scaleY = (window.innerHeight * 2.5) / model.height;

      // 模型大小
      model.scale.set(Math.min(scaleX, scaleY));
      //模型位置坐标
      model.y = innerHeight * 0.01;
      model.x = innerWidth * 0.125;
      // 口型大小定义
      const setMouthOpenY = v => {
        v = Math.max(0, Math.min(1, v));
        model.internalModel.coreModel.setParameterValueById('ParamMouthOpenY', v);
      }


      // ajax异步——口型检测
      // 引用自https://juejin.cn/post/7242279345136861241
      setInterval(() => {
        $.ajax({
          type: "GET",
          url: "/api/mouth",
          dataType: 'json',
          success(data) {
            // 调用口型函数，7毫秒请求一次tmp.txt文件获取口型数值
            setMouthOpenY(parseFloat(audioElement))
          }
        });
      }, 7); // 每7毫秒检查一次


    });

  })();