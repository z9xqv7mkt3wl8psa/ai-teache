import React, { useState } from "react";
import axios from "axios";
import { FaPaperPlane, FaMicrophone, FaVolumeUp, FaClipboard, FaVideo  } from "react-icons/fa";
import { franc } from "franc-min";
import "./App.css";
import logo from "./assets/logo.jpg"; // Adjust the path if needed

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [detectedLang, setDetectedLang] = useState("en");
  const [chats, setChats] = useState([]); // Store previous chats
  const [showWelcome, setShowWelcome] = useState(true);
  const [isListening, setIsListening] = useState(false);
  const [isGeneratingVideo, setIsGeneratingVideo] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [copyMessage, setCopyMessage] = useState("");
  const [isSpeaking, setIsSpeaking] = useState(false);


  // Initialize Speech Recognition API
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.continuous = false;
  recognition.lang = "en-US";
  recognition.interimResults = false;

  recognition.onresult = (event) => {
    const spokenText = event.results[0][0].transcript;
    setQuery(spokenText);
    handleSend(spokenText);
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
  };

  const handleMicrophoneClick = () => {
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);
    }
  };

  const handleNewChat = () => {
    if (messages.length > 0) {
      setChats([{ id: Date.now(), messages }, ...chats]);
    }
    setMessages([]);
    setQuery("");
    setShowWelcome(true);
  };
 const handleGenerateVideo = async (text) => {
    if (!text.trim()) {
      alert("Please enter a topic first.");
      return;
    }

    setIsGeneratingVideo(true);

    try {
      const response = await axios.post("http://localhost:5000/generate_video", { query: text });

      if (response.data.video_url) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "🎬 Video generated! Click below to watch/download:", sender: "bot", video_url: response.data.video_url }
        ]);
      }
    } catch (error) {
      console.error("Video Generation Error:", error);
      alert("Failed to generate video.");
    } finally {
      setIsGeneratingVideo(false);
    }
  };

const handleSend = async (text = query) => {
    text = String(text).trim(); // ✅ Ensure text is always a string
    if (text === "") return;

    setMessages([...messages, { text, sender: "user" }]);
    setLoading(true);
    setIsLoading(true);
    setShowWelcome(false);

    try {
        const response = await axios.post("http://localhost:5000/search", { query: text });
        console.log("API Response:", response.data);

        if (response.data.result) {
            setMessages((prevMessages) => [...prevMessages, { text: response.data.result, sender: "bot" }]);

            // ✅ Automatically generate a video for the response
            handleGenerateVideo(text);
        }
    } catch (error) {
        console.error("API Error:", error);
    } finally {
        setTimeout(() => {
            setLoading(false);
            setIsLoading(false);
            setQuery("");
        }, 5);
    }
};

 const handleShare = () => {
    if (messages.length === 0) return;

    const chatText = messages
      .map((msg) => `${msg.sender === "user" ? "You" : "Bot"}: ${msg.text}`)
      .join("\n");

    navigator.clipboard.writeText(chatText).then(() => {
      setCopyMessage("Copied to clipboard!");
      setTimeout(() => setCopyMessage(""), 2000);
    });
  };

  const speakText = (text) => {
    if (!text) return;

    if (!("speechSynthesis" in window)) {
      alert("Text-to-Speech is not supported in this browser.");
      return;
    }

    if (isSpeaking) {
      speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    let detected = detectedLang;
    if (!detected || detected === "en") {
      const langCode = franc(text);
      const langMap = { hin: "hi", urd: "ur" };
      detected = langMap[langCode] || "en";
    }

    console.log("Final Language Used:", detected);

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = detected;

    utterance.onend = () => {
      setIsSpeaking(false);
    };

    setIsSpeaking(true);
    speechSynthesis.speak(utterance);
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md p-4 border-r">
        <div className="flex items-center gap-2 mb-4">
          <img src={logo} alt="PRASUNET Logo" className="w-10 h-10 object-contain" />
          <h2 className="text-2xl font-extrabold bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-transparent bg-clip-text drop-shadow-md tracking-wide">
            PRASUNET
          </h2>
        </div>

        <button className="w-full bg-blue-500 text-white px-4 py-2 rounded mt-4" onClick={handleNewChat}>
          New Chat
        </button>

        <div className="mt-6 text-gray-500">Recent Chats</div>
        <ul className="mt-2">
          {chats.map((chat) => (
            <li key={chat.id} className="p-2 bg-gray-200 rounded cursor-pointer mt-2">
              Chat {new Date(chat.id).toLocaleTimeString()}
            </li>
          ))}
        </ul>
      </aside>

      {/* Main Chat Window */}
      <main className="flex-1 flex flex-col justify-between bg-white relative max-w-screen-lg mx-auto">
        <header className="w-full h-16 bg-white shadow-md flex items-center justify-between px-6 border-b">
          <h1 className="text-xl font-bold text-gray-700">PRASUNET AI</h1>
          <button className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg flex items-center gap-2" onClick={handleShare}>
            <FaClipboard /> Share
          </button>
        </header>

        {copyMessage && (
          <div className="absolute top-20 right-6 bg-green-500 text-white px-4 py-2 rounded-md shadow-md">
            {copyMessage}
          </div>
        )}

        {showWelcome && messages.length === 0 && (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center transition-opacity duration-500 ease-in-out pointer-events-none">
            <h2 className="text-4xl font-extrabold text-gray-500 mb-2">Hi, I'm PRASUNET AI</h2>
            <p className="text-gray-500 text-lg">How can I assist you today?</p>
          </div>
        )}

        <div className="flex-1 p-4 overflow-y-auto">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"} mb-4`}>
              <div className={`p-4 rounded-lg shadow-md ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"} max-w-lg text-sm`}>
                {msg.text}
                {msg.sender === "bot" && (
                  <button className="ml-2 text-gray-500 hover:text-gray-700" onClick={() => speakText(msg.text)}>
                    <FaVolumeUp />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>

        {isLoading && <div className="flex justify-center mb-4"><div className="p-4 text-gray-800">Typing...</div></div>}

        <div className="border-t p-2 flex items-center">
          <button className={`p-3 rounded-full ${isListening ? "bg-red-500 text-white" : "bg-gray-200 text-gray-500"}`}
                  onClick={handleMicrophoneClick}>
            <FaMicrophone/>
          </button>
          <input type="text" className="flex-1 p-3 border rounded-lg outline-none" placeholder="Type your message..."
                 value={query} onChange={(e) => setQuery(e.target.value)}
                 onKeyDown={(e) => e.key === "Enter" && handleSend()}/>
          <button className="p-3 bg-blue-500 text-white rounded-lg" onClick={handleSend}><FaPaperPlane/></button>
          <button className="p-3 bg-green-500 text-white" onClick={handleGenerateVideo} disabled={isGeneratingVideo}>
            <FaVideo/></button>
        </div>
      </main>
    </div>
  );
}

export default App;

