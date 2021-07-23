<template>
  <div class="outsideWrapper">
    <div class="insideWrapper">
      <img src="" class="baseImage">
      <canvas class="overlayCanvas" ref="canvas"></canvas>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InteractionCanvas',
  data() {
    return {
      canvasCtx: null,
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
  created() {
    this.mouseX = 0;
    this.mouseY = 0;
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
      this.canvasCtx.lineWidth = this.$store.getters.getBrushSize;
      this.canvasCtx.lineCap = 'square';
      this.canvasCtx.strokeStyle = ((this.$store.getters.getBrushType === 'fg') ? 'rgba(255, 0, 0, 1)' : 'rgba(0, 0, 255, 1)');
      this.canvasCtx.moveTo(this.mouseX, this.mouseY);
      this.repositionMouse(e);
      this.canvasCtx.lineTo(this.mouseX, this.mouseY);
      this.canvasCtx.stroke();
    },

    resize() {
      this.canvasCtx.canvas.width = 512;
      this.canvasCtx.canvas.height = 384;
    },
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