import { useState } from "react";

function VoiceAssistant() {

  const [userText, setUserText] = useState("");
  const [response, setResponse] = useState("");
  const [isListening, setIsListening] = useState(false);

  // Speech To Text
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

    setIsListening(true);

    recognition.onresult = async (event) => {

      const text =
        event.results[0][0].transcript;

      setUserText(text);

      setIsListening(false);

      try {

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

        setResponse(data.guidance);

      } catch (error) {

        console.log(error);

        setResponse("Backend connection failed");
      }
    };
  };

  // Text To Speech
  const speakText = () => {

    const speech =
      new SpeechSynthesisUtterance(response);

    speech.lang = "en-US";

    window.speechSynthesis.speak(speech);
  };

  return (

    <div
      style={{
        padding: "30px",
        border: "2px solid #ccc",
        marginTop: "30px",
        borderRadius: "10px",
      }}
    >

      <h2>🎤 Voice Healthcare Assistant</h2>

      <button
        onClick={startListening}
        style={{
          padding: "10px",
          marginRight: "10px",
        }}
      >
        {isListening
          ? "Listening..."
          : "🎤 Speak Symptoms"}
      </button>

      <button
        onClick={speakText}
        style={{
          padding: "10px",
        }}
      >
        🔊 Listen Response
      </button>

      <div style={{ marginTop: "20px" }}>

        <h3>Your Symptoms:</h3>

        <p>{userText}</p>

      </div>

      <div>

        <h3>Medical Guidance:</h3>

        <div
          dangerouslySetInnerHTML={{
            __html: response,
          }}
        />

      </div>

    </div>
  );
}

export default VoiceAssistant;