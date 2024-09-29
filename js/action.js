//判断是否在用电脑或手机浏览，如果用电脑浏览，则使用“style_from_computer.css”；如果用手机浏览，则使用“style_from_phone.css”，这两个文件里的修饰大不相同。
document.addEventListener('DOMContentLoaded', function() {
	const themeStylesheet = document.getElementById('default_style');
	// 判断是否用手机还是电脑浏览的屏幕宽度阈值为600像素
	const mq = window.matchMedia("(max-width: 600px)");
	mq.addListener(function(e) {
		if (e.matches) {
			themeStylesheet.href = 'css/style_from_phone.css';
		} else {
			themeStylesheet.href = 'css/style_from_computer.css';
		}
	});
	mq.matches ? themeStylesheet.href = 'css/style_from_phone.css' : themeStylesheet.href =
		'css/style_from_computer.css';
});
// 用于录音按键的互动:如果点击,将会平滑展开,并显示"开始录音"四个字,再点一下将会复原
function toggleButton() {  
    console.log('Button clicked!');  
    const button = document.getElementById('recordButton');  
    const recorderImg = document.getElementById('recorder');  
  
    button.classList.toggle('expanded');  
    console.log('Expanded class:', button.classList.contains('expanded'));  
  
    if (button.classList.contains('expanded')) {  
        recorderImg.src = "img/record_on.png";  
        console.log('Image changed to record_on.png');  
    } else {  
        recorderImg.src = "img/record_off.png";  
        console.log('Image changed to record_off.png');  
    }  
}