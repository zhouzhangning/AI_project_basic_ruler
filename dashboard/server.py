#!/usr/bin/env python3
"""dashboard/server.py — AI Dev System 本地 Web 服务

提供:
1. 静态文件服务 (dashboard/index.html)
2. API: GET  /api/status        — 合成状态快照
3. API: POST /api/run-script    — 运行校验脚本 (实时输出)
4. API: GET  /api/git-status    — Git 状态
5. API: GET  /api/data          — 完整 dashboard-data.json
6. API: GET  /api/health        — 服务健康检查

用法:
    python dashboard/server.py
    python dashboard/server.py --port 8765
    python dashboard/server.py --no-browser
"""

import json
import os
import subprocess
import sys
import time
import threading
import webbrowser
from pathlib import Path
from datetime import datetime

# ---- 确定项目根 ----
SCRIPT_DIR = Path(__file__).resolve().parent  # dashboard/
PROJECT_ROOT = SCRIPT_DIR.parent              # AI_project_basic_ruler/

# ---- Flask app ----
from flask import Flask, jsonify, request, send_from_directory, Response, stream_with_context

app = Flask(__name__, static_folder=None)

# ---- 给静态文件用 ----
@app.route('/')
def index():
    return send_from_directory(str(SCRIPT_DIR), 'index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(str(SCRIPT_DIR), path)

# ---- API 端点 ----

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'time': datetime.now().isoformat(),
        'project': str(PROJECT_ROOT),
    })

@app.route('/api/data')
def full_data():
    """读取 dashboard-data.json"""
    data_file = SCRIPT_DIR / 'dashboard-data.json'
    if data_file.exists():
        return jsonify(json.loads(data_file.read_text(encoding='utf-8')))
    return jsonify({'error': 'dashboard-data.json not found. Run scripts/generate-dashboard-data.py first.'}), 404

@app.route('/api/status')
def status_snapshot():
    """快速状态快照"""
    skills_dir = PROJECT_ROOT / 'skills'
    skill_names = [d.name for d in skills_dir.iterdir() if d.is_dir()] if skills_dir.exists() else []

    # Git
    stdout, _, _ = _run('git status --short', str(PROJECT_ROOT))
    dirty = len(stdout.strip()) > 0
    dirty_files = stdout.strip().split('\n') if stdout.strip() else []

    stdout2, _, _ = _run('git log --oneline -1', str(PROJECT_ROOT))
    last_commit = stdout2.strip()

    # DCE 集成
    dce = Path('D:/test/DCE_V1.1_clean')
    integration = {
        'AGENTS.md': (dce / 'AGENTS.md').exists(),
        'preflight.py': (dce / 'tools' / 'ai_project_preflight.py').exists(),
        '.codegraph': (dce / '.codegraph').exists(),
        '.cursorrules': (dce / '.cursorrules').exists(),
    }

    return jsonify({
        'time': datetime.now().isoformat(),
        'project': str(PROJECT_ROOT),
        'skills': skill_names,
        'skill_count': len(skill_names),
        'git': {
            'dirty': dirty,
            'dirty_files': dirty_files,
            'last_commit': last_commit,
        },
        'dce_integration': {
            'all_connected': all(integration.values()),
            'details': integration,
        },
    })


@app.route('/api/git-status')
def git_status():
    stdout, _, _ = _run('git status --short', str(PROJECT_ROOT))
    stdout2, _, _ = _run('git log --oneline -8', str(PROJECT_ROOT))
    stdout3, _, _ = _run('git rev-parse --abbrev-ref HEAD', str(PROJECT_ROOT))

    return jsonify({
        'dirty': len(stdout.strip()) > 0,
        'files': stdout.strip().split('\n') if stdout.strip() else [],
        'branch': stdout3.strip(),
        'recent': stdout2.strip().split('\n') if stdout2.strip() else [],
    })


@app.route('/api/run-script', methods=['POST'])
def run_script():
    """执行校验脚本，实时流式输出"""
    body = request.get_json(silent=True) or {}
    script = body.get('script', '')
    cwd = body.get('cwd', str(PROJECT_ROOT))

    # 安全检查：只允许白名单中的脚本
    allowed = [
        'scripts/audit-ai-dev-system.ps1',
        'skills/zzn-skill/scripts/validate_zzn_skill.py',
        'skills/engineering-standard/scripts/validate_engineering_standard.py',
        'skills/engineering-standard/scripts/validate_project_rules.py',
        'skills/engineering-standard/scripts/ai_preflight.py',
    ]
    # DCE 预检
    allowed.append(str(Path('D:/test/DCE_V1.1_clean/tools/ai_project_preflight.py')))

    # 规范化比较
    script_path = Path(script).resolve() if Path(script).is_absolute() else (Path(cwd) / script).resolve()
    allowed_resolved = []
    for a in allowed:
        p = Path(a)
        if p.is_absolute():
            allowed_resolved.append(p.resolve())
        else:
            allowed_resolved.append((PROJECT_ROOT / a).resolve())

    if script_path not in allowed_resolved:
        # 尝试相对路径匹配
        matched = False
        for a in allowed_resolved:
            try:
                if script_path.samefile(a):
                    matched = True
                    break
            except Exception:
                if str(script_path) == str(a):
                    matched = True
                    break

        if not matched:
            return jsonify({
                'error': f'脚本不在允许列表中: {script}',
                'allowed': [str(a) for a in allowed_resolved],
            }), 403

    # 确定执行器
    script_str = str(script_path)
    if script_str.endswith('.ps1'):
        cmd = f'powershell -ExecutionPolicy Bypass -File "{script_str}"'
    elif script_str.endswith('.py'):
        # 按优先级查找可用的 Python
        import shutil
        python_paths = [
            # WorkBuddy managed Python (优先)
            str(Path.home() / '.workbuddy/binaries/python/versions/3.13.12/python.exe'),
            # 系统 Python
            'C:/Python314/python.exe',
            # 系统 PATH
            'python', 'python3',
        ]
        py = None
        for pp in python_paths:
            if shutil.which(pp) or Path(pp).exists():
                py = pp
                break
        if not py:
            return jsonify({'error': '找不到可用的 Python，请检查 server.py 中的 python_paths'}), 500
        cmd = f'"{py}" "{script_str}"'
    else:
        return jsonify({'error': f'不支持的脚本类型: {script_str}'}), 400

    def generate():
        yield f'data: {{"type":"start","script":"{script}","time":"{datetime.now().isoformat()}"}}\n\n'
        try:
            process = subprocess.Popen(
                cmd,
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                cwd=cwd, text=True, encoding='utf-8', errors='replace'
            )
            for line in iter(process.stdout.readline, ''):
                if line:
                    yield f'data: {{"type":"output","text":{json.dumps(line.rstrip())}}}\n\n'
            process.wait()
            yield f'data: {{"type":"done","exit_code":{process.returncode}}}\n\n'
        except Exception as e:
            yield f'data: {{"type":"error","text":{json.dumps(str(e))}}}\n\n'

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


def _run(cmd, cwd=None, timeout=15):
    """运行命令辅助"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           cwd=cwd, timeout=timeout, encoding='utf-8', errors='replace')
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except Exception as e:
        return '', str(e), -1


# ---- 启动 ----

def main():
    import argparse
    parser = argparse.ArgumentParser(description='AI Dev System Dashboard Server')
    parser.add_argument('--port', '-p', type=int, default=8765, help='监听端口 (默认 8765)')
    parser.add_argument('--host', default='127.0.0.1', help='监听地址 (默认 127.0.0.1)')
    parser.add_argument('--no-browser', action='store_true', help='不自动打开浏览器')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    args = parser.parse_args()

    url = f'http://{args.host}:{args.port}'

    print('=' * 60)
    print('  AI Dev System — Dashboard Server')
    print('=' * 60)
    print(f'  地址: {url}')
    print(f'  项目: {PROJECT_ROOT}')
    print(f'  静态: {SCRIPT_DIR}')
    print()
    print('  API 端点:')
    print(f'    GET  {url}/api/health      — 健康检查')
    print(f'    GET  {url}/api/status      — 状态快照')
    print(f'    GET  {url}/api/git-status  — Git 状态')
    print(f'    GET  {url}/api/data        — 完整数据')
    print(f'    POST {url}/api/run-script  — 执行校验脚本')
    print('=' * 60)

    if not args.no_browser:
        def _open():
            time.sleep(0.6)
            webbrowser.open(url)
        threading.Thread(target=_open, daemon=True).start()

    app.run(host=args.host, port=args.port, debug=args.debug, threaded=True)


if __name__ == '__main__':
    main()
