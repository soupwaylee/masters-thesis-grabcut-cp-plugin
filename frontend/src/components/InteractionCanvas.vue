<template>
  <div class="outsideWrapper">
    <div class="insideWrapper">
      <img :src="dhmImageSrc" class="baseImage" ref="dhmImg">
      <canvas class="overlayCanvas" ref="canvas"></canvas>
    </div>
  </div>
</template>

<script>
import colormap from "colormap";
import {APIService as grabcutAPIService} from "../api/grabcutAPI";

const grabcutAS = new grabcutAPIService();

export default {
  name: 'InteractionCanvas',
  data() {
    return {
      dhmImageSrc: '',
      canvasCtx: null,
      width: 512,
      height: 384,
      mouseX: 0,
      mouseY: 0,
    };
  },
  computed: {
    brushType() {
      return this.$store.getters.getBrushType;
    },

    brushSize() {
      return this.$store.getters.getBrushSize;
    },
  },
  async created() {
    this.loadImage()
      .catch(e => {
          //TODO implement better error handling here later
          console.log(`Problem: ${e}`)
        }
      )
  },
  mounted() {
    const canvas = this.$refs.canvas;
    this.canvasCtx = canvas.getContext('2d');
    canvas.addEventListener('mousedown', this.startMousePath);
    canvas.addEventListener('mouseup', this.stopMousePath);
    window.addEventListener('resize', this.resize);
    this.resize();
  },
  methods: {
    repositionMouse(e) {
      this.mouseX = e.clientX - this.$refs.canvas.getBoundingClientRect().left;
      this.mouseY = e.clientY - this.$refs.canvas.getBoundingClientRect().top;
    },

    startMousePath(e) {
      this.$refs.canvas.addEventListener('mousemove', this.draw);
      this.repositionMouse(e);
    },

    stopMousePath() {
      this.$refs.canvas.removeEventListener('mousemove', this.draw);
    },

    draw(e) {
      this.canvasCtx.beginPath();
      this.canvasCtx.lineWidth = this.brushSize;
      this.canvasCtx.lineCap = 'square';
      this.canvasCtx.strokeStyle = ((this.brushType === 'fg') ? 'rgba(255, 0, 0, 1)' : 'rgba(0, 0, 255, 1)');
      this.canvasCtx.moveTo(this.mouseX, this.mouseY);
      this.repositionMouse(e);
      this.canvasCtx.lineTo(this.mouseX, this.mouseY);
      this.canvasCtx.stroke();
    },

    resize() {
      this.canvasCtx.canvas.width = this.width;
      this.canvasCtx.canvas.height = this.height;
    },

    async loadImage() {
      let currentImgIdx = 1;
      let pendingDHMImage = grabcutAS.getDHMImage(currentImgIdx);
      //     .then( (data) => {
      //        phaseImgDataArray = data;
      //        console.log(`Loaded ${phaseImgDataArray.length} long list.`);
      //      });

      const dhmCanvas = document.createElement('canvas');
      dhmCanvas.width = this.width;
      dhmCanvas.height = this.height;

      const dhmCtx = dhmCanvas.getContext('2d');
      const dhmImgData = dhmCtx.getImageData(0, 0, dhmCanvas.width, dhmCanvas.height);

      let colors = colormap({
        colormap: 'jet',
        nshades: 255,
        format: 'rgba',
        alpha: 1
      })

      let phaseImgDataArray = await pendingDHMImage;
      for (const [idx, intVal] of phaseImgDataArray.entries()) {
        let imgDataOffset = idx * 4;

        dhmImgData.data[imgDataOffset] = colors[intVal][0];
        dhmImgData.data[imgDataOffset + 1] = colors[intVal][1];
        dhmImgData.data[imgDataOffset + 2] = colors[intVal][2];
        dhmImgData.data[imgDataOffset + 3] = 255; // fully opaque
      }

      dhmCtx.putImageData(dhmImgData, 0, 0);
      this.dhmImageSrc = dhmCanvas.toDataURL();
    }
  }
}
</script>

<style scoped lang="scss">
  .outsideWrapper {
    width: 512px;
    height: 382px;
  }

  .insideWrapper {
    width: 100%;
    height: 100%;
    position: relative;
  }

  .baseImage {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0px;
    left: 0px;
  }

  .overlayCanvas {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0px;
    left: 0px;
  }
</style>