# Clipster
 A Python script that creates a new video from a folder of video files, by randomly choosing and trimming clips of a specified length, and joining them with smooth crossfade effects. The output video is 720p 30fps and can be customized by setting the maximum clip length and total length. Great for making fun and creative video compilations.
# Project README

## Introduction

This project implements a video remix generator that creates a new video by combining clips from a specified input folder. The code utilizes various Python libraries such as `os`, `random`, `moviepy.editor`, and `PySimpleGUI` to accomplish this task.

## Functionality

The code follows the following steps to generate the remix video:

1. **Importing Dependencies**: The necessary modules, including `os`, `random`, `moviepy.editor`, and `PySimpleGUI`, are imported.

2. **Defining the Function**: The code defines a function called `generate_remix_video` that accepts four parameters: `input_folder`, `output_file`, `max_clip_length`, and `max_total_length`.

3. **Retrieving Video Files**: An empty list called `video_files` is created. The code uses `os.walk` to iterate over the files in the `input_folder` and appends the file paths of the video files ending with `.mp4`, `.avi`, or `.mov` extensions to the `video_files` list.

4. **Shuffling Video Files**: The `video_files` list is shuffled using `random.shuffle` to introduce randomness in the video selection process.

5. **Initializing Variables**: The code creates an empty list called `clips` and initializes a variable named `total_length` to zero. Additionally, a variable named `delay` is set to one second, representing the duration of the crossfade transition between clips.

6. **Generating Clips**: The code loops over the `video_files` list as long as it is not empty and the `total_length` is less than the `max_total_length`. In each iteration, a random video file is selected from the list using `random.choice`, and it is removed from the list using `list.remove`. The code creates a `VideoFileClip` object from the video file using `moviepy.editor` and retrieves its duration.

   - If the duration of the video is greater than the `max_clip_length`, a start time is randomly chosen between zero and the duration minus the `max_clip_length` using `random.uniform`. The end time is obtained by adding the `max_clip_length` to the start time. The code creates a subclip using the `subclip` method with the start and end times as arguments. The duration, fps, and height of the subclip are set using the `set_duration`, `set_fps`, and `resize` methods, respectively. A crossfadein effect is added to the subclip using the `crossfadein` method with the `delay` as an argument. Finally, the subclip is appended to the `clips` list, and the duration of the subclip is added to the `total_length`.

7. **Concatenating Clips**: After exiting the loop, all the clips in the `clips` list are concatenated using the `concatenate_videoclips` function from `moviepy.editor`. The `padding` parameter is set to a negative `delay`, and the `method` parameter is set to `compose`. This process creates a `final_clip` object with crossfade transitions between each clip.

8. **Writing the Output**: The `final_clip` object is written to a video file using the `write_videofile` method with `output_file` and `fps` as arguments.

9. **User Interface**: The code creates a PySimpleGUI window with input fields for selecting an input folder, setting a maximum clip length, setting a maximum total length, choosing an output file name, and a button for generating the video.

10. **Event Loop**: The code enters an event loop that reads user inputs from the window. If the user closes the window, the loop

 is broken. If the user clicks on the "Generate Video" button, the values from each input field are retrieved and assigned to variables. The code checks if the input folder is valid using `os.path.isdir`. If the folder is invalid, an error popup is displayed using `sg.popup_error`. If the folder is valid, the `generate_remix_video` function is called with the input variables. Upon successful video generation, a success popup is displayed using `sg.popup`.

## Limitations and Considerations

The code has the following limitations and details:

- **Supported Video Formats**: The code only supports video files with `.mp4`, `.avi`, or `.mov` extensions. Other formats may not work correctly or may cause errors.

- **Audio Track Assumption**: The code assumes that all video files in the input folder have audio tracks. Videos without audio may result in synchronization issues or silent gaps in the output video.

- **Resolution and Frame Rate**: The code converts all video clips to a standardized resolution of 720p and a frame rate of 30fps, regardless of their original resolution or frame rate. This may lead to quality loss or distortion in some videos.

- **Error Handling**: The code lacks comprehensive error handling or exception handling mechanisms. If any issues arise during the processing or writing of videos, the code may crash or produce corrupted output files.

It's important to be aware of these limitations and adapt the code accordingly to suit specific project requirements or constraints.
