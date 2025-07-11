#!/bin/bash

# Fedora Post-Installation Setup Script
# This script updates the system and installs essential development tools

set -e  # Exit on any error

echo "🚀 Starting Fedora setup..."

# Update system packages
echo "📦 Updating system packages..."
sudo dnf update -y

# Install essential packages and dependencies
echo "🔧 Installing essential packages..."
sudo dnf install -y curl wget git python3 python3-pip

# Install VS Code
echo "💻 Installing Visual Studio Code..."
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
sudo dnf check-update
sudo dnf install -y code

# Install Docker
echo "🐳 Installing Docker..."
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable Docker service
echo "🔄 Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to docker group (requires logout/login to take effect)
echo "👤 Adding user to docker group..."
sudo usermod -aG docker $USER

# Install additional Python tools
echo "🐍 Installing Python development tools..."
sudo dnf install -y python3-devel python3-setuptools
pip3 install --user --upgrade pip

# Install useful development tools
echo "🛠️ Installing additional development tools..."
sudo dnf install -y vim nano htop tree unzip zip

# Clean up
echo "🧹 Cleaning up..."
sudo dnf autoremove -y
sudo dnf clean all

echo "✅ Setup complete!"
echo ""
echo "📋 What was installed:"
echo "   • System updates"
echo "   • Git CLI"
echo "   • Visual Studio Code"
echo "   • Docker (with Docker Compose)"
echo "   • Python 3 with pip"
echo "   • Development tools (vim, nano, htop, tree, etc.)"
echo ""
echo "⚠️  Important notes:"
echo "   • You need to log out and log back in for Docker group permissions to take effect"
echo "   • VS Code can be launched with: code"
echo "   • Docker version: $(docker --version 2>/dev/null || echo 'Docker installed, restart required')"
echo "   • Python version: $(python3 --version)"
echo "   • Git version: $(git --version)"
echo ""
echo "🎉 Your Fedora development environment is ready!"
