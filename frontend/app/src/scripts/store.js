import { reactive, watch } from 'vue'

export const globalState = reactive({
  isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
})

watch(() => globalState.isAuthenticated, (newValue) => {
  localStorage.setItem('isAuthenticated', newValue)
})
