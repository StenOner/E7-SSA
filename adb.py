from ppadb.client import Client as AdbClient

BASE_SCREENSHOT_PATH: str = 'screenshots'
SELECTED_DEVICE: any

def main():
    client = AdbClient(host='127.0.0.1', port=5037)
    devices = client.devices()

    if not devices:
        raise RuntimeError('No ADB devices found')

    print(' ───────────\n','|','Devices','|','\n ───────────')
    for index, d in enumerate(devices):
        print(f'{index+1}.', d.serial)

    invalid = True
    while invalid:
        try:
            device_index = int(input('Select a device: '))

            global SELECTED_DEVICE
            SELECTED_DEVICE = devices[device_index-1]
            invalid = False
        except:
            print('Invalid index or value.')

    take_screenshot()

def take_screenshot() -> str:
    screenshot_name = generate_random_name()
    with open(f"{BASE_SCREENSHOT_PATH}/{screenshot_name}", 'wb') as f:
        f.write(SELECTED_DEVICE.screencap())

    return screenshot_name

def generate_random_name() -> str:
    from uuid import uuid4
    file_name: str = str(uuid4())

    return f"{file_name}.png"

if __name__ == '__main__':
    main()