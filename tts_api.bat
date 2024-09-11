::使用gk18030打开
@echo off  
setlocal  
set CONDA_ENV_NAME=allium  
call conda activate %CONDA_ENV_NAME% 
echo 启动程序中.....
echo 正在启动声带...
start cmd /k python tools/fish_speech_1_2/tools/api.py --llama-checkpoint-path models/checkpoints/fish-speech-1.2-sft --decoder-checkpoint-path models/checkpoints/fish-speech-1.2-sft/firefly-gan-vq-fsq-4x1024-42hz-generator.pth
echo Python 程序正在运行中的两个黑窗口不要关闭，此窗口可关闭。
echo （按任意键退出）聊的愉快Ciallo～ （∠・ω< ）⌒★
:End  
endlocal  
pause
