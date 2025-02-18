<script>
import {checkSession} from "@/scripts/utils.js";
import router from '@/router/index.js'

export default {
  data() {
    return {
      loading: false,
    }
  },
  async mounted() {
    this.loading = await checkSession(router);
  }
}
</script>
<template>
  <div class="wrapper" v-if="!loading">
    <p>TO JEST 404</p>
  </div>
</template>
