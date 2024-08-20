import subprocess
## Enter the path to the audio file here
src_audio = r"D:\PORJECT\Animism\Allium\hh.wav"

subprocess.run(f'python D:\PORJECT\Animism\Allium\\tools\\fish-speech-1.2\\tools\\vqgan/inference.py \
    -i {src_audio} \
    --checkpoint-path "D:\PORJECT\Animism\models\\fish-speech-1.2-sft/firefly-gan-vq-fsq-4x1024-42hz-generator.pth"')

from IPython.display import Audio, display
audio = Audio(filename=src_audio)
display(audio)
subprocess.run('python D:\PORJECT\Animism\Allium\\tools\\fish-speech-1.2\\tools\\llama/generate.py \
                --text "你好" \
                --prompt-text "The text corresponding to reference audio" \
                --prompt-tokens "fake.npy" \
                --checkpoint-path "D:\PORJECT\Animism\models\\fish-speech-1.2-sft/fish-speech-1.2-sft" \
                --num-samples 2')
subprocess.run('python D:\PORJECT\Animism\Allium\\tools\\fish-speech-1.2\\tools\\vqgan/inference.py \
                -i "codes_0.npy" \
                --checkpoint-path "D:\PORJECT\Animism\models\\fish-speech-1.2-sft/firefly-gan-vq-fsq-4x1024-42hz-generator.pth"')
from IPython.display import Audio, display
audio = Audio(filename=src_audio)
display(audio)