@echo off
chcp 65001 >nul
echo 正在编译mesh_inpaint_processor模块（修复版本）...

:: 设置Python环境路径
set PYTHON_PATH=C:\Users\admin\.conda\envs\hunyuan3D\python.exe
echo 使用Python环境: %PYTHON_PATH%

:: 验证Python环境
"%PYTHON_PATH%" --version
if %errorlevel% neq 0 (
    echo 错误：找不到指定的Python环境
    pause
    exit /b 1
)

:: 检查依赖
echo 检查依赖...
"%PYTHON_PATH%" -c "import pybind11, numpy; print('依赖检查通过')"
if %errorlevel% neq 0 (
    echo 安装依赖...
    "%PYTHON_PATH%" -m pip install pybind11 numpy setuptools
)

:: 清理之前的构建文件
echo 清理构建文件...
if exist build rmdir /s /q build
if exist mesh_inpaint_processor.*.pyd del mesh_inpaint_processor.*.pyd
if exist mesh_inpaint_processor.egg-info rmdir /s /q mesh_inpaint_processor.egg-info

:: 设置编译环境变量
set PYTHONIOENCODING=utf-8
set LANG=en_US.UTF-8

:: 编译模块
echo 开始编译...
"%PYTHON_PATH%" setup.py build_ext --inplace

if %errorlevel% equ 0 (
    echo ✅ 编译成功！
    :: 查找生成的.pyd文件
    for %%f in (mesh_inpaint_processor.*.pyd) do (
        echo 生成文件: %%f
    )
    echo.
    echo 测试模块导入...
    "%PYTHON_PATH%" -c "import mesh_inpaint_processor; print('✅ 模块导入成功!')"
    if %errorlevel% equ 0 (
        echo.
        echo 🎉 编译和测试都成功完成！
    ) else (
        echo ❌ 模块导入失败
    )
) else (
    echo ❌ 编译失败！
    pause
    exit /b 1
)

echo.
echo 按任意键退出...
pause >nul 