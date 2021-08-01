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
      lastX: 0,
      lastY: 0,
      drawing: false,
      points: [],
      redoStack: [],
      pointsPerScribble: []
    };
  },
  computed: {
    brushType() {
      return this.$store.getters.getBrushType;
    },

    brushSize() {
      return this.$store.getters.getBrushSize;
    },

    selectedStrokeColor() {
      return (this.brushType === 'fg') ? 'rgba(255, 0, 0, 1)' : 'rgba(0, 0, 255, 1)'
    }
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
    //TODO mouseout will also trigger console log action..
    canvas.addEventListener('mouseout', this.stopMousePath);
    canvas.addEventListener('mouseup', this.stopMousePath);
    window.addEventListener('resize', this.resize);
    this.resize();
  },
  methods: {
    clearDrawings() {
      this.canvasCtx.clearRect(0, 0, this.canvasCtx.canvas.width, this.canvasCtx.canvas.height);
      this.points = [];
      this.redoStack = [];
      this.pointsPerScribble = [];
    },

    setUpBrush() {
      this.canvasCtx.lineCap = 'square';
      if (this.canvasCtx.lineWidth !== this.brushSize) {
        this.canvasCtx.lineWidth = this.brushSize;
      }
      if (this.canvasCtx.strokeStyle !== this.selectedStrokeColor) {
        this.canvasCtx.strokeStyle = (this.brushType === 'fg') ? 'rgba(255, 0, 0, 1)' : 'rgba(0, 0, 255, 1)';
      }
    },

    repositionMouse(e) {
      let { left, top } = this.$refs.canvas.getBoundingClientRect();
      this.mouseX = parseInt(e.clientX - left);
      this.mouseY = parseInt(e.clientY - top);
    },

    startMousePath(e) {
      this.setUpBrush();
      this.$refs.canvas.addEventListener('mousemove', this.draw);
      this.repositionMouse(e);
      this.pointsPerScribble.push(0);
      this.addPointToCurrentStroke("begin");
    },

    stopMousePath() {
      if (!this.drawing) {
        return;
      }
      this.$refs.canvas.removeEventListener('mousemove', this.draw);
      this.addPointToCurrentStroke("end");
      this.drawing = false;
      // console.log(e.buttons);
      // console.log(e.type);
      let reducer = (acc, curr) => acc + curr;
      console.log(`Scribbles: ${this.pointsPerScribble.length}`);
      console.log(`Points: ${this.points.length}`);
    },

    draw(e) {
      this.drawing = true;
      this.canvasCtx.beginPath();
      this.canvasCtx.moveTo(this.mouseX, this.mouseY);
      this.addPointToCurrentStroke("draw");
      this.repositionMouse(e);
      this.canvasCtx.lineTo(this.mouseX, this.mouseY);
      this.canvasCtx.stroke();
      this.lastX = this.mouseX;
      this.lastY = this.mouseY;
      this.addPointToCurrentStroke("draw");
    },

    resize() {
      this.canvasCtx.canvas.width = this.width;
      this.canvasCtx.canvas.height = this.height;
    },

    addPointToCurrentStroke(trigger) {
      this.points.push({
        x: this.mouseX,
        y: this.mouseY,
        size: this.brushSize,
        color: this.canvasCtx.strokeStyle,
        trigger: trigger
      });

      this.pointsPerScribble[this.pointsPerScribble.length - 1]++;
    },

    redrawAllPoints() {
      this.canvasCtx.clearRect(0, 0, this.canvasCtx.canvas.width, this.canvasCtx.canvas.height);

      for (const [i, point] of this.points.entries()) {
        let begin = false;

        if (this.canvasCtx.lineWidth !== point.size) {
          this.canvasCtx.lineWidth = point.size;
          begin = true;
        }
        if (this.canvasCtx.strokeStyle !== point.color) {
          this.canvasCtx.strokeStyle = point.color;
          begin = true;
        }
        if (point.trigger === 'begin' || begin) {
          this.canvasCtx.beginPath();
          this.canvasCtx.moveTo(point.x, point.y);
        }
        this.canvasCtx.lineTo(point.x, point.y);
        if (point.trigger === 'end' || (i === this.points.length - 1)) {
          this.canvasCtx.stroke();
        }
      }
    },

    undoLastStroke() {
      if (this.pointsPerScribble.length === 0 || this.points.length === 0) return;

      let undoScribbleLength = this.pointsPerScribble.pop();
      while (undoScribbleLength > 0) {
        let pt = this.points.pop();
        // this.redoStack.unshift(pt); TODO: unshift the discarded points to the redo stack
        undoScribbleLength -= 1;
      }

      this.redrawAllPoints();
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

      //TODO offer multiple options for color picking
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
    display: block;
    margin: 0 auto;
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