<template>
  <div class="outsideWrapper">
    <div class="insideWrapper">
      <img :src="dhmImageSrc" class="baseImage" ref="dhmImg">
      <img v-if="displayedSegmentation"
           :src="displayedSegmentation.dataUri"
           :style="segmentationOverlayStyle"
           class="segImage" ref="segImg">
      <canvas :style="{visibility: isCanvasDisplaySelected ? 'visible' : 'hidden'}"
        class="overlayCanvas" ref="canvas"></canvas>
    </div>
  </div>
</template>

<script>
import colormap from "colormap";
import {mapGetters, mapActions} from 'vuex';
import {colorToPixelType, getImageDataURIFromDataArray, pixelTypeToColor} from "@/helpers/canvas";
import {APIService as grabcutAPIService} from "@/api/grabcutAPI";

const grabcutAS = new grabcutAPIService();

export default {
  name: 'InteractionCanvas',

  data() {
    return {
      dhmColorSpace: colormap({
        'colormap': 'jet',
        'nshades': 256,
        'format': 'rgba',
        'alpha': 1,
      }),
      maskColorSpace: colormap({
        'colormap': 'viridis',
        'nshades': 256,
        'format': 'rgba',
        'alpha': 1,
      }),
      dhmImageSrc: '',
      segmentationSrc: '',
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
      pointsPerScribble: [],
    };
  },

  computed: {
    ...mapGetters({
      isFirstInteraction: 'getCurrentImageFirstInteraction',
      brushType: 'getBrushType',
      brushSize: 'getBrushSize',
      segmentationContexts: 'getSegmentationContexts',
      segmentationCounter: 'getSegmentationCounter',
      latestSegmentation: 'getLatestSegmentation',
      displayedSegmentation: 'getDisplayedSegmentation',
      isCanvasDisplaySelected: 'isCanvasDisplaySelected',
      isMaskDisplaySelected: 'isMaskDisplaySelected'
    }),

    segmentationOverlayStyle() {
      return {
        opacity: 0.4,
        visibility: this.isMaskDisplaySelected ? 'visible' : 'hidden',
      };
    }
  },

  async created() {
    await this.loadImage();
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
    ...mapActions([
      'incrementScribbleCount',
      'decrementScribbleCount',
      'resetScribbleCount',

      'punchInImageInteractionStartingTime',
      'punchInSegmentationTime',
      'incrementSubmissionCounter',

      'setIsFirstInteractionFlag',
      'setIsCanvasEmptyFlag',

      'setSegmentationForDisplay',
    ]),

    clearDrawings() {
      this.canvasCtx.clearRect(0, 0, this.canvasCtx.canvas.width, this.canvasCtx.canvas.height);
      this.setSegmentationForDisplay(null);

      this.points = [];
      this.redoStack = [];
      this.pointsPerScribble = [];
      this.resetScribbleCount();
      this.$store.dispatch('setPreviousScribbleType', null);
    },

    setUpBrush() {
      this.canvasCtx.lineCap = 'square';
      if (this.canvasCtx.lineWidth !== this.brushSize) {
        this.canvasCtx.lineWidth = this.brushSize;
      }
      if (this.canvasCtx.strokeStyle !== pixelTypeToColor[this.brushType]) {
        this.canvasCtx.strokeStyle = pixelTypeToColor[this.brushType];
      }
    },

    repositionMouse(e) {
      let {left, top} = this.$refs.canvas.getBoundingClientRect();
      this.mouseX = parseInt(e.clientX - left);
      this.mouseY = parseInt(e.clientY - top);
    },

    startMousePath(e) {
      if (this.isFirstInteraction) {
        this.punchInImageInteractionStartingTime();
        this.setIsFirstInteractionFlag(false);
      }

      this.setUpBrush();
      this.$refs.canvas.addEventListener('mousemove', this.draw);
      this.repositionMouse(e);
      this.pointsPerScribble.push(0);
      this.addPointToCurrentStroke("begin");
      this.incrementScribbleCount();
    },

    stopMousePath() {
      if (!this.drawing) {
        return;
      }
      this.$refs.canvas.removeEventListener('mousemove', this.draw);
      this.addPointToCurrentStroke("end");
      this.drawing = false;

      this.$store.dispatch('setPreviousScribbleType', this.brushType);
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
      const point = {
        'x': this.mouseX,
        'y': this.mouseY,
        'size': this.brushSize,
        'color': this.canvasCtx.strokeStyle,
        'trigger': trigger,
      };

      this.points.push(point);

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
          this.$store.dispatch('setPreviousScribbleType', colorToPixelType[point.color]);
        }
      }
    },

    undoLastStroke() {
      if (this.pointsPerScribble.length === 0 || this.points.length === 0) return;

      let undoScribbleLength = this.pointsPerScribble.pop();
      this.points.splice(-undoScribbleLength);
      this.decrementScribbleCount();
      this.redrawAllPoints();
    },

    async loadImage() {
      let currentImgId = 1;  //TODO fix this hard-coded index

      let colors = colormap({
        'colormap': 'jet',
        'nshades': 255,
        'format': 'rgba',
        'alpha': 1
      });

      await grabcutAS.getDHMImage(currentImgId).then(imageDataArray => {
        this.dhmImageSrc = getImageDataURIFromDataArray(imageDataArray, colors, this.width, this.height);
      }, error => {
        console.error(error);
      });
    },

    hasScribbles() {
      let isPixelWhite = (elt, idx, arr) => {
        if (idx % 4 === 0) {
          return arr[idx] === 0
            && arr[idx + 1] === 0
            && arr[idx + 2] === 0
            && arr[idx + 3] === 255;
        }
      };

      return this.canvasCtx.getImageData(
        0,
        0,
        this.canvasCtx.canvas.width,
        this.canvasCtx.canvas.height).every(isPixelWhite);
    },

    async segment() {
      this.incrementSubmissionCounter();
      this.punchInSegmentationTime();

      return this.$store.dispatch('getSegmentation', {
        imageData: this.canvasCtx.getImageData(0, 0, this.width, this.height).data,
        colors: this.maskColorSpace,
      }).then(
        () => {
          this.$store.dispatch('setSegmentationForDisplay', this.latestSegmentation);
        }
      );
    },

    async submitDisplayedMask() {
      return this.$store.dispatch('submitDisplayedMask')
        .then(
          () => {
            this.$store.dispatch('resetInteractionState');
            this.$store.dispatch('resetCanvasState');
            this.$store.dispatch('clearSegmentations');
            this.clearDrawings();
          }
        );
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

  .segImage {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0px;
    left: 0px;
  }
</style>