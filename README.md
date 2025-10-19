# 🎯 Python AutoClicker

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

A powerful and customizable Python-based autoclicker application with a sleek GUI interface. Record mouse clicks and movements, then replay them with randomized timing and positioning for natural automation.

## ✨ Features

- 🎨 **Modern Dark Theme GUI** - Apple-inspired interface with smooth animations
- 🖱️ **Mouse Recording** - Record sequences of mouse clicks and movements
- 🎲 **Randomization Options** - Add human-like variation to timing and positioning
- ⚙️ **Configurable Settings** - Customize move times, click intervals, radius, and angles
- 📊 **Real-time Console** - Monitor recorded actions with detailed statistics
- 💾 **Data Export** - Export recorded data to CSV files
- 🔄 **Multiple Easing Modes** - Choose from various mouse movement curves
- 🛑 **Hotkey Control** - Start/stop recording with customizable keybinds
- 🖼️ **Cross-platform Support** - Works on Windows, macOS, and Linux

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)
*The main autoclicker interface with configuration options.*

### Recording Console
![Recording Console](screenshots/recording_console.png)
*Real-time monitoring of recorded mouse actions.*

### Configuration Panel
![Configuration Panel](screenshots/configuration_panel.png)
*Detailed settings for timing, radius, and easing modes.*

*Note: Screenshots will be added once the application is fully set up.*

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Quick Install

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/python-autoclicker.git
   cd python-autoclicker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r Requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Alternative Installation (Standalone Executable)

For Windows users, you can use the provided executable:
- Download `AutoClicker.exe` from the releases
- Run the executable directly (no Python installation required)

## 📖 Usage

### Basic Workflow

1. **Launch the Application**
   - Run `python main.py` or execute `AutoClicker.exe`

2. **Configure Settings**
   - Set move time range (seconds)
   - Set click time range (seconds)
   - Adjust radius and angle for randomization
   - Select desired easing modes

3. **Select Target Application**
   - Click "Select key:" to choose your hotkey
   - Click "Start Recording" to choose the target window

4. **Record Actions**
   - Press your hotkey to start recording
   - Click on the target application to record positions
   - Press the hotkey again to stop recording

5. **Playback**
   - The autoclicker will automatically replay the recorded sequence
   - Use the console to monitor progress

### Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| **Move Time** | Time range for mouse movements (seconds) | 2.0 - 5.0 |
| **Click Time** | Time range between clicks (seconds) | 0.0 - 5.0 |
| **Radius** | Randomization radius around click points | 5 pixels |
| **Angle** | Angle range for randomization | 360° |
| **Timeout** | Delay between action sequences | 2.0 seconds |

### Easing Modes

Choose from these mouse movement curves:
- `easeInQuad` - Accelerating movement
- `easeOutQuad` - Decelerating movement
- `easeInOutQuad` - Accelerate then decelerate
- `easeOutQuart` - Sharp deceleration
- `easeInOutQuart` - Smooth acceleration/deceleration
- `easeInBack` - Bounce-back effect

## ⚙️ Configuration

The application uses a `config.ini` file to store settings:

```ini
[Mouse]
modelist = easeInQuad easeOutQuad easeInOutQuad easeOutQuart easeInOutQuart easeInQuad easeInBack
startmove = 2.0
endmove = 5.0
startclick = 0.0
endclick = 5.0
radius = 5
angle = 360
timeout = 2.0

[key]
keybind = Key.space
```

### Configuration Parameters

- **modelist**: Space-separated list of easing functions
- **startmove/endmove**: Min/max time for mouse movements
- **startclick/endclick**: Min/max time between clicks
- **radius**: Pixel radius for position randomization
- **angle**: Degree range for angle randomization
- **timeout**: Seconds to wait between sequences
- **keybind**: Keyboard key for start/stop recording

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Install development dependencies: `pip install -r dev-requirements.txt`
4. Make your changes
5. Run tests: `python -m pytest`
6. Commit your changes: `git commit -am 'Add new feature'`
7. Push to the branch: `git push origin feature/your-feature`
8. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters
- Add docstrings to classes and methods
- Keep functions focused and single-purpose

### Reporting Issues

- Use the GitHub issue tracker
- Provide detailed steps to reproduce
- Include system information (OS, Python version)
- Attach relevant screenshots or logs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Developer**: [Your Name]
- **Libraries Used**:
  - [pynput](https://pypi.org/project/pynput/) - Keyboard and mouse control
  - [Pillow](https://pypi.org/project/Pillow/) - Image processing
  - [pyautogui](https://pypi.org/project/PyAutoGUI/) - GUI automation
  - [configparser](https://docs.python.org/3/library/configparser.html) - Configuration file parsing

## 📞 Support

If you have questions or need help:

- 📧 **Email**: your.email@example.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/python-autoclicker/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/python-autoclicker/discussions)

---

**⚠️ Disclaimer**: Use this tool responsibly and in accordance with applicable laws and terms of service. The developers are not responsible for misuse.