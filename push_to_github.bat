@echo off
chcp 65001 >nul
echo ============================================
echo   Rocky 使用说明文档 - 部署到 GitHub Pages
echo ============================================
echo.
echo 准备工作：请先在浏览器中打开 https://github.com/new
echo 创建一个新仓库，例如名字叫 "rocky-doc" （公开/公开 Public）
echo 创建后不要勾选 "Add a README file"
echo.
pause

set /p REPO_URL="请输入你的仓库地址 (如 https://github.com/你的用户名/rocky-doc.git): "

if "%REPO_URL%"=="" (
    echo 没有输入地址，取消。
    pause
    exit /b
)

echo.
echo 正在添加远程仓库...
git remote add origin %REPO_URL%

echo 正在推送到 GitHub...
git branch -M main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo   推送成功！
    echo ============================================
    echo.
    echo 接下来在浏览器中打开：
    echo   %REPO_URL%/settings/pages
    echo 或者手动操作：
    echo   1. 进入你的 GitHub 仓库页面
    echo   2. 点击 Settings
    echo   3. 左侧菜单找到 Pages
    echo   4. Source 选择 "Deploy from a branch"
    echo   5. Branch 选择 "main" 目录选 "/ (root)"
    echo   6. 点击 Save
    echo.
    echo 1-2 分钟后，你的网站将在以下地址上线：
    echo   https://你的用户名.github.io/rocky-doc/
    echo.
) else (
    echo.
    echo 推送失败！请检查仓库地址是否正确，或是否已登录 GitHub。
    echo.
)

pause
