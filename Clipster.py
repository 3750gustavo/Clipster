import os
import random
import moviepy.editor as mp
import PySimpleGUI as sg

def generate_remix_video(input_folder, max_clip_length, max_total_length):
    video_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov')):
                video_files.append(os.path.join(root, file))

    if not video_files:
        raise ValueError("No video files found in the selected folder.")

    random.shuffle(video_files)

    clips = []
    total_length = 0
    delay = 1  # tempo de transição em segundos

    while video_files and total_length < max_total_length:
        video_file = random.choice(video_files)
        video_files.remove(video_file)
        try:
            video = mp.VideoFileClip(video_file)
        except Exception as e:
            print(f"Error processing video file: {video_file}")
            print(f"Error message: {str(e)}")
            continue

        duration = video.duration

        if duration > max_clip_length:
            start_time = random.uniform(0, duration - max_clip_length)
            end_time = start_time + max_clip_length
            subclip = video.subclip(start_time, end_time)
            subclip = subclip.set_duration(max_clip_length).set_fps(30).resize(height=720)
            subclip = subclip.crossfadein(delay)  # adiciona a transição Crossfadeout
            clips.append(subclip)
            total_length += end_time - start_time

    return mp.concatenate_videoclips(clips, padding=-delay, method="compose")  # concatena os clipes com o método compose

def main():
    sg.theme('DarkBlue3')

    layout = [
        [sg.Text('Select Input Folder')],
        [sg.Input(key='-INPUT-', enable_events=True), sg.FolderBrowse()],
        [sg.Text('Max Clip Length'), sg.Input(key='-MAX_CLIP_LENGTH-')],
        [sg.Text('Max Total Length'), sg.Input(key='-MAX_TOTAL_LENGTH-')],
        [sg.Button('Generate Video')],
    ]

    window = sg.Window('Video Remix Generator', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Generate Video':
            input_folder = values['-INPUT-']
            max_clip_length = values['-MAX_CLIP_LENGTH-']
            max_total_length = values['-MAX_TOTAL_LENGTH-']

            if not input_folder or not os.path.isdir(input_folder):
                sg.popup_error('Invalid input folder!', title='Error')
                continue

            try:
                max_clip_length = float(max_clip_length)
                max_total_length = float(max_total_length)
            except ValueError:
                sg.popup_error('Invalid input for max clip length or max total length. Please enter valid numeric values.', title='Error')
                continue

            try:
                final_clip = generate_remix_video(input_folder, max_clip_length, max_total_length)
            except ValueError as e:
                sg.popup_error(str(e), title='Error')
                continue
            except Exception as e:
                sg.popup_error('An error occurred during video generation. Please check the input folder and try again.', title='Error')
                print(f"Error message: {str(e)}")
                continue

            if final_clip:
                folder_name = os.path.basename(input_folder)
                default_name = folder_name + '_remix.mp4'
                save_path = sg.popup_get_file('Save Remix Video As', default_extension='.mp4', default_path=default_name, save_as=True)
                if save_path:
                    try:
                        final_clip.write_videofile(save_path, codec='libx264', fps=30)
                        sg.popup('Video generated successfully!', title='Success')
                    except Exception as e:
                        sg.popup_error('An error occurred while saving the video. Please check the save path and try again.', title='Error')
                        print(f"Error message: {str(e)}")
                else:
                    sg.popup('Operation cancelled!', title='Cancelled')

    window.close()

if __name__ == '__main__':
    main()