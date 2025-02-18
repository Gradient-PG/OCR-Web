<script>
import axios from 'axios'
import { getCSRFToken } from '@/scripts/utils.js'
import { globalState } from '@/scripts/store.js'
import router from '@/router/index.js'
export default {
  data() {
    return {
      email: null,
      csrfToken: null,
      error: null,
      loading: false,
      showModal: false,
    }
  },
  methods: {
    async goToLogin() {
      this.loading = true;
      try {
        const response = await axios.post(
          '/api/auth/send-password',
          {
            login: this.email,
          },
          {
            headers: {
              'X-CSRF-TOKEN': getCSRFToken(),
            },
          },
        )
        this.loading = false
        if (response.status === 200) {
          this.showModal = true
        }
      }
      catch (error) {
        this.loading = false
        this.error = error.response.data.message;
      }
    },
    closeModal() {
      this.showModal = false
      this.$router.push('/login')
    }
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
    <div class="card border-light-subtle mb-3 mt-5" style="max-width: 70%; width: 100%; max-height: 60%; height: 100%;">
      <div class="card-body p-3 d-flex flex-column justify-content-between">
        <h3 class="text-xl text-center my-4">PODAJ MAIL DO ZAREJESTROWANEGO KONTA</h3>
        <div class="d-flex flex-column align-items-center ">
          <input
            placeholder="Email..."
            class="form-control w-75 p-3 mb-3"
            type="email"
            name="email"
            v-model="email"
          />
        </div>
        <h5 class="text-center my-3">Jeśli nie masz jeszcze konta, napisz do [email]</h5>
        <div v-if="error" class="border border-danger p-3 rounded bg-light">
          <h3 class="text-center text-danger">{{ error }}</h3>
        </div>
        <div class="align-items-center mt-3 d-flex flex-column justify-content-between">
          <button class="btn btn-lg btn-primary w-50 mb-3" @click="goToLogin">WYŚLIJ HASŁO</button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="showModal" class="modal fade show d-block" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Sukces!</h5>
          <button type="button" class="btn-close" @click="showModal = false"></button>
        </div>
        <div class="modal-body">
          <p>Hasło zostało wysłane na podany adres email.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="closeModal">
            Zamknij
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="showModal" class="modal-backdrop fade show"></div>

  <div v-if="loading" class="loading-overlay">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal {
  display: block;
  background: rgba(0, 0, 0, 0.5);
}

.modal-dialog {
  max-width: 500px;
  margin: 100px auto;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}

@media (orientation: portrait) {
  div.card {
    height: 40% !important;
  }
}

@media(max-width: 768px) {
  div.card {
    height: 40% !important;
  }

  button.btn.btn-lg {
    font-size: 14px !important;
    width: 100% !important;
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
