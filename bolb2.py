import cv2   
import numpy as np
import random

MIN_AREA = 80      # ignore tiny blobs
TEXT_SIZE = 0.7   # control text size (0.3 = small, 0.5 = medium, 0.8 = large)

# SPEED CONTROL: update every N frames
# 10 = changes every 10 frames
# 30 = changes every 30 frames (roughly 1 second at 30fps)
# 60 = changes every 60 frames (roughly 2 seconds at 30fps)
FRAME_INTERVAL = 1
# This won't change the generation speed but will create a small delay between generation 

# Choose what to display: 'equations', 'words', 'numbers', 'time', 'colors', 'names'
DISPLAY_MODE = 'equations'

# Store text persistently across frames
blob_text = {}
frame_count = 0

def generate_random_content():
    """Generate random content based on DISPLAY_MODE"""
    
    if DISPLAY_MODE == 'equations':
        operators = ['+', '-', '×', '÷']
        options = [
            f"{random.randint(1, 99)} {random.choice(operators)} {random.randint(1, 99)}",
            f"x² {random.choice(['+', '-'])} {random.randint(1, 20)}",
            f"√{random.randint(1, 100)}",
            f"{random.randint(1, 20)}x = {random.randint(1, 100)}",
            f"∫x dx",
            f"π × {random.randint(1, 20)}",
            f"e^{random.randint(1, 5)}",
            f"{random.randint(1, 10)}! = ?",
        ]
    
    elif DISPLAY_MODE == 'words':
        options = [
            "HELLO", "WORLD", "LIGHT", "SOUND", "WAVE", "PULSE",
            "FLOW", "GLOW", "BEAM", "SPARK", "FLUX", "DRIFT",
            "ECHO", "VOID", "AURA", "RIFT", "NOVA", "SYNC"
        ]
    
    elif DISPLAY_MODE == 'numbers':
        options = [
            f"{random.randint(0, 999)}",
            f"{random.randint(0, 99):02d}",
            f"{random.random():.2f}",
            f"{random.randint(1000, 9999)}",
            f"#{random.randint(1, 999)}"
        ]

    elif DISPLAY_MODE == 'time':
        h = random.randint(0, 23)
        m = random.randint(0, 59)
        options = [f"{h:02d}:{m:02d}"]
    
    elif DISPLAY_MODE == 'colors':
        options = [
            "RED", "BLUE", "GREEN", "CYAN", "PINK",
            "YELLOW", "ORANGE", "PURPLE", "WHITE", "VIOLET",
            "CRIMSON", "AZURE", "LIME", "CORAL", "INDIGO"
        ]
    
    elif DISPLAY_MODE == 'names':
        options = [
            "ALPHA", "BETA", "GAMMA", "DELTA", "OMEGA",
            "ZETA", "THETA", "SIGMA", "PHI", "PSI",
            "NOVA", "LUNA", "SOLAR", "ASTRA", "COSMO"
        ]
    
    else:
        options = ["???"]
    
    return random.choice(options)

def onCook(scriptOp):
    global frame_count
    frame_count += 1
    
    # 1) Get input image
    src = scriptOp.inputs[0].numpyArray(delayed=False)   # float32 RGBA 0..1
    src8 = (src * 255).astype('uint8')                   # convert to uint8
    src8 = cv2.flip(src8, 0) #Comment out this and line 147 if you want mirror text
    gray = src8[..., 0]                                  # single channel
    
    # 2) Threshold to binary
    _, binimg = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # 3) Find contours (blobs)
    contours, _ = cv2.findContours(binimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 4) Prepare output image (same size as input)
    h, w = gray.shape
    out8 = np.zeros((h, w, 4), dtype=np.uint8)
    
    # 5) Loop over each blob and draw bounding boxes + centers + equations
    centers = []
    for idx, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area < MIN_AREA:
            continue   # skip small specks
        
        # bounding box
        x, y, bw, bh = cv2.boundingRect(cnt)
        cv2.rectangle(out8, (x, y), (x+bw, y+bh), (200, 200, 200, 255), 1)
        
        # blob center
        cx = x + bw // 2
        cy = y + bh // 2
        centers.append((cx, cy))
        cv2.circle(out8, (cx, cy), 4, (255, 255, 255, 255), -1)
        
        # Generate or retrieve content based on FRAME_INTERVAL
        if frame_count % FRAME_INTERVAL == 0:
            blob_text[idx] = generate_random_content()
        
        text_content = blob_text.get(idx, "")
        
        # Draw equation text inside the bounding box
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = TEXT_SIZE
        thickness = 1
        
        # Get text size to center it
        (text_w, text_h), baseline = cv2.getTextSize(text_content, font, font_scale, thickness)
        
        # Position text in center of bounding box
        text_x = x + (bw - text_w) // 2
        text_y = y + (bh + text_h) // 2

        # Ensure text stays within bounds
        text_x = max(x + 2, min(text_x, x + bw - text_w - 2))
        text_y = max(y + text_h + 2, min(text_y, y + bh - 2))
        
        # Draw text with a slight shadow for better visibility
        cv2.putText(out8, text_content, (text_x+1, text_y+1), font, font_scale, (0, 0, 0, 255), thickness)
        #cv2.putText(out8, text_content, (text_x, text_y), font, font_scale, (0, 0 , 255, 255), thickness)
        # UnComment out the above line if you want shadow in text
    
    # 6) Draw connecting lines between consecutive centers
    for i in range(len(centers)-1):
        cv2.line(out8, centers[i], centers[i+1], (215, 81, 239, 255), 1)
    
    # 7) Flip output back to correct orientation
    out8 = cv2.flip(out8, 0)
    
    # 8) Convert back to float32 0..1 for TOP output
    scriptOp.copyNumpyArray(out8.astype(np.float32) / 255.0)
    return
