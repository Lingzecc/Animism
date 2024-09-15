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
      window.model = model;
      app.stage.addChild(window.model);
      const scaleX = (window.innerWidth * 1) / window.model.width;
      const scaleY = (window.innerHeight * 2.5) / window.model.height;

      // 模型大小
      window.model.scale.set(Math.min(scaleX, scaleY));
      //模型位置坐标
      window.model.y = innerHeight * 0.01;
      window.model.x = innerWidth * 0.125;
      // 口型大小定义
      window.setMouthOpenY = v => {
        v = Math.max(0, Math.min(1, v));
        window.model.internalModel.coreModel.setParameterValueById('ParamMouthOpenY', v);
      }
    });

  })();