const state = {
  brushType: 'fg',
  brushSize: 1,
};

const mutations = {
  SET_BRUSHTYPE (state, payload) {
    state.brushType = payload.brushType;
  },
  SET_BRUSHSIZE (state, payload) {
    state.brushSize = payload.brushSize;
  },
};

const actions = {
  setBrushType ({ commit }, payload) {
    commit('SET_BRUSHTYPE', payload);
  },
  setBrushSize ({ commit }, payload) {
    commit('SET_BRUSHSIZE', payload);
  },
};

const getters = {
  getBrushType: state => state.brushType,
  getBrushSize: state => state.brushSize,
};

const canvasModule = {
  state,
  mutations,
  actions,
  getters,
}

export default canvasModule;