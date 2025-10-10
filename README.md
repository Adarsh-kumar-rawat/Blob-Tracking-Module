🧮 Dynamic Blob Text Overlay (TouchDesigner + OpenCV)

A TouchDesigner Script TOP that detects blobs in an image and displays animated text (like equations, words, or numbers) on them using OpenCV.

Each detected blob is outlined, connected with lines, and labeled with randomized text that updates over time — perfect for generative visuals, math art, or interactive installations.

🧩 Setup :

refer to this video - https://youtu.be/MQ2ErTH20-c?si=-FWNh0X2YHzjqbay


⚙️ Configuration & Customization

All major visual and behavior controls are defined at the top of the script.

🎛 Main Parameters
Variable	Description	Default
MIN_AREA	Minimum blob area (pixels). Smaller ones are ignored.	80

TEXT_SIZE	Size of the text displayed on each blob.	0.7

FRAME_INTERVAL	How often the text changes (in frames). For 30fps: 30 ≈ 1 second.	1

DISPLAY_MODE	What type of content appears on blobs ('equations', 'words', 'numbers', 'time', 'colors', 'names')	'equations'

🎨 Visual Customization Guide

Below are common tweaks you can make easily by editing or commenting lines in the script.

🟪 1. Change Blob Outline Color

Locate:

cv2.rectangle(out8, (x, y), (x+bw, y+bh), (200, 200, 200, 255), 1)


The tuple (200, 200, 200, 255) is RGBA (0–255 scale).
For example:

(255, 0, 0, 255)   # Red
(0, 255, 0, 255)   # Green
(0, 0, 255, 255)   # Blue
(215, 81, 239, 255) # Purple-ish


Increase the last number for full opacity.

🟦 2. Change Blob Center Dot

Locate:

cv2.circle(out8, (cx, cy), 4, (255, 255, 255, 255), -1)


Change the radius 4 to make the dot larger/smaller.

Change (255, 255, 255, 255) to alter the color.

Example for cyan dots: (0, 255, 255, 255)

🟨 3. Change Connecting Line Color

Locate:

cv2.line(out8, centers[i], centers[i+1], (215, 81, 239, 255), 1)


(215, 81, 239, 255) controls line color (purple).

Change thickness 1 → 2 for bolder lines.

Example:

(255, 255, 0, 255)  # Yellow
(0, 255, 128, 255)  # Aqua Green


To disable lines entirely, comment it out:

# cv2.line(out8, centers[i], centers[i+1], (215, 81, 239, 255), 1)

🟩 4. Change Text Color or Add Shadow

cv2.putText(out8, text_content, (text_x+1, text_y+1), font, font_scale, (0, 0, 0, 255), thickness)

Uncomment and edit this line to get shadows:

# cv2.putText(out8, text_content, (text_x, text_y), font, font_scale, (0, 0, 255, 255), thickness)


Example:

(255, 255, 255, 255) → White text

(255, 0, 0, 255) → Red text

(0, 255, 255, 255) → Cyan text


🟥 5. Mirror Text

By default, the text is mirrored vertically (to match TouchDesigner’s flipped texture coordinates)
comment out the following two lines to get mirror text:

# src8 = cv2.flip(src8, 0)
# out8 = cv2.flip(out8, 0)


⚫ 6. Ignore Tiny Blobs

Control this with:

MIN_AREA = 80


Increase to ignore more small details, e.g.:

MIN_AREA = 150

⚙️ 7. Slow Down or Speed Up Text Updates

Text refreshes every few frames.
At the top:

FRAME_INTERVAL = 30


1 → changes every frame (fast)

30 → every ~1 second at 30 FPS

60 → every ~2 seconds

RECOMMENDED - 5 to 10

🧑‍💻 Example Creative Use Cases

Generative math visuals

Audio-reactive projections

“Hacker code rain” aesthetic

Conceptual educational art

Kinetic typography

📜 License
MIT License — free to use and modify
Credit to the creator - Adarsh Kumar Rawat aka IMSANZU
