import cv2

def findObjectInImage(img_url: str) -> bool:
    img = cv2.imread(img_url)
    original = img.copy()

    # Convert to grayscale
    gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blur = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)

    # Edge detection
    edges = cv2.Canny(image=blur, threshold1=50, threshold2=150)
    
    # Find contours
    contours, _ = cv2.findContours(image=edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    box_found = False

    for cnt in contours:
        # area = cv2.contourArea(cnt)
        # if area < 5000:
        #     continue  # ignore small objects

        # Approximate shape
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

        # Box-like shape → 4 corners
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)

            # Optional aspect ratio check
            aspect_ratio = w / float(h)
            if 0.5 < aspect_ratio < 2.0:
                cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 3)
                box_found = True

    if box_found:
        print(f"{img_url} has a match!")
    else:
        print(f"{img_url} not a match.")
    
    cv2.imshow("Detected Box", original)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return box_found

def main():
    images = [
        "img/test1_fail.jpeg",
        "img/test2_fail.jpeg"
    ]

    result = [findObjectInImage(image) for image in images]

if __name__ == "__main__":
    main()