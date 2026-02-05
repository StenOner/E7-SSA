import cv2

IMAGE_BASE_PATH: str = 'images/'
DSIZE: tuple = (1280, 720)
CURRENT_GOLD: int = 0
CURRENT_SKYSTONES: int = 0

def detect_currencies(img_name: str):
    from paddleocr import PaddleOCR
    
    img = cv2.imread(f'{IMAGE_BASE_PATH}{img_name}')
    resized = cv2.resize(src=img, dsize=DSIZE, interpolation=cv2.INTER_AREA)
    cropped = resized[:60,700:960]
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        )

    result = ocr.predict(input=cropped)
    if not result or not result[0]:
        raise Exception('Could not find currencies')
    
    global CURRENT_GOLD, CURRENT_SKYSTONES
    [CURRENT_GOLD, CURRENT_SKYSTONES] = [int(currency.replace(',','')) for currency in result[0]['rec_texts']]