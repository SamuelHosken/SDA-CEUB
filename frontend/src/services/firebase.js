import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
} from "firebase/auth";
import { getFirestore } from "firebase/firestore";
const firebaseConfig = {
  apiKey: "AIzaSyDTAl1HKQUhJNn9YXcCXuVt_jxJEVvp_Uc",
  authDomain: "sda-ceub.firebaseapp.com",
  projectId: "sda-ceub",
  storageBucket: "sda-ceub.firebasestorage.app",
  messagingSenderId: "904261036948",
  appId: "1:904261036948:web:1aeab607d0be10d8443d81",
  measurementId: "G-CT7NFE64TY",
};
const app = initializeApp(firebaseConfig);
let analytics = null;
if (typeof window !== "undefined") {
  analytics = getAnalytics(app);
}
export const auth = getAuth(app);
export const db = getFirestore(app);
export const googleProvider = new GoogleAuthProvider();
export { analytics, app };
export const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    return result.user;
  } catch (error) {
    throw error;
  }
};
export const logout = async () => {
  try {
    await signOut(auth);
  } catch (error) {
    throw error;
  }
};
export { onAuthStateChanged };