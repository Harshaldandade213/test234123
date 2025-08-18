# auto_play_podcast.py
import os
import subprocess
import time
import platform

def play_audio_files_automatically():
    """
    Automatically plays all podcast audio files in sequence using the system's default audio player.
    """
    print("🎵 AUTO-PLAYING PODCAST AUDIO FILES")
    print("=" * 50)
    
    # Get all audio files in the current directory
    audio_files = []
    for file in os.listdir('.'):
        if file.startswith('podcast_output_') and file.endswith('.mp3'):
            audio_files.append(file)
    
    # Sort files by the number in their filename
    audio_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
    
    if not audio_files:
        print("❌ No podcast audio files found!")
        return
    
    print(f"📁 Found {len(audio_files)} audio files")
    print("🎵 Playing all files automatically...")
    print("Press Ctrl+C to stop playback")
    
    # Determine the system and appropriate command
    system = platform.system()
    
    try:
        for i, audio_file in enumerate(audio_files, 1):
            print(f"\n�� Playing segment {i}/{len(audio_files)}: {audio_file}")
            
            if system == "Windows":
                # Use start command to open with default player
                subprocess.run(['start', audio_file], shell=True, check=True)
            elif system == "Darwin":  # macOS
                # Use open command
                subprocess.run(['open', audio_file], check=True)
            else:  # Linux
                # Use xdg-open
                subprocess.run(['xdg-open', audio_file], check=True)
            
            # Wait a bit before playing the next file
            time.sleep(0.5)
            
        print(f"\n🎉 All {len(audio_files)} audio segments have been launched!")
        print("💡 Each file will play in your default audio player")
        print("�� Play them in order for the complete podcast experience")
        
    except KeyboardInterrupt:
        print("\n⏹️ Playback stopped by user")
    except Exception as e:
        print(f"\n❌ Error during playback: {e}")

if __name__ == "__main__":
    play_audio_files_automatically()
