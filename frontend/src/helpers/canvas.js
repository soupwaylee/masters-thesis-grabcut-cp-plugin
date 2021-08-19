const colorToPixelType = {
  'rgba(255, 0, 0, 1)': 'fg',
  'rgba(0, 0, 255, 1)': 'bg',
}

const pixelTypeToColor = {
  'fg': 'rgba(255, 0, 0, 1)',
  'bg': 'rgba(0, 0, 255, 1)',
}

function pixelDataToRgba(r, g, b, a) {
  return `rgba(${r}, ${g}, ${b}, ${(a / 255).toFixed(2)})`;
}

function getImageDataURIFromDataArray(imageDataArray, colormap, width, height) {
  const canvasElement = document.createElement('canvas');
  canvasElement.width = width;
  canvasElement.height = height;

  const canvasCtx = canvasElement.getContext('2d');
  const imageData = canvasCtx.getImageData(0, 0, canvasElement.width, canvasElement.height);

  for (const [idx, intVal] of imageDataArray.entries()) {
    let imageDataOffset = idx * 4;
    imageData.data.set(
      [colormap[intVal][0], colormap[intVal][1], colormap[intVal][2], 255],
      imageDataOffset);
  }

  canvasCtx.putImageData(imageData, 0, 0);
  return canvasElement.toDataURL();
}

/**
 * @typedef {Object} ScribbleContext
 * @property {number[]} scribbleIndices
 * @property {boolean[]} scribbleTypes
 */

/**
 * Compute the coordinates of the unraveled image data array
 * and an array that indicates whether the pixel is fg (true) or bg.
 * @param imageData {Uint8ClampedArray} containing the pixel data of the ImageData object of the user interaction canvas
 * @returns {ScribbleContext}
 */
function getScribbleMaskContext(imageData) {
  let scribbleIndices = [];
  let scribbleTypes = []

  let isWhite = true;

  for (let i = 0; i < imageData.length - 1; i += 4) {
    const [r, g, b,] = imageData.slice(i, i + 4);
    isWhite &&= (r === 0 && g === 0 && b === 0);
    if (isWhite) continue;

    let isForeground = colorToPixelType[`rgba(${r}, ${g}, ${b}, 1)`] === 'fg';

    scribbleIndices.push(i / 4);
    scribbleTypes.push(isForeground);
  }

  return {
    'scribbleIndices': scribbleIndices,
    'scribbleTypes': scribbleTypes,
  };
}

/**
 * @typedef {Object} AnnotationPixelContext
 * @property {number} pixelCount total number of pixels that had been scribbled
 * @property {number} fgPixelCount total number of foreground pixels that had been scribbled
 * @property {number} bgPixelCount total number of background pixels that had been scribbled
 */

/**
 * Compute the number of pixels that have been annotated as foreground or background.
 * @param scribbleIndices {number[]} A list of indices (based on an unraveled image array) with annotated pixels (scribbles).
 * @param scribbleTypes {boolean[]} A list of boolean values indicating whether the pixel isForeground.
 * @return {AnnotationPixelContext}
 */
function getScribblePixelCount(scribbleIndices, scribbleTypes) {
  let pixelCount = scribbleTypes.length;

  let {fgPixelCount, bgPixelCount} = scribbleTypes.reduce(
    function (countObject, isForeground) {
      let key = isForeground ? 'fgPixelCount' : 'bgPixelCount';
      countObject[key] = countObject[key] ? countObject[key] + 1 : 1;
      return countObject;
    },
    {
      'fgPixelCount': 0,
      'bgPixelCount': 0,
    }
  );

  return {
    'pixelCount': pixelCount,
    'fgPixelCount': fgPixelCount,
    'bgPixelCount': bgPixelCount,
  };
}

export {
  colorToPixelType,
  pixelTypeToColor,
  pixelDataToRgba,
  getImageDataURIFromDataArray,
  getScribbleMaskContext,
  getScribblePixelCount
};