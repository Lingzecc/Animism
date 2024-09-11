::使用gk18030打开
@echo off  
setlocal  
set CONDA_ENV_NAME=allium  
call conda activate %CONDA_ENV_NAME% 
echo 启动程序中.....
echo 正在补妆...
echo 神秘通道：http://127.0.0.1:4800/
start cmd /k python "weblive2d.py"  
echo Python 程序正在运行中的两个黑窗口不要关闭，此窗口可关闭。
echo （按任意键退出）聊的愉快Ciallo～ （∠・ω< ）⌒★
:End  
endlocal  
pause