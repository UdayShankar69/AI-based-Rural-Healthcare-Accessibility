import "./App.css";

function App() {

  // -----------------------------
  // Speech To Text
  // -----------------------------
  const startListening = () => {

    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

      alert("Speech Recognition not supported");

      return;
    }

    const recognition =
      new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();

    recognition.onresult = async (event) => {

      const text =
        event.results[0][0].transcript;

      // Show symptoms on webpage
      document.getElementById(
        "symptoms"
      ).innerText = text;

      // Send to backend
      const res = await fetch(
        "http://127.0.0.1:8000/check-symptoms",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            symptoms: text,
          }),
        }
      );

      const data = await res.json();

      // Show backend response
      document.getElementById(
        "response"
      ).innerHTML = data.guidance;
    };
  };

  // -----------------------------
  // Text To Speech
  // -----------------------------
  const speakText = () => {

    const text =
      document.getElementById(
        "response"
      ).innerText;

    const speech =
      new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";

    window.speechSynthesis.speak(speech);
  };

  return (

    <div className="container">

      <h1>
        🏥 Rural Healthcare Assistant
      </h1>

      {/* Buttons */}

      <div className="button-group">

        <button
          className="mic-btn"
          onClick={startListening}
        >
          🎤 Speak Symptoms
        </button>

        <button
          className="speak-btn"
          onClick={speakText}
        >
          🔊 Listen Response
        </button>

      </div>

      {/* Symptoms */}

      <div className="card">

        <h2>Your Symptoms</h2>

        <p id="symptoms">
          Speak something...
        </p>

      </div>

      {/* AI Response */}

      <div className="card">

        <h2>Medical Guidance</h2>

        <div id="response">
          AI response will appear here...
        </div>

      </div>

    </div>
  );
}

export default App;