const state = {
  brushType: 'fg',
  brushSize: 2,
  brushSizes: [
    {label: '2px', size: 2},
    {label: '4px', size: 4},
    {label: '8px', size: 8},
    {label: '12px', size: 12},
    {label: '16px', size: 16},
    {label: '20px', size: 20},
    {label: '24px', size: 24},
  ],
  maskOpacity: 40,
  isCanvasEmpty: true,
  isImageLoading: false,
  currentlyDisplayedSegmentation: null,
  isCanvasVisible: true,
  isMaskVisible: true,
};

const mutations = {
  SET_BRUSHTYPE (state, payload) {
    state.brushType = payload.brushType;
  },
  SET_BRUSHSIZE (state, payload) {
    state.brushSize = payload.brushSize;
  },
  SET_MASK_OPACITY (state, payload) {
    state.maskOpacity = payload.opacity;
  },
  SET_IS_CANVAS_EMPTY (state, payload) {
    state.isCanvasEmpty = payload.isEmpty;
  },
  SET_IS_IMAGE_LOADING (state, payload) {
    state.isImageLoading = payload.isLoading;
  },
  SET_IS_CANVAS_VISIBLE (state, payload) {
    state.isCanvasVisible = payload.isCanvasVisible;
  },
  SET_IS_MASK_VISIBLE (state, payload) {
    state.isMaskVisible = payload.isMaskVisible;
  },
  SET_CURRENTLY_DISPLAYED_SEGMENTATION (state, payload) {
    state.currentlyDisplayedSegmentation = payload.segmentation;
  },
};

const actions = {
  setBrushType ({ commit }, payload) {
    commit('SET_BRUSHTYPE', payload);
  },
  setBrushSize ({ commit }, payload) {
    commit('SET_BRUSHSIZE', payload);
  },
  setIsCanvasEmptyFlag({ commit }, payload) {
    commit('SET_IS_CANVAS_EMPTY', payload);
  },
  setIsImageLoadingFlag({ commit }, isLoading) {
    commit({type: 'SET_IS_IMAGE_LOADING', isLoading: isLoading});
  },
  setSegmentationForDisplay ({ commit }, segmentation) {
    commit({
      type: 'SET_CURRENTLY_DISPLAYED_SEGMENTATION',
      segmentation: segmentation
    });
  },
  resetCanvasState({ commit }) {
    commit({
      type: 'SET_BRUSHTYPE',
      brushType: 'fg'
    });
    commit({
      type: 'SET_BRUSHSIZE',
      brushSize: 1
    });
    commit({
      type: 'SET_CURRENTLY_DISPLAYED_SEGMENTATION',
      segmentation: null
    });
    commit({
      type: 'SET_IS_CANVAS_VISIBLE',
      isCanvasVisible: true,
    });
    commit({
      type: 'SET_IS_MASK_VISIBLE',
      isMaskVisible: true,
    });

  }
};

const getters = {
  getBrushType: state => state.brushType,
  getBrushSize: state => state.brushSize,
  getBrushSizes: state => state.brushSizes,
  getMaskOpacity: state => state.maskOpacity,
  getIsCanvasEmpty: state => state.brushSize,
  getIsImageLoading: state => state.isImageLoading,
  getIsCanvasVisible: state => state.isCanvasVisible,
  getIsMaskVisible: state => state.isMaskVisible,
  getDisplayedSegmentation: state => state.currentlyDisplayedSegmentation,
};

const canvasModule = {
  state,
  mutations,
  actions,
  getters,
}

export default canvasModule;