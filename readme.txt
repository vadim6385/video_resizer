Video Resizer Tool
==================

A Python GUI application that resizes videos to a target resolution while maintaining aspect ratio. The tool only downscales videos (never enlarges them) and processes all videos in a folder and its subfolders recursively.

Features
--------
- Recursive folder processing
- Smart resizing (maintains aspect ratio, only downscales)
- Color-coded output (green for success, gray for skipped, red for errors)
- Dual progress bars (overall and per-video)
- Stop button to interrupt processing
- Auto-scrolling log display
- Customizable target resolution
- Multiple video codec support (libx264, libx265, copy)

Requirements
------------
- Python 3.6 or newer
- FFmpeg installed on your system

System Requirements
-------------------
- Windows, macOS, or Linux
- FFmpeg accessible from system PATH

Installation
------------
1. Install FFmpeg on your system:
   - Windows: Download from https://ffmpeg.org/download.html and add to PATH
   - macOS: brew install ffmpeg
   - Linux (Ubuntu/Debian): sudo apt install ffmpeg

2. Run the script:
   python video_resizer.py

No additional Python packages are required as the script uses only standard library modules.

Usage
-----
1. Run the script: python video_resizer.py
2. Optionally change the target resolution (default: 1920x1080)
3. Optionally select a different video codec (default: libx264)
4. Click "Browse" to select a folder containing videos
5. Click "Start Processing" to begin resizing videos
6. Monitor progress in the log window and progress bars
7. Click "Stop" to interrupt processing if needed

Supported Video Formats
-----------------------
- MP4 (.mp4)
- MOV (.mov) 
- AVI (.avi)
- MKV (.mkv)
- FLV (.flv)
- WMV (.wmv)
- M4V (.m4v)
- WebM (.webm)

Notes
-----
- The tool will overwrite original files after successful resizing
- Videos already smaller than the target resolution will be skipped
- Processing time depends on video size and your computer's performance
- The application uses FFmpeg for video processing

Troubleshooting
---------------
1. If you get "FFmpeg not found" errors:
   - Ensure FFmpeg is installed and added to your system PATH
   - Test FFmpeg by running "ffmpeg -version" in your command prompt

2. If you encounter path-related errors:
   - Try using folders with shorter path names
   - Avoid special characters in folder and file names

3. For other issues:
   - Check the error messages in the log window
   - Ensure you have write permissions for the video files

License
-------
This tool is provided as-is for personal use.