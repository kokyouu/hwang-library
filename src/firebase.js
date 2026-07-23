import { getApp, getApps, initializeApp } from 'firebase/app'

import { getAuth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: 'AIzaSyCcNlpMxOUqD8x2DLmI3GFMlE4PC_hUqUo',
  authDomain: 'hwang-library-lab7.firebaseapp.com',
  projectId: 'hwang-library-lab7',
  storageBucket: 'hwang-library-lab7.firebasestorage.app',
  messagingSenderId: '1008155963147',
  appId: '1:1008155963147:web:df17597bf471ea19c97c0e'
}

/*
 * Initialize Firebase only once.
 * This prevents duplicate initialization during Vite hot reload.
 */
const firebaseApp = getApps().length > 0 ? getApp() : initializeApp(firebaseConfig)

/*
 * Firebase Authentication instance.
 * Registration, login and logout pages will import this.
 */
export const auth = getAuth(firebaseApp)

export default firebaseApp
