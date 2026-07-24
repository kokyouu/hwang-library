import { ref } from 'vue'
import { onAuthStateChanged } from 'firebase/auth'

import { auth } from './firebase/init'

export const firebaseUser = ref(null)
export const firebaseRole = ref('')

const roleStorageKey = (email) => `hwang-library-firebase-role:${email}`

export const saveFirebaseRole = (email, role) => {
  localStorage.setItem(roleStorageKey(email), role)
  firebaseRole.value = role
}

export const getFirebaseRole = (email) => localStorage.getItem(roleStorageKey(email)) || 'Member'

onAuthStateChanged(auth, (user) => {
  firebaseUser.value = user
  firebaseRole.value = user ? getFirebaseRole(user.email) : ''
})
