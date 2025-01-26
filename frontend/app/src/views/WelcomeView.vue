<script>
import axios from 'axios'
import {getCSRFToken} from "@/scripts/utils.js";
export default {
  data() {
    return {
      email: null,
      csrfToken: null,
      error: null,
      message: "Jeśli nie masz jeszcze konta, napisz do [email]",
    }
  },
  methods: {
    async goToLogin() {
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
        if (response.status === 200) {
          alert(response.data.message)
          this.$router.push('/login')
        }
      }
      catch (error) {
        this.error = error;
      }
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
        <h5 class="text-center my-3">{{this.message}}</h5>
        <h3 v-if="error" class="text-center my-4">{{ error }}</h3>
        <div class="align-items-center d-flex flex-column justify-content-between">
          <button class="btn btn-lg btn-primary w-50 mb-3" @click="goToLogin">WYŚLIJ HASŁO</button>
        </div>
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
