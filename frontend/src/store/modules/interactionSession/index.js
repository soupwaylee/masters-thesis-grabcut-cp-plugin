const state = {
  testImages: null,

  sessionId: "",
  currentImageIndex: 0,
  currentImageFirstInteraction: true,
  currentImageInteractionStartingTime: null,
  previousScribbleType: null,
  scribbles: 0,
  foregroundScribbles: 0,
  backgroundScribbles: 0,
  pixelsAtSubmission: 0,
  foregroundPixelsAtSubmission: 0,
  backgroundPixelsAtSubmission: 0,
  submissionCounter: 0,
  segmentationRequestTime: null,

  isLoadingSegmentation: false,
  isSubmittingSegmentation: false,
};

const mutations = {
  SET_SESSION_ID(state, payload) {
    state.sessionId = payload.sessionId;
  },

  SET_TEST_IMAGES(state, payload) {
    state.testImages = payload.testImages;
  },

  SET_CURRENT_IMAGE_FIRST_INTERACTION(state, payload) {
    state.currentImageFirstInteraction = payload.currentImageFirstInteraction;
  },

  SET_CURRENT_IMAGE_STARTED_AT(state, payload) {
    state.currentImageInteractionStartingTime = payload.interactionStartingTime;
  },

  SET_PREVIOUS_SCRIBBLE_TYPE(state, payload) {
    state.previousScribbleType = payload.scribbleType;
  },

  SET_SCRIBBLES(state, payload) {
    state.scribbles = payload.scribbles;
  },

  SET_FOREGROUND_SCRIBBLES(state, payload) {
    state.foregroundScribbles = payload.scribbles;
  },

  SET_BACKGROUND_SCRIBBLES(state, payload) {
    state.backgroundScribbles = payload.scribbles;
  },

  SET_PIXELS_AT_SUBMISSION(state, payload) {
    state.pixelsAtSubmission = payload.pixels;
  },

  SET_FOREGROUND_PIXELS_AT_SUBMISSION(state, payload) {
    state.foregroundPixelsAtSubmission = payload.pixels;
  },

  SET_BACKGROUND_PIXELS_AT_SUBMISSION(state, payload) {
    state.backgroundPixelsAtSubmission = payload.pixels;
  },

  SET_SUBMISSION_COUNTER(state, payload) {
    state.submissionCounter = payload.value;
  },

  SET_SEGMENTATION_REQUEST_TIME(state, payload) {
    state.segmentationRequestTime = payload.segmentationRequestTime;
  },

  SET_IS_LOADING_SEGMENTATION(state, payload) {
    state.isLoadingSegmentation = payload.isLoading;
  },

  SET_IS_SUBMITTING_SEGMENTATION(state, payload) {
    state.isSubmittingSegmentation = payload.isSubmitting;
  }
};

const actions = {
  setSessionId({ commit }, id) {
    commit({
      type: 'SET_SESSION_ID',
      sessionId: id,
    });
  },

  setTestImages({ commit }, imageArray) {
    commit({
      type: 'SET_TEST_IMAGES',
      testImages: imageArray,
    });
  },

  setIsFirstInteractionFlag({ commit }, isFirstInteraction) {
    commit({
      type: 'SET_CURRENT_IMAGE_FIRST_INTERACTION',
      currentImageFirstInteraction: isFirstInteraction,
    });
  },

  punchInImageInteractionStartingTime({ commit }) {
    let now = new Date();
    let rightNowUTC = now.toUTCString();
    commit({
      type: 'SET_CURRENT_IMAGE_STARTED_AT',
      interactionStartingTime: rightNowUTC,
    });
  },

  incrementScribbleCount({ state, commit, rootState }) {
    const newCounter = state.scribbles + 1;
    commit({
      type: 'SET_SCRIBBLES',
      scribbles: newCounter
    });
    let currentScribbleIsForeground = rootState.canvasModule.brushType === 'fg';
    let {newTypeCount, commitType} = {
      newTypeCount: currentScribbleIsForeground ? state.foregroundScribbles + 1 : state.backgroundScribbles + 1,
      commitType: currentScribbleIsForeground ? 'SET_FOREGROUND_SCRIBBLES' : 'SET_BACKGROUND_SCRIBBLES',
    };
    commit({
      type: commitType,
      scribbles: newTypeCount
    });
  },

  decrementScribbleCount({ state, commit, rootState }) {
    if (state.scribbles === 0) return;
    let newCounter = state.scribbles - 1;
    commit({
      type: 'SET_SCRIBBLES',
      scribbles: newCounter
    });
    let previousScribbleIsForeground = rootState.canvasModule.brushType === 'fg';
    let {newTypeCount, commitType} = {
      newTypeCount: previousScribbleIsForeground ? state.foregroundScribbles - 1 : state.backgroundScribbles - 1,
      commitType: previousScribbleIsForeground ? 'SET_FOREGROUND_SCRIBBLES' : 'SET_BACKGROUND_SCRIBBLES',
    };
    commit({
      type: commitType,
      scribbles: newTypeCount
    });
  },

  resetScribbleCount({ commit }) {
    const scribbleMutationTypes = ['SET_SCRIBBLES', 'SET_FOREGROUND_SCRIBBLES', 'SET_BACKGROUND_SCRIBBLES'];

    for (let type of scribbleMutationTypes) {
      commit({type: type, scribbles: 0});
    }
  },

  setPreviousScribbleType({ commit }, type) {
    commit({
      'type': 'SET_PREVIOUS_SCRIBBLE_TYPE',
      'scribbleType': type,
    });
  },

  setCurrentPixelCounters({ commit }, pixelCount, foregroundPixelCount, backgroundPixelCount) {
    commit({
      type: 'SET_PIXELS_AT_SUBMISSION',
      pixels: pixelCount,
    });

    commit({
      type: 'SET_FOREGROUND_PIXELS_AT_SUBMISSION',
      pixels: foregroundPixelCount,
    });

    commit({
      type: 'SET_BACKGROUND_PIXELS_AT_SUBMISSION',
      pixels: backgroundPixelCount,
    });
  },

  incrementSubmissionCounter({ commit, state }) {
    let newValue = state.submissionCounter + 1;
    commit({
      type: 'SET_SUBMISSION_COUNTER',
      value: newValue,
    });
  },

  resetSubmissionCounter({ commit }) {
    commit({
      type: 'SET_SUBMISSION_COUNTER',
      value: 0,
    });
  },

  punchInSegmentationTime({ commit }) {
    let now = new Date();
    let rightNowUTC = now.toUTCString();
    commit({
      type: 'SET_SEGMENTATION_REQUEST_TIME',
      segmentationRequestTime: rightNowUTC,
    });
  },

  setIsLoadingFlag({ commit }, isLoading) {
    commit({
      type: 'SET_IS_LOADING_SEGMENTATION',
      isLoading: isLoading,
    });
  },

  setIsSubmittingFlag({ commit }, isSubmitting) {
    commit({
      type: 'SET_IS_SUBMITTING_SEGMENTATION',
      isSubmitting: isSubmitting,
    });
  },

  resetInteractionState({ commit }) {
    commit({
      type: 'SET_CURRENT_IMAGE_FIRST_INTERACTION',
      currentImageFirstInteraction: true,
    });

    commit({
      type: 'SET_CURRENT_IMAGE_STARTED_AT',
      interactionStartingTime: null,
    });

    commit({
      type: 'SET_SCRIBBLES',
      scribbles: 0,
    });

    commit({
      type: 'SET_FOREGROUND_SCRIBBLES',
      scribbles: 0,
    });

    commit({
      type: 'SET_BACKGROUND_SCRIBBLES',
      scribbles: 0,
    });

    commit({
      type: 'SET_SUBMISSION_COUNTER',
      value: 0,
    });

    commit({
      type: 'SET_SEGMENTATION_REQUEST_TIME',
      segmentationRequestTime: null,
    });
  },
};

const getters = {
  getSessionId: state => state.sessionId,
  getCurrentImageIndex: state => state.currentImageIndex,
  getCurrentImageFirstInteraction: state => state.currentImageFirstInteraction,
  getScribbleCounter: state => state.scribbles,
  getForegroundScribbleCounter: state  => state.foregroundScribbles,
  getBackgroundScribbleCounter: state  => state.backgroundScribbles,
  hasNoScribbles: state => state.scribbles === 0,
  isLoadingSegmentation: state => state.isLoadingSegmentation,
  isSubmittingSegmentation: state => state.isSubmittingSegmentation,
};

const interactionSessionModule = {
  state,
  mutations,
  actions,
  getters,
}

export default interactionSessionModule;