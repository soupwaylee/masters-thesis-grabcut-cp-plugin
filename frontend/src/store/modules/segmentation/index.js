import {APIService as grabcutAPIService} from "@/api/grabcutAPI";
import {getScribbleMaskContext, getScribblePixelCount} from "@/helpers/canvas";

// const grabcutAS = new grabcutAPIService();

const state = {
  /**
   * {
   *   "segmentationImageSrc": String,
   *   "thumbnailImageSrc": String,
   *   "segmentationMethod": String
   * }
   */
  segmentations: [],
};

const mutations = {
};

const actions = {
  getSegmentation({ state, commit, rootState }, imageData) {
    const interactionSessionState = rootState.interactionSessionModule;

    let {scribbleIndices, scribbleTypes} = getScribbleMaskContext(imageData);
    let {pixelCount, fgPixelCount, bgPixelCount} = getScribblePixelCount(scribbleIndices, scribbleTypes);

    let interactionRecord = {
      'sessionId': interactionSessionState.sessionId,
      'imageId': interactionSessionState.currentImageIndex,
      "scribbles": interactionSessionState.scribbles,
      "foregroundScribbles": interactionSessionState.foregroundScribbles,
      "backgroundScribbles": interactionSessionState.backgroundScribbles,
      "annotatedPixels": pixelCount,
      "foregroundPixels": fgPixelCount,
      "backgroundPixels": bgPixelCount,
      "submissionIndex": interactionSessionState.submissionCounter,
      "submissionTime": interactionSessionState.segmentationRequestTime,
    }

    console.table(interactionRecord);
    // grabcutAS.segmentImage()
  },
};

const getters = {

};

const segmentationModule = {
  state,
  mutations,
  actions,
  getters,
}

export default segmentationModule;