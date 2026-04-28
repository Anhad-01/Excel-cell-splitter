from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from playwright.sync_api import sync_playwright


WIDTH = 2160
HEIGHT = 2160
SCALE = 2


def render_html_slides(input_path: str) -> list[bytes]:
    html_path = Path(input_path).resolve()

    with TemporaryDirectory() as temp_dir:
        image_paths: list[Path] = []

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )

            try:
                context = browser.new_context(
                    viewport={"width": WIDTH, "height": HEIGHT},
                    device_scale_factor=SCALE,
                )
                page = context.new_page()

                page.goto(html_path.as_uri())
                page.wait_for_selector(".slide")

                total_slides = page.locator(".slide").count()
                if total_slides == 0:
                    raise ValueError("No elements with class '.slide' were found in the HTML.")

                for index in range(total_slides):
                    page.evaluate(
                        """
                        (activeIndex) => {
                            const slides = document.querySelectorAll('.slide');
                            slides.forEach((slide, idx) => {
                                slide.style.display = idx === activeIndex ? 'flex' : 'none';
                            });
                        }
                        """,
                        index,
                    )
                    page.wait_for_timeout(300)

                    image_path = Path(temp_dir) / f"slide_{index}.png"
                    page.locator(".frame").screenshot(path=str(image_path), type="png")
                    image_paths.append(image_path)
            finally:
                browser.close()

        if not image_paths:
            raise ValueError("No slide images were generated from the uploaded HTML.")

        return [image_path.read_bytes() for image_path in image_paths]


def save_slide_images_as_pdf(slide_images: list[bytes], output_path: str) -> str:
    pdf_path = Path(output_path).resolve()

    images = [Image.open(BytesIO(image_bytes)).convert("RGB") for image_bytes in slide_images]
    try:
        images[0].save(
            pdf_path,
            save_all=True,
            append_images=images[1:],
            resolution=300.0,
        )
    finally:
        for image in images:
            image.close()

    return str(pdf_path)


def convert_html_to_pdf(input_path: str, output_path: str) -> str:
    slide_images = render_html_slides(input_path)
    return save_slide_images_as_pdf(slide_images, output_path)
