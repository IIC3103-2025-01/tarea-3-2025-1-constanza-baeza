import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [pregunta, setPregunta] = useState("");
  const [respuesta, setRespuesta] = useState("");
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  const handleIndexar = async () => {
    setError("");
    setCargando(true);
    try {
      const res = await fetch("http://localhost:8000/indexar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await res.json();
      if (data.fragmentos_indexados === 0) {
        setError("No se pudieron indexar fragmentos.");
      } else {
        alert(`Se indexaron ${data.fragmentos_indexados} fragmentos.`);
      }
    } catch (e) {
      setError("Error al indexar: " + e.message);
    } finally {
      setCargando(false);
    }
  };

  const handlePreguntar = async () => {
    setError("");
    setCargando(true);
    try {
      const res = await fetch("http://localhost:8000/preguntar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pregunta }),
      });
      const data = await res.json();
      setRespuesta(data.respuesta || "Sin respuesta.");
    } catch (e) {
      setError("Error al preguntar: " + e.message);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Wikipedia Chatbot 🧠</h1>

      <input
        type="text"
        placeholder="URL de Wikipedia en inglés"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "100%", padding: 8, marginBottom: 10 }}
      />
      <button onClick={handleIndexar} disabled={cargando}>
        Indexar Artículo
      </button>

      <hr />

      <input
        type="text"
        placeholder="¿Qué quieres saber?"
        value={pregunta}
        onChange={(e) => setPregunta(e.target.value)}
        style={{ width: "100%", padding: 8, marginBottom: 10 }}
      />
      <button onClick={handlePreguntar} disabled={cargando}>
        Preguntar
      </button>

      {cargando && <p>Cargando...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Respuesta:</h2>
      <p>{respuesta}</p>
    </div>
  );
}

export default App;
