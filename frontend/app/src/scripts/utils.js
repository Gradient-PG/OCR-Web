import axios from "axios";

export async function checkSession() {
  try {
    const response = await axios.get('/api/auth/session', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    if (response.status !== 200) {
      this.$router.push('/')
    }
    else
      return false;
  } catch {
    this.$router.push('/')
  }
}

export async function adminCheckSession() {
  try {
    const response = await axios.get('/api/auth/session-admin', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    console.log(response)
    if (response.status !== 200) {
      this.$router.push('/')
    }
    else
      return true;
  } catch {
    this.$router.push('/')
  }
}

export function getCSRFToken() {
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let cookie of cookies) {
      cookie = cookie.trim()
      let [cookieName, cookieValue] = cookie.split('=')
      if (cookieName == 'csrftoken') return cookieValue
    }
  }
  return null
}

export function changeOrientation() {
  if (window.screen.width > 768) {
    document.querySelector('.wrapper').classList.add('horizontal')
    document.querySelector('.wrapper').classList.remove('vertical')
  } else {
    document.querySelector('.wrapper').classList.remove('horizontal')
    document.querySelector('.wrapper').classList.add('vertical')
  }
}
