@echo off  
setlocal  
  
:: 设置Conda环境和Python版本的变量  
set CONDA_ENV_NAME=allium  
set PYTHON_VERSION=3.10
  
:: 检查环境是否存在  
conda info --envs | findstr /b /c:"%CONDA_ENV_NAME% " >nul  
if %ERRORLEVEL% equ 0 (  
    echo 环境 '%CONDA_ENV_NAME%' 已存在，正在激活...  
    call conda activate %CONDA_ENV_NAME%  
    if %ERRORLEVEL% neq 0 (  
        echo 激活环境失败，请手动激活或检查Conda安装。  
        goto End  
    )  
    echo 激活成功，现在使用清华源安装依赖...  
    set PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple  
    pip install -r ./requirements.txt -i %PIP_INDEX_URL%  
    if %ERRORLEVEL% neq 0 (  
        echo 安装依赖失败，请检查requirements.txt和网络连接。  
        goto End  
    )  
    echo 依赖安装成功。  
    :: 注意：由于conda activate的影响，这里之后的命令可能仍在激活的环境中运行  
    :: 但批处理文件结束时，激活的环境通常会失效（除非你在新的shell中）  
) else (  
    echo 环境 '%CONDA_ENV_NAME%' 不存在，正在创建...  
    conda create --name %CONDA_ENV_NAME% python=%PYTHON_VERSION%  
    if %ERRORLEVEL% neq 0 (  
        echo 创建环境失败。  
        goto End  
    )  
    echo 环境创建成功，现在尝试激活并安装依赖...  
    call conda activate %CONDA_ENV_NAME%
    pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple  
)  
  
:End  
echo 脚本执行完毕。  
endlocal  
pause