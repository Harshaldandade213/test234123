# sequential_podcast_player.py
import os
import time
import pygame

def play_podcast_sequentially():
    """
    Plays all podcast audio files sequentially, waiting for each to finish.
    """
    print(" SEQUENTIAL PODCAST PLAYER")
    print("=" * 50)
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
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
    print("🎵 Playing files sequentially (waiting for each to finish)...")
    print("Press Ctrl+C to stop playback")
    
    try:
        for i, audio_file in enumerate(audio_files, 1):
            print(f"\n Playing segment {i}/{len(audio_files)}: {audio_file}")
            
            # Load and play the audio file
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for the audio to completely finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            print(f"  ✅ Completed segment {i}")
            
        print(f"\n🎉 Complete podcast playback finished!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Playback stopped by user")
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"\n❌ Error during playback: {e}")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    play_podcast_sequentially()
