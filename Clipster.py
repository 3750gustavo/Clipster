import copy
import os
import random
import moviepy.editor as mp
import PySimpleGUI as sg

def generate_remix_video(input_folder, max_clip_length, max_total_length):
    video_files = []

    # Dicionário para armazenar os trechos usados, cada entrada é um par (video_file, [(start_time, end_time), ...])
    # Exemplo: {'video1.mp4': [(0.0, 10.0), (20.0, 30.0)], 'video2.mp4': [(5.0, 15.0)]}
    # se um trecho para video1.mp4 for de por exemplo 8.0 a 12.0, ele entraria em conflito com o trecho (0.0, 10.0) já usado, já que
    # 8.0 a 10.0 faz parte do trecho de um dos trechos já usados
    used_clips = {}

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov')):
                video_files.append(os.path.join(root, file))

    if not video_files:
        raise ValueError("No video files found in the selected folder.")

    for video_file in video_files:
        used_clips[video_file] = []  # Inicializa a lista de trechos usados para cada vídeo
    random.shuffle(video_files)

    clips = []
    total_length = 0
    delay = 1  # tempo de transição em segundos
    temp_video_files = copy.deepcopy(video_files)

    while total_length < max_total_length:
        video_file = random.choice(temp_video_files) #video selecionado
        temp_video_files.remove(video_file)

        # se o ultimo video tiver sido removido, reinicia a lista de videos, pondo todos de volta
        if not temp_video_files:
            temp_video_files = copy.deepcopy(video_files)

        try:
            video = mp.VideoFileClip(video_file)
        except Exception as e:
            print(f"Error processing video file: {video_file}")
            print(f"Error message: {str(e)}")
            continue

        duration = video.duration

        if duration > max_clip_length:
            # trecho selecionado
            start_time = random.uniform(0, duration - max_clip_length)
            end_time = start_time + max_clip_length

            # Primeiro checa se o video selecionado sequer esta na lista de videos usados, se não tiver podemos assumer que todos trechos dele estão disponíveis
            if video_file not in used_clips:
                used_clips[video_file] = [(start_time, end_time)]
            else:
                # o video já foi usado, então precisamos checar se o trecho selecionado não está sobrepondo com algum trecho já usado
                overlapping = False
                for used_start, used_end in used_clips[video_file]:
                    if start_time < used_end and end_time > used_start:
                        overlapping = True
                        break

                if not overlapping:
                    # Se não houver sobreposição, adiciona o trecho à lista de trechos usados
                    used_clips[video_file].append((start_time, end_time))
                    subclip = video.subclip(start_time, end_time)
                    subclip = subclip.set_duration(max_clip_length).set_fps(30).resize(height=720)
                    subclip = subclip.crossfadein(delay)  # adiciona a transição Crossfadeout
                    clips.append(subclip)
                    total_length += end_time - start_time

    # for debugging purposes, prints all the used clips timestamps (start, end)
    for video_file, used in used_clips.items():
        print(f"Used clips for {video_file}: {used}")

    return mp.concatenate_videoclips(clips, padding=-delay, method="compose")  # concatena os clipes com o método compose

def main():
    sg.theme('DarkBlue3')

    default_input_folder = 'C:/path/to/your/video/folder'  # Replace with your default input folder
    default_max_clip_length = '10.0'  # Default max clip length in seconds
    default_max_total_length = '60.0'  # Default max total length in seconds

    layout = [
        [sg.Text('Select Input Folder')],
        [sg.Input(default_input_folder, key='-INPUT-', enable_events=True), sg.FolderBrowse()],
        [sg.Text('Max Clip Length'), sg.Input(default_max_clip_length, key='-MAX_CLIP_LENGTH-')],
        [sg.Text('Max Total Length'), sg.Input(default_max_total_length, key='-MAX_TOTAL_LENGTH-')],
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