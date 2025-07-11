import os
import shutil
from pathlib import Path
from fnmatch import fnmatch

def load_gitignore_patterns(gitignore_path=".gitignore"):
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns

def is_ignored(path, patterns):
    for pattern in patterns:
        if fnmatch(path, pattern) or fnmatch(os.path.basename(path), pattern):
            return True
    return False

def backup_ignored_files(base_dir=".", backup_dir="backup_ignorados"):
    base_dir = Path(base_dir).resolve()
    backup_dir = base_dir / backup_dir
    patterns = load_gitignore_patterns(base_dir / ".gitignore")

    if not patterns:
        print("Nenhum padrão encontrado no .gitignore.")
        return

    if not backup_dir.exists():
        backup_dir.mkdir(parents=True)

    for root, dirs, files in os.walk(base_dir):
        root_path = Path(root)
        rel_root = root_path.relative_to(base_dir)

        # Ignora o próprio diretório de backup
        if backup_dir in root_path.parents or root_path == backup_dir:
            continue

        for name in files + dirs:
            rel_path = rel_root / name
            if is_ignored(str(rel_path), patterns):
                src_path = base_dir / rel_path
                dest_path = backup_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                if src_path.is_file():
                    shutil.copy2(src_path, dest_path)
                elif src_path.is_dir():
                    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)

    print(f"Backup concluído em: {backup_dir}")

# Executar o backup
backup_ignored_files()
