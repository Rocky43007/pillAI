extern crate image;
extern crate imageproc;

use image::{GenericImageView, RgbaImage};
use imageproc::drawing::Canvas;
use imageproc::pixelops::weighted_sum;
use imageproc::rect::Rect;
use imageproc::region_labelling::connected_components_labeling;
use imageproc::rect::Region;

fn main() {
    let image_path = "/Users/achakra/Downloads/test_drug.jpg";
    let img = image::open(image_path).expect("Failed to open image");

    let mut output = RgbaImage::new(img.width(), img.height());

    let threshold = 200;

    for (x, y, pixel) in img.pixels() {
        let intensity = weighted_sum(pixel.channels(), &[0.299, 0.587, 0.114]);
        let label = if intensity > threshold { 1 } else { 0 };
        output.put_pixel(x, y, image::Rgba([label as u8, 0, 0, 255]));
    }

    let mut components = Vec::new();
    connected_components_labeling(&output, &mut components);

    for component in components {
        let bounding_rect = bounding_rect(&component);
        output.draw_hollow_rect(bounding_rect, image::Rgba([0, 255, 0, 255]));
    }

    output.save("output.png").expect("Failed to save output image");
}

fn bounding_rect(region: &Region) -> Rect {
    let mut min_x = std::i32::MAX;
    let mut min_y = std::i32::MAX;
    let mut max_x = std::i32::MIN;
    let mut max_y = std::i32::MIN;

    for point in &region.points {
        min_x = min_x.min(point[0] as i32);
        min_y = min_y.min(point[1] as i32);
        max_x = max_x.max(point[0] as i32);
        max_y = max_y.max(point[1] as i32);
    }

    Rect::at(min_x, min_y).of_size((max_x - min_x + 1) as u32, (max_y - min_y + 1) as u32)
}
