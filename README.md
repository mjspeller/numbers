# Number Learning App

A simple Docker-based web application to teach toddlers how to read numbers.

## Features

- Random number generation from 0 to user-selected maximum (0-1001, default 99)
- Large number display (70% of screen)
- Interactive correct/incorrect feedback with sounds and images
- Customizable backgrounds, feedback images, and sounds

## Folder Structure

```
images/
  ├── backgrounds/     # Background images for the main screen
  ├── correct/         # Image shown when "Correct" is clicked (use: image.jpg)
  └── incorrect/       # Image shown when "Incorrect" is clicked (use: image.jpg)

sounds/
  ├── correct/         # Sound played when "Correct" is clicked (use: sound.mp3)
  └── incorrect/       # Sound played when "Incorrect" is clicked (use: sound.mp3)
```

## Setup Instructions

### 1. Add Your Media Files

Add your custom images and sounds to the appropriate folders:

- **Backgrounds**: Add images to `images/backgrounds/` (named bg1.jpg, bg2.jpg, etc.)
- **Correct feedback**: Add `images/correct/image.jpg`
- **Incorrect feedback**: Add `images/incorrect/image.jpg`
- **Correct sound**: Add `sounds/correct/sound.mp3`
- **Incorrect sound**: Add `sounds/incorrect/sound.mp3`

### 2. Build and Run

```bash
docker-compose up --build
```

### 3. Access the App

Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Use the slider at the top to set the maximum number (0-1001)
2. Click "Start" to begin
3. A random number will appear
4. Click "✓ Correct" if the child reads it correctly
5. Click "✗ Incorrect" if they need to try again
6. The app will play the appropriate sound and show feedback
7. A new number appears automatically after 2 seconds

## Stopping the App

```bash
docker-compose down
```

## Quick Start (No Media Files)

The app will work even without custom media files - it will use a gradient background and skip sounds if files are missing.

## Optional: AI Voice (Kokoro TTS)

To enable AI voice that speaks feedback messages:

1. Download the Kokoro model: `git clone https://huggingface.co/hexgrad/Kokoro-82M ai_voice`
2. Rebuild the container: `docker-compose up --build`

If the `ai_voice/` folder is empty, the app runs normally without voice. The voice will speak the scrolling text (e.g., "Well done [name]!" or "Incorrect, the number was 42").
