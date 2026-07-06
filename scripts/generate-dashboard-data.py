#!/usr/bin/env python3
"""generate-dashboard-data.py — 扫描项目结构，生成 dashboard-data.json

用法:
    python scripts/generate-dashboard-data.py
    python scripts/generate-dashboard-data.py --output dashboard/dashboard-data.json
    python scripts/generate-dashboard-data.py --watch   # 持续监控，文件变化时自动重新生成

输出: dashboard/dashboard-data.json
"""

import json
import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# ---------- 工具函数 ----------

def run_cmd(cmd, cwd=None, timeout=15):
    """运行命令并返回 (stdout, stderr, returncode)"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           cwd=cwd, timeout=timeout, encoding='utf-8', errors='replace')
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except Exception as e:
        return '', str(e), -1


def read_file(path, encoding='utf-8'):
    """安全读取文件"""
    try:
        return Path(path).read_text(encoding=encoding)
    except Exception:
        try:
            return Path(path).read_text(encoding='gbk', errors='replace')
        except Exception:
            return None


def count_files(directory, pattern='*', max_depth=10):
    """递归统计文件数"""
    d = Path(directory)
    if not d.exists():
        return 0
    files = [p for p in d.rglob(pattern) if p.is_file() and '.git' not in p.parts]
    return len(files)


# ---------- 数据采集 ----------

def scan_skills(root: Path):
    """扫描 skills/ 目录"""
    skills_dir = root / 'skills'
    if not skills_dir.exists():
        return []

    skills = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / 'SKILL.md'
        if not skill_md.exists():
            continue

        name = skill_dir.name
        refs = list((skill_dir / 'references').rglob('*.md')) if (skill_dir / 'references').exists() else []
        scripts = list((skill_dir / 'scripts').rglob('*.py')) + list((skill_dir / 'scripts').rglob('*.ps1')) if (skill_dir / 'scripts').exists() else []
        agents = list((skill_dir / 'agents').rglob('*.yaml')) + list((skill_dir / 'agents').rglob('*.yml')) if (skill_dir / 'agents').exists() else []

        all_files = [str(p.relative_to(skill_dir)) for p in skill_dir.rglob('*') if p.is_file() and '.git' not in p.parts]

        # 读 SKILL.md 提取描述
        content = read_file(skill_md) or ''
        first_line = content.split('\n')[0].strip('# ').strip() if content else ''
        desc_line = ''
        for line in content.split('\n')[1:8]:
            clean = line.strip()
            if clean and not clean.startswith('#') and not clean.startswith('---'):
                desc_line = clean
                break

        skills.append({
            'name': name,
            'title': first_line or name,
            'description': desc_line,
            'path': str(skill_dir.relative_to(root)),
            'files': all_files,
            'file_count': len(all_files),
            'ref_count': len(refs),
            'script_count': len(scripts),
            'refs': [str(p.name) for p in refs],
            'scripts': [str(p.name) for p in scripts],
            'agents': [str(p.name) for p in agents],
        })

    return skills


def scan_experience_candidates(root: Path):
    """读取经验候选池"""
    candidates_file = root / 'skills' / 'zzn-skill' / 'references' / 'experience-candidates.md'
    if not candidates_file.exists():
        return {'total': 0, 'candidates': [], 'upgraded': []}

    content = read_file(candidates_file) or ''
    candidates = []
    upgraded = []

    # 简单解析：找 ## 标题和规则内容
    current = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('## ') and 'C0' in line:
            if current:
                candidates.append(current)
            current = {'id': line.strip('# ').strip(), 'rules': [], 'status': 'candidate'}
        elif line.startswith('## ') and '已升级' in line:
            if current:
                current['status'] = 'upgraded'
                upgraded.append(current)
            current = None
        elif current and line and not line.startswith('#'):
            if line.startswith('- ') or line.startswith('* '):
                current['rules'].append(line.strip('- *').strip())

    if current and current.get('rules'):
        if current['status'] == 'upgraded':
            upgraded.append(current)
        else:
            candidates.append(current)

    return {
        'total': len(candidates) + len(upgraded),
        'candidate_count': len(candidates),
        'upgraded_count': len(upgraded),
        'candidates': candidates,
        'upgraded': upgraded,
    }


def check_git_status(root: Path):
    """检查 Git 状态"""
    stdout, stderr, rc = run_cmd('git status --short', cwd=str(root))
    dirty_files = stdout.split('\n') if stdout else []

    stdout2, _, _ = run_cmd('git log --oneline -10', cwd=str(root))
    commits = stdout2.split('\n') if stdout2 else []

    stdout3, _, _ = run_cmd('git rev-parse --abbrev-ref HEAD', cwd=str(root))
    branch = stdout3.strip() if stdout3 else 'unknown'

    stdout4, _, _ = run_cmd('git log --oneline -1', cwd=str(root))
    last_commit = stdout4.strip() if stdout4 else ''

    return {
        'dirty': len([f for f in dirty_files if f]) > 0,
        'dirty_files': [f.strip() for f in dirty_files if f],
        'branch': branch,
        'commit_count': len([c for c in commits if c]),
        'last_commit': last_commit,
        'recent_commits': [c.strip() for c in commits[:5] if c],
    }


def scan_project_integration(root: Path):
    """检查 DCE 项目集成状态"""
    dce_path = Path('D:/test/DCE_V1.1_clean')
    items = []

    checks = [
        ('AGENTS.md', 'DCE 项目入口规则', 'agents'),
        ('tools/ai_project_preflight.py', 'AI 预检脚本', 'preflight'),
        ('.codegraph/', '代码知识图谱', 'codegraph'),
        ('.cursorrules', 'Cursor 规则', 'cursor'),
    ]

    for rel_path, label, key in checks:
        full_path = dce_path / rel_path
        exists = full_path.exists()
        items.append({
            'key': key,
            'label': label,
            'path': str(full_path),
            'exists': exists,
            'status': 'connected' if exists else 'missing',
        })

    # 检查 .codex skills
    codex_skills_dir = Path.home() / '.codex' / 'skills'
    installed_skills = []
    if codex_skills_dir.exists():
        installed_skills = [d.name for d in codex_skills_dir.iterdir() if d.is_dir()]

    return {
        'project': 'DCE 检测归档报告编辑器',
        'path': str(dce_path),
        'items': items,
        'all_connected': all(it['exists'] for it in items),
        'codex_skills_installed': installed_skills,
        'codex_skills_count': len(installed_skills),
    }


def scan_docs(root: Path):
    """扫描文档"""
    docs_dir = root / 'docs'
    if not docs_dir.exists():
        return {'count': 0, 'docs': []}

    docs = []
    for f in sorted(docs_dir.rglob('*.md')):
        docs.append(str(f.relative_to(docs_dir)))

    return {'count': len(docs), 'docs': docs}


def scan_prompts(root: Path):
    """扫描 Prompt 模板"""
    prompts_dir = root / 'prompts'
    if not prompts_dir.exists():
        return {'count': 0, 'prompts': []}

    prompts = [f.name for f in sorted(prompts_dir.glob('*.md'))]
    return {'count': len(prompts), 'prompts': prompts}


def scan_scripts(root: Path):
    """扫描脚本"""
    scripts_dir = root / 'scripts'
    if not scripts_dir.exists():
        return {'count': 0, 'scripts': []}

    scripts = [f.name for f in sorted(scripts_dir.glob('*')) if f.is_file()]
    return {'count': len(scripts), 'scripts': scripts}


def scan_project_structure(root: Path):
    """统计项目文件结构"""
    total = count_files(str(root))
    return {
        'total_files': total,
        'skills': count_files(str(root / 'skills')),
        'docs': count_files(str(root / 'docs')),
        'prompts': count_files(str(root / 'prompts')),
        'scripts': count_files(str(root / 'scripts')),
        'configs': count_files(str(root), '*.md') + count_files(str(root), '.cursorrules'),
    }


# ---------- 主逻辑 ----------

def generate(root: Path, output: Path):
    """生成完整 JSON"""
    data = {
        'generated_at': datetime.now().isoformat(),
        'generator': 'generate-dashboard-data.py',
        'project': {
            'name': 'AI Dev System',
            'version': 'v1.0',
            'path': str(root),
        },
        'structure': scan_project_structure(root),
        'skills': scan_skills(root),
        'experience': scan_experience_candidates(root),
        'git': check_git_status(root),
        'docs': scan_docs(root),
        'prompts': scan_prompts(root),
        'scripts': scan_scripts(root),
        'integration': scan_project_integration(root),
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return data


def watch_mode(root: Path, output: Path, interval=5):
    """文件监控模式，变化时自动重新生成"""
    import hashlib

    print(f'[watch] 监控 {root}，每 {interval}s 检查变化...')

    # 建立初始文件哈希
    file_hashes = {}
    for f in root.rglob('*'):
        if f.is_file() and '.git' not in f.parts:
            try:
                file_hashes[str(f)] = hashlib.md5(f.read_bytes()).hexdigest()
            except Exception:
                pass

    while True:
        time.sleep(interval)
        changed = False
        current_files = set()

        for f in root.rglob('*'):
            if f.is_file() and '.git' not in f.parts:
                fp = str(f)
                current_files.add(fp)
                try:
                    h = hashlib.md5(f.read_bytes()).hexdigest()
                except Exception:
                    continue

                if fp not in file_hashes or file_hashes[fp] != h:
                    changed = True
                    file_hashes[fp] = h

        # 检测删除的文件
        for fp in list(file_hashes.keys()):
            if fp not in current_files:
                changed = True
                del file_hashes[fp]

        if changed:
            print(f'[{datetime.now().strftime("%H:%M:%S")}] 检测到文件变化，重新生成...')
            data = generate(root, output)
            print(f'  → 生成完成: {output} ({len(json.dumps(data))} bytes)')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='生成 AI Dev System Dashboard 数据')
    parser.add_argument('--output', '-o', default=None, help='输出 JSON 路径')
    parser.add_argument('--watch', '-w', action='store_true', help='文件监控模式')
    parser.add_argument('--interval', type=int, default=5, help='监控间隔(秒)')
    args = parser.parse_args()

    # 确定项目根目录
    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent  # scripts/ 的父目录 = 项目根

    # 输出路径
    if args.output:
        output = Path(args.output)
    else:
        output = root / 'dashboard' / 'dashboard-data.json'

    if args.watch:
        watch_mode(root, output, args.interval)
    else:
        data = generate(root, output)
        print(f'✅ 数据已生成: {output}')
        print(f'   {data["structure"]["total_files"]} 文件')
        print(f'   {len(data["skills"])} Skills')
        print(f'   {data["experience"]["total"]} 经验候选')
        print(f'   {'工作区干净' if not data["git"]["dirty"] else "有未提交变更"}')
        print(f'   DCE 集成: {'全部就绪' if data["integration"]["all_connected"] else "部分缺失"}')


if __name__ == '__main__':
    main()
