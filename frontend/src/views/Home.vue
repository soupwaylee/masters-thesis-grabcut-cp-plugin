<template>
  <Card class="noTotalWidth p-shadow-5">
    <template #title>
      <div class="title-wrapper">
        <span class="title">GrabCut</span>
        <Button icon="pi pi-info-circle"
          @click="openGrabCutInfo"/>
        <Dialog v-model:visible="displayInfo"
          :closeOnEscape="true"
          :dismissableMask="true"
          :closable="true">
          <div class="dialog-header">
            <h3>GrabCut</h3>
          </div>

          This is GrabCut. Explainations will follow.

        </Dialog>
      </div>
    </template>
      <template #content>
      <div class="tool-wrapper">
        <RadioButton id="brush1" name="brushType" value="fg" v-model="brushType" />
        <label for="brush1">Foreground</label>
        <RadioButton id="brush2" name="brushType" value="bg" v-model="brushType" />
        <label for="brush2">Background</label>
        <Slider v-model="brushSizeRange" 
          :range="true" 
          ref="brushSizeSlider"
        />
        <span class="p-buttonset">
          <Button label="Undo" icon="pi pi-undo" />
          <Button label="Redo" icon="pi pi-refresh" />
          <Button label="Clear" icon="pi pi-trash" />
        </span>
      </div>
      <canvas id="canvas" ref="canvas"></canvas>
    </template>
  </Card>
</template>

<script>
// import { ref } from 'vue';
// import { APIService as grabcutAPIService } from "../api/grabcutAPI";
// const grabcutAS = new grabcutAPIService();
export default {
  name: "App",
  data() {
    return {
      displayInfo: false,
			brushType: 'fg',
      brushSize: 2,
			brushSizeRange: [0,30],
      canvasCtx: null,
      mouseX: 0,
      mouseY: 0,
    };
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
		openGrabCutInfo() {
			this.displayInfo = true;
		},
    reposition(e) {
      this.mouseX = e.clientX - this.$refs.canvas.getBoundingClientRect().left;
      this.mouseY = e.clientY - this.$refs.canvas.getBoundingClientRect().top;
    },
    startMousePath(e) {
      this.$refs.canvas.addEventListener('mousemove', this.draw);
      this.reposition(e);
    },
    stopMousePath() {
      this.$refs.canvas.removeEventListener('mousemove', this.draw);
    },
    draw(e) {
      this.canvasCtx.beginPath();
      this.canvasCtx.lineWidth = this.$refs.brushSizeSlider.modelValue; // TODO = this.brushWidth;
      // console.log(`${this.canvasCtx.ctx.lineWidth}`);
      this.canvasCtx.lineCap = 'square';
      this.canvasCtx.strokeStyle = 'rgba(255, 0, 0, 1)';
      this.canvasCtx.moveTo(this.mouseX, this.mouseY);
      this.reposition(e);
      this.canvasCtx.lineTo(this.mouseX, this.mouseY);
      this.canvasCtx.stroke();
    },
    resize() {
      this.canvasCtx.canvas.width = 512;
      this.canvasCtx.canvas.height = 384;
    },
  },
};
</script>

<style lang="scss">
.noTotalWidth {
  width: 80%;
  margin: auto;
}
</style>
