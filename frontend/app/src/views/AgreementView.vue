<script>
import {checkSession} from "@/scripts/utils.js";
import {getCSRFToken} from "@/scripts/utils.js";
export default {
  data() {
    return {
      loading: true
    }
  },
  async mounted() {
    this.loading = await checkSession(this.$router);
  },
  methods: {
    async submitAgreement() {
      const response = await fetch("/api/agreement/contract", {
        method: "POST",
        headers: {
          'X-CSRF-TOKEN': getCSRFToken(),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ agree: "on" }) // Send 'agree' as JSON
      });

      if (response.ok) {
        this.$router.push({ name: "instruction" }); // Navigate to instruction page
      }
    }
  }
}
</script>
<template>
  <div id="ins-main"
       class="d-flex flex-column justify-content-between align-items-center mt-1 mt-md-4"
       v-if="!loading">

    <div class="card border-light-subtle mb-md-3 mb-1 mt-1 mt-md-3"
         style="max-width: 70%; width:auto; max-height:70%; height:auto;">
      <div class="card-body"
           style="height: 70vh; overflow-y: auto;">
        <h1 class="text-center">Umowa o zachowaniu poufności</h1>
        <p class="text-justify fs-6 text-md-f">
          <h4> Umowa o Zachowaniu Poufności w Procesie Ręcznej Weryfikacji Zdigitalizowanych Honorowych Kart Krwiodawców </h4>
          <h5> Sekcja 1: Identyfikacja Stron </h5>
          - <b>Administrator Danych</b>: Polski Czerwony Krzyż z siedzibą w Warszawie (00-561) przy ul. Mokotowskiej 14, iod@pck.pl
          <br>
          - <b>Weryfikator</b>: [Imię i nazwisko, adres, dane kontaktowe]
          <br> <br>
          <h5>Sekcja 2: Zakres i Cel</h5>
          Weryfikator przyjmuje do wiadomości, że: <br>
          1. Jego zadaniem jest wyłącznie potwierdzenie zgodności zdigitalizowanych danych (numery PESEL, imiona i nazwiska, daty urodzenia, ilość oddanej krwi) z zeskanowanymi honorowymi kartami krwiodawców dostarczonymi przez Administratora Danych. <br>
          2. Weryfikator nie nabywa żadnych praw do przechowywania, kopiowania lub wykorzystywania tych danych w celach innych niż wskazane powyżej.
          <br> <br>
          <h5>Sekcja 3: Obowiązki</h5>
          Weryfikator zobowiązuje się do: <br>
          1. Wykorzystywania udostępnionych danych osobowych wyłącznie w procesie weryfikacji zgodnie z instrukcjami Administratora Danych. <br>
          2. Zachowania danych w ścisłej poufności i nieujawniania ich osobom trzecim. <br>
          3. Nie kopiowania, zapisywania ani przechowywania danych w żadnej formie poza zatwierdzonym procesem weryfikacji. <br>
          4. Zwrócenia lub usunięcia wszystkich danych po zakończeniu weryfikacji, zgodnie z instrukcjami Administratora Danych.
          <br> <br>
          <h5>Sekcja 4: Zasady RODO</h5>
          Weryfikator przyjmuje do wiadomości zasady RODO, w tym: <br>
          1. Przetwarzanie danych zgodnie z prawem, w sposób rzetelny i przejrzysty (<b>Art. 5 RODO</b>). <br>
          2. Utrzymanie poufności i integralności danych osobowych (<b>Art. 32 RODO</b>).
          <br> <br>
          <h5>Sekcja 5: Konsekwencje Naruszenia</h5>
          Naruszenie warunków niniejszej umowy może skutkować: <br>
          1. Natychmiastowym zakończeniem współpracy w ramach procesu weryfikacji. <br>
          2. Podjęciem działań prawnych na podstawie obowiązujących przepisów dotyczących ochrony danych osobowych, w tym kar wynikających z RODO.
          <br> <br>
          <h5>Sekcja 6: Potwierdzenie</h5>
          Podpisując tę umowę, Weryfikator potwierdza zrozumienie i akceptację opisanych powyżej obowiązków i zobowiązań.
        </p>
      </div>
    </div>

    <div class="m-3 align-items-center w-50 d-flex justify-content-center mt-1 mt-md-5">
      <button class="btn btn-primary w-100 btn-lg" @click="submitAgreement">ZGADZAM SIĘ</button>
    </div>
  </div>
</template>
<style scoped>
body {
  overflow: hidden;
}

p {
  text-align: justify;
}

@media(max-width: 1000px) {
  div.d-flex {
    margin-top: 80px !important;
    justify-content: start !important;
  }

  div.card {
    max-width: 95% !important;
  }
}

@media(max-width: 768px) {
  div.card {
    margin-bottom: 0 !important;
  }

  div.card-body {
    height: 60vh !important;
  }

  button.btn.btn-lg {
    font-size: 5vw !important;
    width: 100% !important;
  }
}

@media (max-height: 700px) and (max-width: 768px) {
  div.card-body {
    height: 50vh !important;
  }
}
</style>
