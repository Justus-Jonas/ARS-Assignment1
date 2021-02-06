import os
import moviepy.video.io.ImageSequenceClip


images='images/'
fps=10

image_files = [images+'/'+img for img in os.listdir(images) if img.endswith(".png")]
video = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
video.write_videofile('GradienDescent.mp4')