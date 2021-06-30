import { createStore } from 'vuex';
import canvasModule from './modules/canvas';

export default createStore({
  modules: {
    canvasModule
  }
});
