<script>
import { globalState } from '@/scripts/store'
import { adminCheckSession } from '@/scripts/utils.js'
import axios from 'axios'
import { getCSRFToken } from '@/scripts/utils.js'
import router from '@/router/index.js'
export default {
  data() {
    return {
      email: null,
      password: null,
      csrfToken: null,
      error: null,
    }
  },
  methods: {
    async goToAgreement() {
      try {
        const response = await axios.post(
          '/api/auth/login',
          {
            login: this.email,
            password: this.password,
          },
          {
            headers: {
              'X-CSRF-TOKEN': getCSRFToken(),
            },
          },
        )
        if (response.status === 200) {
          globalState.isAuthenticated = true

          this.admin = await adminCheckSession(this.$router)

          if (this.admin) {
            this.$router.push({ name: 'admin' })
          } else {
            const response = await fetch('/api/agreement/contract', {
              method: 'GET',
              headers: {
                'X-CSRF-TOKEN': getCSRFToken(),
              },
            })

            if (response.ok) {
              const data = await response.json()
              if (data.message === 'You have already agreed to the contract.') {
                this.$router.push({ name: 'instruction' })
                return
              }
              if (data.message === 'You have not agreed to the contract yet.') {
                this.$router.push({ name: 'agreement' })
              }
            } else {
              const errorData = await response.json()
              console.error(errorData.error)
              alert(errorData.error)
            }
          }
        }
      } catch (error) {
        console.error(error)
        this.error = error.response.data.message
      }
    },
  },
  async mounted() {
    if (globalState.isAuthenticated) {
      await router.push({ name: 'instruction' })
    }
  },
}
</script>
<template>
  <div class="d-flex justify-content-center align-items-center mt-5">
    <div
      class="card border-light-subtle mb-3 mt-5"
      style="max-width: 70%; width: 100%; max-height: 60%; height: 100%"
    >
      <div class="card-body p-3 d-flex flex-column justify-content-between">
        <h2 class="text-xl text-center my-4">ZALOGUJ SIĘ ABY KONTUNOWAĆ...</h2>
        <div class="d-flex flex-column align-items-center">
          <input
            placeholder="Email..."
            class="form-control w-75 p-3 mb-3"
            type="email"
            name="email"
            v-model="email"
          />
          <input
            placeholder="Haslo..."
            class="form-control w-75 p-3 mb-3"
            type="password"
            name="password"
            v-model="password"
          />
        </div>
        <h5 class="text-center my-2">Jeśli nie masz jeszcze konta, napisz do [email]</h5>
        <h3 v-if="error" class="text-center my-4">{{ error }}</h3>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media (orientation: portrait) {
  div.card {
    height: 40% !important;
  }
}

@media (max-width: 768px) {
  div.card {
    height: 40% !important;
  }


  h2.text-xl {
    font-size: 18px !important;
  }

  input.form-control {
    width: 100% !important;
    margin: 5px !important;
  }
}
</style>
