# dotfiles

Configuration personnelle : Claude Code, Git, Bash.

## Contenu

| Fichier | Destination |
|---------|-------------|
| `.bashrc` | `~/.bashrc` |
| `.gitconfig` | `~/.gitconfig` |
| `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| `.claude/settings.json` | `~/.claude/settings.json` |

## Installation sur une nouvelle machine

```bash
git clone git@github.com:ChrisHeral/dotfiles.git ~/dotfiles
bash ~/dotfiles/install.sh
```

Le script crée des symlinks depuis `~/dotfiles` vers les emplacements attendus.

## Mise à jour

Les fichiers étant des symlinks, toute modification est directement dans le repo :

```bash
cd ~/dotfiles
git add .
git commit -m "chore: ..."
git push
```

Sur les autres machines :

```bash
cd ~/dotfiles && git pull
```
