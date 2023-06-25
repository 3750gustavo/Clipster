import os
import random
import moviepy.editor as mp
import PySimpleGUI as sg

def generate_remix_video(input_folder, output_file, max_clip_length, max_total_length):
    video_files = []
    used_clips = {}  # Dicionário para armazenar os trechos usados
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov')):
                video_files.append(os.path.join(root, file))
                used_clips[os.path.join(root, file)] = []  # Inicializa a lista de trechos usados para cada vídeo
    random.shuffle(video_files)

    clips = []
    total_length = 0
    delay = 1  # tempo de transição em segundos

    while video_files and total_length < max_total_length:
        video_file = random.choice(video_files)
        video = mp.VideoFileClip(video_file)
        duration = video.duration

        if duration > max_clip_length:
            start_time = random.uniform(0, duration - max_clip_length)
            end_time = start_time + max_clip_length

            # Verifica se o trecho selecionado já foi usado
            for used_start, used_end in used_clips[video_file]:
                if not (end_time <= used_start or start_time >= used_end):
                    # Se o trecho já foi usado, pula para a próxima iteração do loop
                    continue

            # Adiciona o trecho à lista de trechos usados
            used_clips[video_file].append((start_time, end_time))

            subclip = video.subclip(start_time, end_time)
            subclip = subclip.set_duration(max_clip_length).set_fps(30).resize(height=720)
            subclip = subclip.crossfadein(delay)  # adiciona a transição Crossfadeout
            clips.append(subclip)
            total_length += end_time - start_time

    final_clip = mp.concatenate_videoclips(clips, padding=-delay, method="compose")  # concatena os clipes com o método compose
    final_clip.write_videofile(output_file, fps=30)

sg.theme('DefaultNoMoreNagging')

layout = [
    [sg.Text('Select Input Folder')],
    [sg.Input(key='-INPUT-', enable_events=True), sg.FolderBrowse()],
    [sg.Text('Max Clip Length'), sg.Input(key='-MAX_CLIP_LENGTH-')],
    [sg.Text('Max Total Length'), sg.Input(key='-MAX_TOTAL_LENGTH-')],
    [sg.Text('Output File'), sg.Input(key='-OUTPUT-', enable_events=True), sg.SaveAs()],
    [sg.Button('Generate Video')]
]

window = sg.Window('Video Remix Generator', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == 'Generate Video':
        input_folder = values['-INPUT-']
        max_clip_length = float(values['-MAX_CLIP_LENGTH-'])
        max_total_length = float(values['-MAX_TOTAL_LENGTH-'])
        output_file = values['-OUTPUT-']

        if not input_folder or not os.path.isdir(input_folder):
            sg.popup_error('Invalid input folder!')
            continue

        generate_remix_video(input_folder, output_file, max_clip_length, max_total_length)
        sg.popup('Video generated successfully!', title='Success')

window.close()