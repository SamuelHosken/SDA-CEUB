import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { onAuthStateChanged, auth } from "../services/firebase";
function ProtectedRoute({ children }) {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  useEffect(() => {
    const token = localStorage.getItem("auth_token");
    if (!token) {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user");
      localStorage.removeItem("sda_session_id");
      setUser(null);
      setLoading(false);
      return;
    }
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        try {
          const token = await firebaseUser.getIdToken();
          localStorage.setItem("auth_token", token);
          setUser(firebaseUser);
        } catch (error) {
          console.error("Erro ao obter token:", error);
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user");
          localStorage.removeItem("sda_session_id");
          setUser(null);
        }
      } else {
        localStorage.removeItem("auth_token");
        localStorage.removeItem("user");
        localStorage.removeItem("sda_session_id");
        setUser(null);
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);
  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="spinner" />
      </div>
    );
  }
  const token = localStorage.getItem("auth_token");
  if (!user || !token) {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user");
    localStorage.removeItem("sda_session_id");
    return <Navigate to="/login" replace />;
  }
  return children;
}
export default ProtectedRoute;