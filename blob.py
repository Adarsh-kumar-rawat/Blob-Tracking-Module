import cv2   
import numpy as np

MIN_AREA = 80   # ignore tiny blobs

def onCook(scriptOp):
    # 1) Get input image
    src = scriptOp.inputs[0].numpyArray(delayed=False)   # float32 RGBA 0..1
    src8 = (src * 255).astype('uint8')                   # convert to uint8
    gray = src8[..., 0]                                  # single channel

    # 2) Threshold to binary
    _, binimg = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 3) Find contours (blobs)
    contours, _ = cv2.findContours(binimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4) Prepare output image (same size as input)
    h, w = gray.shape
    out8 = np.zeros((h, w, 4), dtype=np.uint8)

    # 5) Loop over each blob and draw bounding boxes
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < MIN_AREA:
            continue   # skip small specks

        # bounding box
        x, y, bw, bh = cv2.boundingRect(cnt)
        
        #change colour and thickness
        cv2.rectangle(out8, (x, y), (x+bw, y+bh), (255, 255, 255, 255), 1)

        # blob center
        cx = x + bw // 2
        cy = y + bh // 2
        #cv2.circle(out8, (cx, cy), 4, (255, 255, 255, 255), -1)

    # 6) Convert back to float32 0..1 for TOP output
    scriptOp.copyNumpyArray(out8.astype(np.float32) / 255.0)
    return
