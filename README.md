This is a AI that runs only in kitty's terminal

# Dependancies
You must have installed in pip
## ollama
```pip install ollama```
## sys
```pip install sys``` (if you don't have it already)
## subprocess
```pip install subprocess``` (if you don't have it already)

# How to execute
first to execute this script you must have an ollama llm installed to install it on linux you must do
```
sudo pacman -S ollama
ollama pull llama3.2:3b-instruct-q4_K_M
ollama serve 
```
once you're serving your ollama service you can try and run it
<img width="549" height="396" alt="imagen" src="https://github.com/user-attachments/assets/13cc70c0-13c6-4644-8ee8-b3548b59a81e" />

you should see this. once you see the Amadeus logo you can start prompting to the AI
