import { getApp, getApps, initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: 'AIzaSyCcNlpMxOUqD8x2DLmI3GFMlE4PC_hUqUo',
  authDomain: 'hwang-library-lab7.firebaseapp.com',
  projectId: 'hwang-library-lab7',
  storageBucket: 'hwang-library-lab7.firebasestorage.app',
  messagingSenderId: '1008155963147',
  appId: '1:1008155963147:web:df17597bf471ea19c97c0e'
}

const firebaseApp = getApps().length > 0 ? getApp() : initializeApp(firebaseConfig)

export const auth = getAuth(firebaseApp)
export const db = getFirestore(firebaseApp)

export default firebaseApp
