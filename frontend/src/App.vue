<template>
  <div id="nav">
    <router-link to="/">Example</router-link> |
    <router-link to="/about">About this plugin</router-link>
  </div>
  <router-view/>
</template>

<script>
export default {
  watch: {
    // Keep an eye on changes of the location (URL)
    $route() { // You could get "to" and "from" information like this: $route(to, from) {
      // If I'm in a iframe...
      if(window.parent && (window.parent!=window)) {
        // notify the parent (cp-component-core, where the dashboard is)
        // of the location change
        window.parent.postMessage("locationChangedNotification", "*");
      }
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
