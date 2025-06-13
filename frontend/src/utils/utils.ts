export const isBright = (hex: string) => {
    var hex = hex.substring(1);
    var rgb = parseInt(hex, 16);
    var r = (rgb >> 16) & 0xff;
    var g = (rgb >> 8) & 0xff;
    var b = (rgb >> 0) & 0xff;

    var luma = 0.2126 * r + 0.7152 * g + 0.0722 * b; // per ITU-R BT.709

    return luma > 127
}
