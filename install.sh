#!/bin/bash
set -e

DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"

symlink() {
  local src="$DOTFILES_DIR/$1"
  local dst="$HOME/$2"
  mkdir -p "$(dirname "$dst")"
  ln -sf "$src" "$dst"
  echo "  $dst -> $src"
}

echo "Installing dotfiles..."
symlink ".bashrc"            ".bashrc"
symlink ".gitconfig"         ".gitconfig"
symlink ".claude/CLAUDE.md"  ".claude/CLAUDE.md"
symlink ".claude/settings.json" ".claude/settings.json"
echo "Done."
