# fix_indentation_complete.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Split into lines
lines = content.split('\n')

# Find the problematic section and fix it completely
for i, line in enumerate(lines):
    if 'success, audio_files = generate_podcast_audio_simple(script_text, output_filename)' in line:
        # Fix the entire else block structure
        lines[i] = '        success, audio_files = generate_podcast_audio_simple(script_text, output_filename)'
        lines[i+1] = '        if success:'
        lines[i+2] = '            if len(audio_files) == 1:'
        lines[i+3] = '                print("\\n PODCAST GENERATION COMPLETE!")'
        lines[i+4] = '                print(f" Single audio file: {audio_files[0]}")'
        lines[i+5] = '                print("🎵 You can now play the complete podcast!")'
        lines[i+6] = '            else:'
        lines[i+7] = '                print("\\n PODCAST GENERATION COMPLETE!")'
        lines[i+8] = '                print("📁 Individual audio files generated")'
        lines[i+9] = '                print("🎵 You can play the individual audio files or combine them manually")'
        lines[i+10] = ''
        lines[i+11] = '            # Ask user if they want to play the audio'
        lines[i+12] = '            try:'
        lines[i+13] = '                play_choice = input("\\n🎵 Would you like to play the complete podcast now? (y/n): ").lower().strip()'
        lines[i+14] = '                if play_choice == "y":'
        lines[i+15] = '                    play_audio_sequence(output_filename, audio_files)'
        lines[i+16] = '            except KeyboardInterrupt:'
        lines[i+17] = '                print("\\n⏹️ Skipping playback")'
        lines[i+18] = '        else:'
        lines[i+19] = '            print("\\n❌ Podcast generation failed at audio stage.")'
        break

# Write the fixed content back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Fixed complete indentation structure in app.py")
