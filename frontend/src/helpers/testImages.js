function getTestImageSet() {
  const imageIdentifiers = [
    ['lym0', 'lym17'],
    ['neu0', 'neu12', 'neu90'],
    ['agg17', 'agg23', 'agg185'],
    ['neurblas5', 'neurblas16', 'neurblas10', 'normal2', 'normal4']
  ];

  let testImages = [];
  imageIdentifiers.forEach((arr, idx) => {
    const randIdx = Math.floor(Math.random() * imageIdentifiers[idx].length);
    testImages.push(imageIdentifiers[idx][randIdx]);
  });
  return testImages;
}

export {
  getTestImageSet,
};