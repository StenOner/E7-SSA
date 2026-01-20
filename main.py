import cv2
import numpy as np

IMAGE_BASE_PATH = "images/"

# Using template matching for "Buy" button
def detect_by_buy_button(img_name: str, button_template_path=None):
    img = cv2.imread(f"{IMAGE_BASE_PATH}{img_name}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if button_template_path:
        template = cv2.imread(button_template_path, 0)
        w, h = template.shape[::-1]
        
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        
        matches = []
        for pt in zip(*loc[::-1]):
            matches.append(pt)
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        
        print(f"Found {len(matches)} Buy buttons")
        cv2.imshow('Detected Buttons', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return matches
    
# Text detection
def detect_shop_items_robust(img_name: str):
    img = cv2.imread(f"{IMAGE_BASE_PATH}{img_name}")
    resized = cv2.resize(src=img, dsize=(1280, 720), interpolation=cv2.INTER_AREA)
    
    # Detect "Buy" button regions using color-based detection
    hsv = cv2.cvtColor(src=resized, code=cv2.COLOR_BGR2HSV)
    
    # Green color range for the Buy button
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(src=hsv, lowerb=lower_green, upperb=upper_green)

    # Blue mask to exclude when inside of button
    blue_lower = np.array([90, 50, 50])
    blue_upper = np.array([130, 255, 255])
    mask_blue = cv2.inRange(src=hsv, lowerb=blue_lower, upperb=blue_upper)
    
    # Find contours
    contours, _ = cv2.findContours(image=mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    
    buy_buttons = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Filter small contours
            x, y, w, h = cv2.boundingRect(contour)

            roi_blue = mask_blue[y:y+h, x:x+w]
            blue_pixels = cv2.countNonZero(roi_blue)
            aspect_ratio = w / float(h)

            if 1.5 < aspect_ratio < 4.0 and blue_pixels == 0:
                buy_buttons.append((x, y, w, h))
    
    print(f"Found {len(buy_buttons)} items")
    
    # Draw rectangles around detected items
    for (x, y, w, h) in buy_buttons:
        # Draw the buy button
        cv2.rectangle(resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Estimate the full item region (extending left from the button)
        item_x = max(0, x - 650)
        item_y = max(0, y - 60)
        item_w = x - item_x + w
        item_h = h + 80
        cv2.rectangle(resized, (item_x, item_y), (item_x + item_w, item_y + item_h), (255, 0, 0), 2)
    
    cv2.imshow('Detected Items', resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return buy_buttons

def main():
    images = [
        "test1_fail.jpeg",
        "test2_fail.jpeg",
        "test1_success_achieved.jpg",
        "test2_success_achieved.jpg",
    ]

    result2 = [detect_by_buy_button(image) for image in images] # needs template
    result3 = [detect_shop_items_robust(image) for image in images]

if __name__ == "__main__":
    main()