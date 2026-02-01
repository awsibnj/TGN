#!/bin/bash

echo "=========================================="
echo "WorkHub Telegram Bot Setup Script"
echo "=========================================="
echo ""

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        echo "✓ Python 3 found: $PYTHON_VERSION"
        return 0
    else
        echo "✗ Python 3 not found. Please install Python 3.8 or higher."
        exit 1
    fi
}

check_pip() {
    if command -v pip3 &> /dev/null; then
        echo "✓ pip3 found"
        return 0
    else
        echo "✗ pip3 not found. Installing..."
        sudo apt-get install python3-pip -y
    fi
}

create_venv() {
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo "✓ Virtual environment created"
    else
        echo "✓ Virtual environment already exists"
    fi
}

activate_venv() {
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "✓ Virtual environment activated"
}

install_dependencies() {
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
}

setup_env() {
    if [ ! -f ".env" ]; then
        echo "Creating .env file from template..."
        cp .env.example .env
        echo "✓ .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env file with your credentials before running the bot!"
        echo "   nano .env"
    else
        echo "✓ .env file already exists"
    fi
}

echo "Step 1: Checking Python installation..."
check_python
echo ""

echo "Step 2: Checking pip installation..."
check_pip
echo ""

echo "Step 3: Creating virtual environment..."
create_venv
echo ""

echo "Step 4: Activating virtual environment..."
activate_venv
echo ""

echo "Step 5: Installing dependencies..."
install_dependencies
echo ""

echo "Step 6: Setting up environment file..."
setup_env
echo ""

echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials:"
echo "   nano .env"
echo ""
echo "2. Set up Supabase database:"
echo "   - Go to https://supabase.com"
echo "   - Create a new project"
echo "   - Run the SQL from supabase_schema.sql"
echo "   - Copy your project URL and API key to .env"
echo ""
echo "3. Create Telegram bot:"
echo "   - Chat with @BotFather on Telegram"
echo "   - Create a new bot and get the token"
echo "   - Add token to .env"
echo ""
echo "4. Create Telegram channel:"
echo "   - Create a channel and add your bot as admin"
echo "   - Add channel ID to .env"
echo ""
echo "5. Run the bot:"
echo "   source venv/bin/activate"
echo "   python bot.py"
echo ""
echo "For detailed instructions, see README.md"
echo "=========================================="
