Title: Automating My Mac Setup with Dotfiles and AI
Date: 2025-06-15 10:00
Modified: 2025-06-15 10:00
Category: posts
Tags: dotfiles, macOS, automation, bash, homebrew, AI, Claude Code
Slug: automating-mac-setup-with-dotfiles-and-ai
Authors: Jitse-Jan
Summary: How I completely automated the provisioning of my new laptop using a structured dotfiles repository, Homebrew, and AI agents.

In the past, setting up a new machine meant spending a whole weekend downloading apps, tweaking terminal settings, and trying to remember exactly which command-line tools I used. With my new laptop, I decided to completely automate the process.

I created a [dotfiles repository](https://github.com/jitsejan/dotfiles) that provisions my entire working environment from scratch with just a single command. It is not a novel concept, but it has completely streamlined my workflow.

## The core philosophy

The goal was simple: clone the repository and run a bootstrap script. The script should handle everything from package management to symlinking configuration files, without requiring manual intervention.

My current setup revolves around a few key technologies:
- **Terminal:** [Kitty](https://sw.kovidgoyal.net/kitty/) with custom tabs and bindings.
- **Shell:** Fish shell paired with the [Starship](https://starship.rs/) prompt for a fast, informative command line.
- **Package Management:** Homebrew paired with a `Brewfile`.
- **Python Ecosystem:** A heavy focus on modern tooling like `uv`, `Rye`, `Ruff`, and `pyright`.

## The bootstrap process

The entry point of my setup is a `bootstrap.sh` script. When executed, it acts as an orchestrator that triggers a series of focused, modular scripts located in the `scripts/` directory.

### 1. Homebrew and the Brewfile
The heavy lifting of software installation is handled by Homebrew. Instead of writing endless `brew install` commands in bash, I use a `Brewfile`. Running `brew bundle` reads this file and installs everything in one go:
- Essential CLI utilities (`bat`, `eza`, `fd`, `fzf`, `jq`, `ripgrep`, `zoxide`)
- Core development tools (`git`, `docker`, `awscli`, `terraform`, `kubectl`, `databricks`)
- Desktop applications (`kitty`, `cursor`, `obsidian`, `google-chrome`)

By keeping the `Brewfile` tracked in git, I have a single source of truth for all my installed software.

### 2. Configuration symlinking
Instead of copying files into system directories, the setup scripts create symlinks from my `dotfiles/.config/` folder to my user's `~/.config/` directory. This means whenever I tweak my Starship prompt (`starship.toml`), update my Fish shell functions, or modify my Kitty configuration, the changes are tracked in my Git repository instantly.

### 3. Application-specific setup
Some configurations require more than just installing a package. For these, I wrote dedicated setup scripts:
- `setup_dock.sh`: Automatically clears the macOS default dock and pins only my essential applications using `dockutil`.
- `install_python_tools.sh`: Bootstraps my Python environment.
- Various setup scripts for tools like PostgreSQL, Terraform, Docker, and Git Filter Repo to ensure they are configured exactly how I like them out of the box.

## AI-powered workflow with Claude Code

Beyond just installing applications, I've deeply integrated AI into my development workflow from day one. Using **Claude Code** within my terminal, I've automated much of the tedious repository management that usually slows down engineering. 

Instead of manually clicking through web interfaces, I prompt Claude from my CLI to understand my codebase, generate tickets, scaffold out new features, create pull requests, and even handle PR merges. Having an autonomous AI pairing partner that lives natively inside the environment that my dotfiles just provisioned is a massive productivity multiplier.

## The result

Now, whenever I need to set up a new Mac, the process looks like this:

```bash
git clone git@github.com:jitsejan/dotfiles.git ~/dotfiles
cd ~/dotfiles
./scripts/bootstrap.sh
```

Within minutes, I have a fully functional development environment backed by AI, looking and behaving exactly like my old one. If you find yourself repeatedly setting up development environments, I highly recommend building your own dotfiles repository. It's an investment that pays off every time you switch hardware.
