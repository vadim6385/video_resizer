# Video Resizer Tool

A professional Python GUI application that automatically resizes videos to a target resolution while maintaining aspect ratio. The tool processes videos recursively through folders and subfolders, only downscaling larger videos to fit your specified dimensions.

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Recursive Processing** | Automatically processes videos in folders and all subfolders |
| **Smart Resizing** | Maintains aspect ratio while resizing to target dimensions (only downscales) |
| **Modern GUI** | User-friendly interface with real-time progress tracking |
| **Color-coded Logging** | Live output with color-coded status messages (green=success, gray=skipped, red=error) |
| **Dual Progress Tracking** | Overall progress bar and individual video progress indicator |
| **Safe Processing** | Only resizes videos larger than target dimensions; skips smaller videos |
| **Batch Processing** | Handles multiple video formats with overwrite capability |
| **Process Control** | Stop button to interrupt processing at any time |

## 🖼️ Screenshots

*Application GUI showing video processing in progress*

*(Add your screenshots here after running the application)*

## 🚀 Installation

### Prerequisites

- **Python 3.6 or higher**
- **FFmpeg** - must be installed and available in system PATH

#### Installing FFmpeg

**Windows:**
1. Download from [FFmpeg Official Website](https://ffmpeg.org/download.html)
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add `C:\ffmpeg\bin` to your system PATH environment variable

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/vadim6385/video_resizer.git
   cd video-resizer-tool
   ```

2. **Verify FFmpeg installation**
   ```bash
   ffmpeg -version
   ```

3. **Run the application**
   ```bash
   python video_resizer.py
   ```

> **Note**: No additional Python packages required! The tool uses only Python's standard library modules.

## 📖 Usage

### Basic Usage

1. **Launch the application**
   ```bash
   python video_resizer.py
   ```

2. **Set target resolution** (optional)
   - Modify the width and height fields (default: 1920x1080)

3. **Select video codec** (optional)
   - Choose from libx264, libx265, or copy

4. **Browse for folder**
   - Click "Browse" and select the folder containing your videos

5. **Start processing**
   - Click "Start Processing" to begin resizing
   - Monitor progress in the log window and progress bars

6. **Stop processing** (if needed)
   - Click "Stop" to interrupt the process at any time

### Supported Video Formats

- **MP4** (.mp4)
- **MOV** (.mov)
- **AVI** (.avi)
- **MKV** (.mkv)
- **FLV** (.flv)
- **WMV** (.wmv)
- **M4V** (.m4v)
- **WebM** (.webm)

## 🔧 How It Works

The Video Resizer Tool uses FFmpeg for reliable video processing:

1. **Dimension Detection**: Uses `ffprobe` to read original video dimensions and rotation metadata
2. **Smart Scaling**: Calculates new dimensions while maintaining aspect ratio using `force_original_aspect_ratio=decrease`
3. **Padding**: Adds padding when necessary to maintain exact target resolution
4. **Efficient Encoding**: Uses libx264/libx265 with CRF 23 for optimal quality/size balance
5. **Audio Preservation**: Copies original audio streams without re-encoding
6. **Safe File Handling**: Creates temporary files with proper validation before overwriting originals

## 📁 Project Structure

```
video-resizer-tool/
├── video_resizer.py          # Main application file
├── README.md                 # Project documentation (this file)
├── requirements.txt          # Python dependencies (none required)
└── assets/                   # Screenshots and documentation assets
    ├── screenshot-main.png
    └── screenshot-processing.png
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Setup

No special development environment needed! Just ensure you have:
- Python 3.6+
- FFmpeg in PATH
- Basic understanding of tkinter for GUI modifications

## ❓ Frequently Asked Questions

**Q: The tool fails to resize my videos. What should I check?**  
A: First, verify FFmpeg is installed correctly by running `ffmpeg -version` in your terminal. Also ensure you have write permissions for the video files.

**Q: Can I resize videos to larger dimensions?**  
A: No, the tool only downscales videos. It will skip any videos that are already smaller than your target resolution.

**Q: How can I verify the resizing worked correctly?**  
A: Check the output log - successful resizes show in green, skipped files in gray. The tool also displays original and output dimensions for verification.

**Q: My video paths contain spaces - will this work?**  
A: Yes! The tool properly handles file paths with spaces and special characters.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **"FFmpeg not found" error**
   - Solution: Reinstall FFmpeg and ensure it's in your system PATH

2. **Permission errors during file overwrite**
   - Solution: Run as administrator or ensure you have write permissions

3. **Long path errors on Windows**
   - Solution: Use folders with shorter path names or enable long paths in Windows

4. **Videos not being resized**
   - Check that original dimensions are larger than target resolution
   - Verify the video files aren't corrupted or DRM-protected

### Getting Help

If you encounter issues:
1. Check the error messages in the application log
2. Ensure FFmpeg works from your command line
3. Try processing a single video file first for testing

---

**Happy Video Processing!** 🎥
```

This README.md provides comprehensive documentation for your Video Resizer Tool GitHub repository. The file includes all essential sections that users and contributors expect to see, with clear installation instructions, usage examples, and troubleshooting guidance.

You can copy this content and save it as `README.md` in your project repository. Remember to:
1. Replace "yourusername" in the clone URL with your actual GitHub username
2. Add actual screenshots of your application in the screenshots section
3. Create a LICENSE file if you choose a specific open-source license

The README uses professional formatting with tables, code blocks, and clear section organization that will make your project appealing to potential users and contributors.
