import qrcode
import sys

def generate_qr(url, output_file='qr_code.png'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
    print(f"QR code saved as {output_file}")

if __name__ == "__main__":
    url = sys.argv[1]
    generate_qr(url)
