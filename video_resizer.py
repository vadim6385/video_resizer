import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from pathlib import Path
import subprocess
import sys
import time
import json
import shutil
import tempfile

class VideoResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Resizer Tool")
        self.root.geometry("900x700")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.stop_processing = False
        self.total_videos = 0
        self.processed_videos = 0
        
        # Setup GUI
        self.setup_gui()
        
        # Check FFmpeg availability
        self.check_ffmpeg()
        
    def check_ffmpeg(self):
        """Check if FFmpeg is available in the system PATH"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            if result.returncode == 0:
                self.log_message("FFmpeg is available\n", "success")
                return True
            else:
                self.log_message("FFmpeg is not available or not working properly\n", "error")
                return False
        except (subprocess.SubprocessError, FileNotFoundError):
            self.log_message("FFmpeg is not installed or not in system PATH\n", "error")
            return False
        
    def setup_gui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Video Resizer Tool", font=("Arial", 16, "bold"), 
                              fg="white", bg='#2b2b2b')
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = tk.Label(main_frame, text="Resize videos to target resolution (only downscale)", 
                             fg="lightgray", bg='#2b2b2b', font=("Arial", 10))
        desc_label.pack(pady=(0, 20))
        
        # Settings frame
        settings_frame = tk.Frame(main_frame, bg='#2b2b2b')
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Resolution settings
        res_label = tk.Label(settings_frame, text="Target Resolution:", 
                            fg="white", bg='#2b2b2b', font=("Arial", 9))
        res_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.width_var = tk.StringVar(value="1920")
        width_entry = tk.Entry(settings_frame, textvariable=self.width_var, width=5, 
                              font=("Arial", 9))
        width_entry.pack(side=tk.LEFT, padx=(0, 2))
        
        x_label = tk.Label(settings_frame, text="x", 
                          fg="white", bg='#2b2b2b', font=("Arial", 9))
        x_label.pack(side=tk.LEFT, padx=2)
        
        self.height_var = tk.StringVar(value="1080")
        height_entry = tk.Entry(settings_frame, textvariable=self.height_var, width=5, 
                               font=("Arial", 9))
        height_entry.pack(side=tk.LEFT, padx=(2, 10))
        
        # Codec settings
        codec_label = tk.Label(settings_frame, text="Video Codec:", 
                              fg="white", bg='#2b2b2b', font=("Arial", 9))
        codec_label.pack(side=tk.LEFT, padx=(10, 5))
        
        self.codec_var = tk.StringVar(value="libx264")
        codec_combo = ttk.Combobox(settings_frame, textvariable=self.codec_var, width=10,
                                  values=["libx264", "libx265", "copy"], state="readonly")
        codec_combo.pack(side=tk.LEFT)
        
        # Browse frame
        browse_frame = tk.Frame(main_frame, bg='#2b2b2b')
        browse_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.folder_path = tk.StringVar()
        folder_entry = tk.Entry(browse_frame, textvariable=self.folder_path, width=50, 
                               font=("Arial", 10))
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(browse_frame, text="Browse", command=self.browse_folder, 
                              bg='#4a4a4a', fg="white", font=("Arial", 10))
        browse_btn.pack(side=tk.RIGHT)
        
        # Progress bars frame
        progress_frame = tk.Frame(main_frame, bg='#2b2b2b')
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Total progress label
        self.total_label = tk.Label(progress_frame, text="Overall Progress: 0/0", 
                                   fg="white", bg='#2b2b2b', font=("Arial", 9))
        self.total_label.pack(anchor=tk.W)
        
        # Total progress bar
        self.total_progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, 
                                             length=100, mode='determinate')
        self.total_progress.pack(fill=tk.X, pady=(5, 10))
        
        # Current video progress label
        self.current_label = tk.Label(progress_frame, text="Current Video: Not started", 
                                     fg="white", bg='#2b2b2b', font=("Arial", 9))
        self.current_label.pack(anchor=tk.W)
        
        # Current video progress bar
        self.current_progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, 
                                               length=100, mode='determinate')
        self.current_progress.pack(fill=tk.X, pady=(5, 0))
        
        # Output text area
        text_frame = tk.Frame(main_frame, bg='#2b2b2b')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_label = tk.Label(text_frame, text="Processing Log:", fg="white", 
                             bg='#2b2b2b', font=("Arial", 10))
        text_label.pack(anchor=tk.W)
        
        self.output_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                    width=80, height=20, 
                                                    bg='black', fg='white', 
                                                    font=("Consolas", 9))
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Tag configurations for colored text
        self.output_text.tag_config("success", foreground="#00ff00")
        self.output_text.tag_config("skip", foreground="#888888")
        self.output_text.tag_config("error", foreground="#ff0000")
        self.output_text.tag_config("info", foreground="#ffffff")
        self.output_text.tag_config("warning", foreground="#ffff00")
        self.output_text.tag_config("debug", foreground="#8888ff")
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(fill=tk.X, pady=(15, 5))
        
        self.start_btn = tk.Button(button_frame, text="Start Processing", 
                                  command=self.start_processing, bg='#2d6e2d', 
                                  fg="white", font=("Arial", 10, "bold"))
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(button_frame, text="Stop", 
                                 command=self.stop_processing_func, 
                                 state=tk.DISABLED, bg='#6e2d2d', 
                                 fg="white", font=("Arial", 10))
        self.stop_btn.pack(side=tk.LEFT)
        
    def browse_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Folder with Videos")
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.log_message(f"Selected folder: {folder_selected}\n", "info")
            
    def log_message(self, message, tag="info"):
        self.output_text.insert(tk.END, message, tag)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_processing(self):
        folder_path = self.folder_path.get()
        if not folder_path or not os.path.exists(folder_path):
            self.log_message("Error: Please select a valid folder first!\n", "error")
            return
            
        self.stop_processing = False
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Start processing in a separate thread
        processing_thread = threading.Thread(target=self.process_videos)
        processing_thread.daemon = True
        processing_thread.start()
        
    def stop_processing_func(self):
        self.stop_processing = True
        self.log_message("Processing stopped by user.\n", "info")
        self.stop_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)
        
    def process_videos(self):
        folder_path = self.folder_path.get()
        
        try:
            target_width = int(self.width_var.get())
            target_height = int(self.height_var.get())
        except ValueError:
            self.log_message("Error: Invalid resolution values. Using default 1920x1080.\n", "error")
            target_width, target_height = 1920, 1080
        
        # Find all video files
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v', '.webm']
        video_files = []
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    video_files.append(Path(root) / file)
        
        self.total_videos = len(video_files)
        self.processed_videos = 0
        
        self.total_progress['maximum'] = self.total_videos
        self.total_label.config(text=f"Overall Progress: 0/{self.total_videos}")
        
        if self.total_videos == 0:
            self.log_message("No video files found in the selected folder.\n", "info")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            return
        
        self.log_message(f"Found {self.total_videos} video files to process.\n", "info")
        self.log_message(f"Target resolution: {target_width}x{target_height}\n", "info")
        self.log_message(f"Video codec: {self.codec_var.get()}\n\n", "info")
        
        # Process each video
        for video_path in video_files:
            if self.stop_processing:
                break
                
            self.process_video(video_path, target_width, target_height)
            self.processed_videos += 1
            
            # Update total progress
            self.total_progress['value'] = self.processed_videos
            self.total_label.config(text=f"Overall Progress: {self.processed_videos}/{self.total_videos}")
            
        # Final message
        if self.stop_processing:
            self.log_message(f"\nProcessing interrupted. {self.processed_videos}/{self.total_videos} videos processed.\n", "info")
        else:
            self.log_message(f"\nProcessing complete! {self.processed_videos}/{self.total_videos} videos processed.\n", "info")
        
        # Reset buttons
        self.stop_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)
        
    def get_video_dimensions(self, video_path):
        """Get video dimensions using ffprobe"""
        try:
            cmd = [
                'ffprobe', 
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(video_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                info = json.loads(result.stdout)
                for stream in info.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        width = int(stream.get('width', 0))
                        height = int(stream.get('height', 0))
                        # Handle rotation metadata
                        rotation = 0
                        if 'tags' in stream and 'rotate' in stream['tags']:
                            try:
                                rotation = int(stream['tags']['rotate'])
                            except (ValueError, TypeError):
                                rotation = 0
                        if rotation in [90, 270]:
                            width, height = height, width  # Swap dimensions for rotated videos
                        return width, height
        except (subprocess.SubprocessError, FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as e:
            self.log_message(f"  WARNING: ffprobe failed: {str(e)}\n", "warning")
        
        return None, None
        
    def resize_with_ffmpeg(self, video_path, new_width, new_height, temp_path):
        """Resize video using ffmpeg directly - most reliable method"""
        try:
            # Get the video codec setting
            video_codec = self.codec_var.get()
            
            # Build the command - use proper file extension for temp file
            cmd = [
                'ffmpeg',
                '-i', f'"{video_path}"',  # Quote the input path to handle spaces
                '-vf', f'scale={new_width}:{new_height}:force_original_aspect_ratio=decrease,pad={new_width}:{new_height}:(ow-iw)/2:(oh-ih)/2',
                '-c:v', video_codec,
                '-c:a', 'copy',  # Copy audio without re-encoding
                '-y',  # Overwrite output file
                '-movflags', '+faststart',  # Enable streaming
                '-loglevel', 'error',  # Only show errors
                f'"{temp_path}"'  # Quote the output path to handle spaces
            ]
            
            # If using a compression codec, add some reasonable quality settings
            if video_codec in ['libx264', 'libx265']:
                # Insert before the output file path
                cmd.insert(-1, '-crf')
                cmd.insert(-1, '23')  # Good quality setting
                cmd.insert(-1, '-preset')
                cmd.insert(-1, 'medium')  # Balance between speed and compression
            
            self.log_message(f"  Executing: {' '.join(cmd)}\n", "debug")
            
            # Use shell=True on Windows to handle paths with spaces properly
            process = subprocess.Popen(
                ' '.join(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                shell=True  # Use shell to handle paths with spaces
            )
            
            # Wait for the process to complete
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_message(f"  FFmpeg error: {stderr}\n", "error")
                return False
                
            return True
            
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            self.log_message(f"  ERROR with ffmpeg execution: {str(e)}\n", "error")
            return False
        
    def process_video(self, video_path, target_width, target_height):
        self.log_message(f"Processing: {video_path}\n", "info")
        
        # Create a temporary file with the same extension as the original
        temp_dir = tempfile.gettempdir()
        original_extension = os.path.splitext(video_path)[1]
        temp_filename = os.path.basename(video_path) + ".tmp" + original_extension
        temp_path = os.path.join(temp_dir, temp_filename)
        
        # If the path is too long, use a shorter name
        if len(temp_path) > 240:  # Windows path limit is 260 characters
            import uuid
            short_name = str(uuid.uuid4())[:8] + ".tmp" + original_extension
            temp_path = os.path.join(temp_dir, short_name)
        
        try:
            # Get video dimensions
            original_width, original_height = self.get_video_dimensions(video_path)
            
            if original_width is None or original_height is None:
                self.log_message(f"  ERROR: Could not get video dimensions\n", "error")
                return
                
            self.log_message(f"  Original dimensions: {original_width}x{original_height}\n", "info")
                
            # Check if video needs processing
            if original_width <= target_width and original_height <= target_height:
                self.log_message(f"  SKIPPED: Video is already smaller than target size\n", "skip")
                return
                
            # Calculate new dimensions while maintaining aspect ratio
            ratio = min(target_width / original_width, target_height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Ensure even dimensions (required by some codecs) 
            new_width = new_width if new_width % 2 == 0 else new_width - 1
            new_height = new_height if new_height % 2 == 0 else new_height - 1
            
            self.log_message(f"  Resizing to: {new_width}x{new_height}\n", "info")
            
            # Update current video progress
            self.current_label.config(text=f"Current Video: {os.path.basename(video_path)}")
            self.current_progress['value'] = 0
            
            # Resize the video using ffmpeg
            if not self.resize_with_ffmpeg(video_path, new_width, new_height, temp_path):
                self.log_message(f"  ERROR: Failed to resize video\n", "error")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return
            
            # Verify the output file was created
            if not os.path.exists(temp_path):
                self.log_message(f"  ERROR: Temporary file was not created\n", "error")
                return
                
            # Check the output dimensions
            output_width, output_height = self.get_video_dimensions(temp_path)
            if output_width and output_height:
                self.log_message(f"  Output dimensions: {output_width}x{output_height}\n", "info")
                
                # Verify the resize worked
                if abs(output_width - new_width) > 2 or abs(output_height - new_height) > 2:
                    self.log_message(f"  WARNING: Output dimensions don't match target\n", "warning")
            
            # Replace original file
            # First, back up the original file
            backup_path = str(video_path) + ".bak"
            try:
                shutil.copy2(video_path, backup_path)
                # Replace the original with the resized version
                shutil.move(temp_path, video_path)
                # Remove the backup
                os.remove(backup_path)
            except Exception as e:
                self.log_message(f"  ERROR during file replacement: {str(e)}\n", "error")
                # Try to restore from backup if possible
                if os.path.exists(backup_path):
                    try:
                        shutil.move(backup_path, video_path)
                    except:
                        pass
                return
            
            self.log_message(f"  SUCCESS: Resized and overwritten original file\n", "success")
            
        except Exception as e:
            self.log_message(f"  ERROR: {str(e)}\n", "error")
            # Clean up temporary file if it exists
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            
        finally:
            # Reset current progress bar
            self.current_progress['value'] = 0
            self.current_label.config(text="Current Video: Completed")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoResizerApp(root)
    root.mainloop()